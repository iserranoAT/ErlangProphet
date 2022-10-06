#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
import os
import subprocess
import sys
import json

import paho.mqtt.client as paho
from paho import mqtt


class suppress_stdout_stderr(object):
	'''
	A context manager for doing a "deep suppression" of stdout and stderr in
	Python, i.e. will suppress all print, even if the print originates in a
	compiled C/Fortran sub-function.
	   This will not suppress raised exceptions, since exceptions are printed
	to stderr just before a script exits, and after the context manager has
	exited (at least, I think that is why it lets exceptions through).

	'''

	def __init__(self):
		
		self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
		self.save_fds = (os.dup(1), os.dup(2))

	def __enter__(self):
		
		os.dup2(self.null_fds[0], 1)
		os.dup2(self.null_fds[1], 2)

	def __exit__(self, *_):
		
		os.dup2(self.save_fds[0], 1)
		os.dup2(self.save_fds[1], 2)
		os.close(self.null_fds[0])
		os.close(self.null_fds[1])

def on_log(client, userdata, level, buf):
	print(("log: ", buf))
	
def on_connect(client, userdata, flags, rc, properties=None):
	print('--> Conectado al servidor MQTT')
	client.subscribe("forecast/+/prophet/+/command")

def on_message(client, userdata, msg):
	
	print("--> Mensaje MQTT recibido")
	
	decoded_payload = msg.payload.decode("utf-8")
	
	client_uuid = msg.topic.split('/')[3]
	topic = "forecast/eCustomer/prophet/" + client_uuid + "/status"

	filename = client_uuid + '_data.json'
	
	print(('--> Ejecutando forecast solicitado por ', client_uuid))
	
	interpreter=sys.executable
	
	process = subprocess.Popen(
		[interpreter, "./prophet-forecast.py", "-u", client_uuid, json.dumps(decoded_payload)], stdout=subprocess.PIPE)
		
	while True:
		out = process.stdout.readline()
		out = out.decode("utf-8")
		
		if out == '' and process.poll() != None:
			break
		if out != '':
			client.publish(topic, out[:-1])
		client.loop()
	
	print('--> Terminado')

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("analyticaltribe", "Analytical1234")
client.connect("f6636b093da44e2e93194b58a0e2f350.s2.eu.hivemq.cloud", 8883)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()