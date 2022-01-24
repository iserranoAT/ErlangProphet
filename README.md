# ErlangAnalytics_Prophet

This project is intended to be a python API to create forecasts using Prophet library from Facebook. You can easily create forecast by setting the parameters at `main.py` and executing the script afterwards. The parameters are:

- df (python str): Path to input data.
- forecast_params (python Dict): parameters to use in the forecast.
- metric (python str): Used metric in the cross-validation. Must use one os the following:
    - "mse": mean squared error
    - "rmse": root mean squared error
    - "mae": mean absolute error
    - "mape": mean absolute percent error
    - "mdape": median absolute percent error
    - "smape": symmetric mean absolute percentage error
    - "coverage": coverage of the upper and lower intervals
- output_name (python str): Path to output data without extension.

The following command is an example of forecast using "mse" metric. Take into account that you need to change the {PATH_TO_PROJECT} by the real path in your computer:

```
 python .\main.py -df "./data/input/births.csv" -forecast_params "./data/input/variables.json" -metric "mse" -output_name "{PATH_TO_PROJECT}/data/outputs/births_forecast"
```
