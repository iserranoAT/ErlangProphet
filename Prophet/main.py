from forecast import forecast
import pandas as pd
import argparse
import json


def main(df_path: str, arguments: str, metric: str, output_name: str):

    dataframe = pd.read_csv(df_path, sep=';')
    with open(arguments) as json_file:
        arguments = json.load(json_file)

    forecast(dataframe, arguments, metric, output_name)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-df', type=str, help='Path to input data')
    parser.add_argument('-forecast_params', type=str, help='Path to params file to be used in the forecast')
    parser.add_argument('-metric', type=str, help='Used metric in the cross-validation', default="mse")
    parser.add_argument('-output_name', type=str, help='Path and name of output file')

    args = parser.parse_args()

    main(df_path = args.df,
         arguments = args.forecast_params,
         metric = args.metric,
         output_name = args.output_name)
