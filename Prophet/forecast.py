import json
import os
import sys
import holidays
import logging
logging.getLogger('fbprophet').setLevel(logging.WARNING)

import pandas as pd
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import plot_cross_validation_metric
from fbprophet.plot import seasonality_plot_df
from loguru import logger

from Prophet.utils.prophet_utils import check_args, set_floor_cap, set_seasonalities, get_future_df, set_floor_cap, get_seasonal_components
import matplotlib.pyplot as plt

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
		
def forecast(df, args, metric, output):

    '''
    :param df (pandas DataFrame): Datos de entrada.
    :param args (python Dict): Parámetros a usar en el pronóstico.
    :param metric (python str): Métrica a usar para la validación cruzada. Usar alguna de las siguientes:
        'mse': mean squared error
        'rmse': root mean squared error
        'mae': mean absolute error
        'mape': mean absolute percent error
        'mdape': median absolute percent error
        'smape': symmetric mean absolute percentage error
        'coverage': coverage of the upper and lower intervals

    '''

    check_args(args)

    df['ds'] = pd.to_datetime(df["ds"]).dt.date

    years = list(set([elem.year for elem in df['ds']]))

    es_holidays = holidays.Spain(years=years)
    es_holidays = pd.DataFrame(list(es_holidays.items()))
    es_holidays.rename(columns={0: 'ds', 1: 'holiday'}, inplace=True)
    
    df = set_floor_cap(df, args['growth'])

    m = Prophet(growth=args['growth']['type'],
                holidays=es_holidays,
                changepoint_range=args['trend']['interval'],
                changepoint_prior_scale=args['trend']['sensibility'],
                holidays_prior_scale=args['holidays']['sensibility'],
                weekly_seasonality=True)

    m = set_seasonalities(m, args['seasonality'], args['seasonality']['fourier'], args['seasonality']['priorScale'])
    
    sys.stdout.flush()
    print("Cargando modelo")
    with suppress_stdout_stderr():
        m.fit(df)
        
    sys.stdout.flush()
    print("Ajustando modelo")
    with suppress_stdout_stderr():
        df_future = get_future_df(m, args['duration'], args['hourly'])
        df_future = set_floor_cap(df_future, args['growth'])

    logger.info(f"Starting forecast with duration of {args['duration']} days")
    forecast = m.predict(df_future)
    
    sys.stdout.flush()
    print("Validando forecast")
    with suppress_stdout_stderr():
        df_cv = cross_validation(m, args["cross_validation"]['horizon'], args["cross_validation"]['initial'], args["cross_validation"]['period'])
        cutoff = df_cv['cutoff'].unique()[0]
        df_cv = df_cv[df_cv['cutoff'].values == cutoff]

    sys.stdout.flush()
    print("Calculando métricas")

    metrics = performance_metrics(df_cv)
    
    sys.stdout.flush()
    print("Generando gráficas")
    
    '''
    daily=get_seasonal_components(model=m, seasonality_flags=args['seasonality'], component_name='daily', dates=df['ds'], frecuency='D')
    weekly=get_seasonal_components(model=m, seasonality_flags=args['seasonality'], component_name='weekly', dates=df['ds'], frecuency='W')
    monthly=get_seasonal_components(model=m, seasonality_flags=args['seasonality'], component_name='monthly', dates=df['ds'], frecuency='M')
    yearly=get_seasonal_components(model=m, seasonality_flags=args['seasonality'], component_name='yearly', dates=df['ds'], frecuency='Y')
    '''
    
    days = pd.date_range(start=df['ds'].min(), end=df['ds'].max())
        
    df_component = seasonality_plot_df(m, days)
    seas = m.predict_seasonal_components(df_component)
    
    posterior_params = {
        "changepoints": json.loads(m.changepoints.to_json()),
        "metrics": json.loads(metrics.to_json()),
        "holidays": json.loads(es_holidays.to_json()),
        "weekly": json.loads(seas["weekly"].to_json()) if args["seasonality"]["weekly"] else {},
        "monthly": json.loads(seas["monthly"].to_json()) if args["seasonality"]["monthly"] else {},
        "yearly": json.loads(seas["yearly"].to_json()) if args["seasonality"]["yearly"] else {},
    }
    
    sys.stdout.flush()
    print("Forecast finalizado")
    
    return forecast, posterior_params