import matplotlib
matplotlib.use('Agg')

def check_args(arguments):

    assert 0 < float(arguments["trend"]["interval"]) <= 1, "El porcentaje de datos empleados debe ser entre 0 y 1"
    assert float(arguments["trend"]["sensibility"]) > 0, "La sensibilidad de la tendencia debe ser mayor de 0"
    assert float(arguments["seasonality"]["fourier"]) > 0, "La sensibilidad de la periodicidad debe ser mayor de 0"
    assert float(arguments["seasonality"]["priorScale"]) > 0, "El intervalo de la periodicidad debe ser mayor de 0"
    assert float(arguments["duration"]) >= 0, "La duración del forecast no puede ser negativa"

def check_cap_floor_args(arguments):

    if arguments["growth"]["type"] == "logistic":

        if arguments["growth"]["cap_type"] == "constante" and arguments["growth"]["floor_type"] == "constante":
            assert float(arguments["growth"]["cap"]) > float(arguments["growth"]["floor"]), "El valor FLOOR ha de ser menor que CAP"

        elif arguments["growth"]["cap_type"] == "variable" and arguments["growth"]["floor_type"] == "constante":
            assert float(arguments["growth"]["cap"]["max"]) > float(arguments["growth"]["cap"]["min"]), "El valor máximo de CAP ha de ser mayor que el mínimo"
            assert float(arguments["growth"]["cap"]["min"]) > float(arguments["growth"]["floor"]), "El valor máximo de CAP ha de ser mayor que el de FLOOR"

        elif arguments["growth"]["cap_type"] == "constante" and arguments["growth"]["floor_type"] == "variable":
            assert float(arguments["growth"]["cap"]) > float(arguments["growth"]["floor"]["max"]), "El valor de CAP ha de ser mayor que el máxmo de FLOOR"
            assert float(arguments["growth"]["floor"]["max"]) > float(arguments["growth"]["floor"]["min"]), "El valor máximo de FLOOR ha de ser mayor que el mínimo"

        else:
            assert float(arguments["growth"]["cap"]["max"]) > float(arguments["growth"]["cap"]["min"]), "El valor máximo de CAP ha de ser mayor que el mínimo"
            assert float(arguments["growth"]["floor"]["max"]) > float(arguments["growth"]["floor"]["min"]), "El valor máximo de FLOOR ha de ser mayor que el mínimo"
            assert float(arguments["growth"]["cap"]["min"]) > float(arguments["growth"]["floor"]["max"]), "El valor máximo de FLOOR ha de ser menor que el valor mínimo de CAP"

def check_regressors_df(df):

    assert "ds" in list(df), "El DataFrame de regressores no contiene la columna de fecha"

    return True
