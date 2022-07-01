import matplotlib
matplotlib.use('Agg')

def check_args(arguments):

    assert 0 < float(arguments["trend"]["interval"]) <= 1, "El porcentaje de datos empleados debe ser entre 0 y 1"
    assert float(arguments["trend"]["sensibility"]) > 0, "La sensibilidad de la tendencia debe ser mayor de 0"
    assert float(arguments["seasonality"]["fourier"]) > 0, "La sensibilidad de la periodicidad debe ser mayor de 0"
    assert float(arguments["seasonality"]["priorScale"]) > 0, "El intervalo de la periodicidad debe ser mayor de 0"
    assert float(arguments["duration"]) >= 0, "La duración del forecast no puede ser negativa"

    if arguments["growth"]["type"] == "logistic" and arguments["growth"]["cap_type"] == "constante" and \
            arguments["growth"]["floor_type"] == "constante":
        assert float(arguments["growth"]["cap"]) > float(
            arguments["growth"]["floor"]), "El valor FLOOR ha de ser menor que CAP"

def check_regressors_df(df):

    assert "ds" in list(df), "El DataFrame de regressores no contiene la columna de fecha"

    return True
