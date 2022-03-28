import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import json
from fbprophet.plot import seasonality_plot_df

def set_floor_cap(df, growth):
    
    if growth['type'] == 'logistic':

        # Fix CAP

        if growth['cap_type'] == 'constante':

            df['cap'] = float(growth['cap'])

        elif growth['type'] == 'variable':

            max_cap = float(max(growth['cap']))
            min_cap = float(min(growth['cap']))

            df['cap'] = np.linspace(start=min_cap, stop=max_cap, num=df.shape[0])

        # Fix FLOOR

        if growth['floor_type'] == 'constante':

            df['floor'] = float(growth['floor'])

        elif growth['floor_type'] == 'variable':

            max_floor = float(max(growth['floor']))
            min_floor = float(min(growth['floor']))

            df['floor'] = np.linspace(start=min_floor, stop=max_floor, num=df.shape[0])

        df = df.astype({'cap': 'float64', 'floor': 'float64'})
        
    return df


def set_seasonalities(model, seasonalities_dict, fourier, prior):
    if seasonalities_dict['daily'] == True:
        model.add_seasonality(name='daily', period=1, fourier_order=fourier, prior_scale=prior)

    if seasonalities_dict['weekly'] == True:
        model.add_seasonality(name='weekly', period=7, fourier_order=fourier, prior_scale=prior)

    if seasonalities_dict['monthly'] == True:
        model.add_seasonality(name='monthly', period=30, fourier_order=fourier, prior_scale=prior)

    if seasonalities_dict['yearly'] == True:
        model.add_seasonality(name='yearly', period=365.25, fourier_order=fourier, prior_scale=prior)

    return model


def get_future_df(model, days, hourly):
    if hourly == 'off':
        future = model.make_future_dataframe(periods=days)

    if hourly == 'on':
        future = model.make_future_dataframe(periods=days * 32, freq='H')

        future = future[future['ds'].dt.hour > 7.5]
        future = future[future['ds'].dt.hour < 22]

    return future

def check_args(arguments):

    assert 0 < float(arguments["trend"]["interval"]) <= 1, "El porcentaje de datos empleados debe ser entre 0 y 1"
    assert float(arguments["trend"]["sensibility"]) > 0, "La sensibilidad de la tendencia debe ser mayor de 0"
    assert float(arguments["seasonality"]["fourier"]) > 0, "La sensibilidad de la periodicidad debe ser mayor de 0"
    assert float(arguments["seasonality"]["priorScale"]) > 0, "El intervalo de la periodicidad debe ser mayor de 0"
    assert float(arguments["duration"]) >= 0, "La duración del forecast no puede ser negativa"

    if arguments["growth"]["type"] == "logistic" and arguments["growth"]["cap_type"] == "constante" and arguments["growth"]["floor_type"] == "constante":
        assert float(arguments["growth"]["cap"]) > float(arguments["growth"]["floor"]), "El valor FLOOR ha de ser menor que CAP"
        
def get_seasonal_components(model, seasonality_flags, component_name, dates):
    
    component = {}
    periods={
        "daily": 1,
        "weekly": 7,
        "monthly": 30,
        "yearly": 365
    }
    
    assert component_name in ["daily", "monthly", "weekly", "yearly"], "El nombre de la componente no es correcto"
    
    if seasonality_flags[component_name]:
        
    	days = pd.date_range(start=dates.min(), end=dates.max(), periods=periods[component_name])
    	        
    	df_component = seasonality_plot_df(model, days)
    	seas = model.predict_seasonal_components(df_component)
    	
    	component = json.loads(seas[component_name].to_json())
    
    return component