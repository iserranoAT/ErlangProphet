#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 

import paho.mqtt.client as mqtt
import os
import subprocess
import sys
import json


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

client = mqtt.Client()


def on_log(client, userdata, level, buf):
	print(("log: ", buf))

def on_connect(client, userdata, flags, rc):
	print('--> Conectado al servidor MQTT')
	client.subscribe("forecast/+/prophet/+/command")


def on_message(client, userdata, msg):
	
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

client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("svnhlhos", "C2dYodq4hmRj")
client.connect('m23.cloudmqtt.com', 17683, 240)

client.loop_forever()