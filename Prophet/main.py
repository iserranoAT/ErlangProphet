from forecast import forecast
import pandas as pd
import argparse
import json


def main(df_path: str, df_regressors_path: str, arguments: str, metric: str, output_name: str):

    dataframe = pd.read_csv(df_path, sep=',')
    dataframe_rgs = pd.read_csv(df_regressors_path, sep=',')

    with open(arguments) as json_file:
        arguments = json.load(json_file)

    forecast(dataframe, dataframe_rgs, arguments, metric, output_name)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-df_path', type=str, help='Path to input data')
    parser.add_argument('-df_regressors_path', type=str, help='Path to input regressors data')
    parser.add_argument('-arguments', type=str, help='Path to params file to be used in the forecast')
    parser.add_argument('-metric', type=str, help='Used metric in the cross-validation', default="mse")
    parser.add_argument('-output_name', type=str, help='Path and name of output file')

    args = parser.parse_args()

    main(df_path = "C:/Users/iserrano/Documents/Proyectos/AT/ErlangProphet/Prophet/data/input/temperatures.csv",
         df_regressors_path = "C:/Users/iserrano/Documents/Proyectos/AT/ErlangProphet/Prophet/data/input/temperatures_rgs.csv",
         arguments = "C:/Users/iserrano/Documents/Proyectos/AT/ErlangProphet/Prophet/data/input/input_args.json",
         metric = "mse",
         output_name = "C:/Users/iserrano/Documents/Proyectos/AT/ErlangProphet/Prophet/data/output/regressors/")

    '''
    main(df_path = args.df,
         arguments = args.forecast_params,
         metric = args.metric,
         output_name = args.output_name)
    '''
