import matplotlib
matplotlib.use('Agg')
import numpy as np

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
