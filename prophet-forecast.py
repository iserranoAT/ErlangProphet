#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import pandas as pd
import json
import os
import sys

from Prophet.forecast import forecast

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
		# Open a pair of null files
		self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
		# Save the actual stdout (1) and stderr (2) file descriptors.
		self.save_fds = (os.dup(1), os.dup(2))

	def __enter__(self):
		# Assign the null pointers to stdout and stderr.
		os.dup2(self.null_fds[0], 1)
		os.dup2(self.null_fds[1], 2)

	def __exit__(self, *_):
		# Re-assign the real stdout/stderr back to (1) and (2)
		os.dup2(self.save_fds[0], 1)
		os.dup2(self.save_fds[1], 2)
		# Close the null files
		os.close(self.null_fds[0])
		os.close(self.null_fds[1])

client_uuid = sys.argv[2]
forecast_params = json.loads(json.loads(sys.argv[3]))
df = pd.DataFrame(data={
	
	'ds': forecast_params['cvs']['ds'],
	'y': forecast_params['cvs']['y']
	
})

filename = client_uuid + '.json'

metric="mse" #Por ahora es esa de manera fija, pero hay que meterlo en Trello para que se fije en la interfaz

forecast, posterior_params = forecast(df=df,
									  args=forecast_params,
									  metric=metric,
									  output="/home/desarrollo/ErlangAnalytics/ErlangAnalytics/Data/")

sys.stdout.flush()
							
forecast = json.loads(forecast.to_json())

data = {
	"ds": forecast['ds'],
	"yhat": forecast['yhat'],
	"trend": forecast['trend'],
	"yhat_lower": forecast['yhat_lower'],
	"yhat_upper": forecast['yhat_upper'],
	"holidays": str(forecast['holidays']),
	"weekly": [],
	"monthly": [],
	"yearly": [],
	"holidays_consideradas": str(posterior_params["holidays"]),
	"changepoints": str(posterior_params["changepoints"]),
	"performance_metrics": posterior_params["metrics"]
}

file = open('../ErlangAnalytics/Data/' + filename, 'w')
file.write(json.dumps(data))
file.close()

#Importante no eliminar este mensaje
print("Finalizado")

sys.stdout.flush()
sys.stderr.close()