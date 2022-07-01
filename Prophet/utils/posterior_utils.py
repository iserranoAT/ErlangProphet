import matplotlib
matplotlib.use('Agg')
import pandas as pd
import json
from fbprophet.plot import seasonality_plot_df

def get_future_df(model, days, hourly):
    if hourly == 'off':
        future = model.make_future_dataframe(periods=days)

    if hourly == 'on':
        future = model.make_future_dataframe(periods=days * 32, freq='H')

        future = future[future['ds'].dt.hour > 7.5]
        future = future[future['ds'].dt.hour < 22]

    return future


def get_seasonal_components(model, seasonality_flags, component_name, dates):
    component = {}
    periods = {
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