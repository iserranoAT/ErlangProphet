import matplotlib
matplotlib.use('Agg')
import pandas as pd

def add_regressor_to_future(future, regressors_df):
    """
    adds extra regressors to a `future` DataFrame dataframe created by fbprophet
    Parameters
    ----------
    data : pandas.DataFrame
        A `future` DataFrame created by the fbprophet `make_future` method

    regressors_df: pandas.DataFrame
        The pandas.DataFrame containing the regressors (with a datetime index)
    Returns
    -------
    futures : pandas.DataFrame
        The `future` DataFrame with the regressors added
    """

    futures = future.copy()

    futures.index = pd.to_datetime(futures.ds)

    if isinstance(regressors_df, list):
        regressors = pd.concat(regressors_df, axis=1)
    else:
        regressors=regressors_df

    futures = futures.merge(regressors, left_index=True, right_index=True)

    futures = futures.reset_index(drop=True)

    return futures

def setup_regressors(df, df_regressors):

    df_regressors['ds'] = pd.to_datetime(df_regressors["ds"]).dt.date
    df_regressors = df_regressors[(df_regressors['ds'] >= min(df["ds"])) & (df_regressors['ds'] <= max(df["ds"]))]

    return df, df_regressors

def setup_prior_rgs(df_in, df_rgs, model):

    df, df_rgs_prior = setup_regressors(df_in, df_rgs)

    for regressor in list(df_rgs_prior):
        if regressor != "ds":
            df[regressor] = df_rgs_prior[regressor]
            model.add_regressor(regressor)

    return df_in, df_rgs_prior, model

def setup_posterior_rgs(df_in, df_rgs):

    df_rgs = df_rgs[(df_rgs['ds'] >= min(df_in["ds"])) & (df_rgs['ds'] <= max(df_in["ds"]))]

    for regressor in list(df_rgs):
        if regressor != "ds":
            df_in[regressor] = df_rgs[regressor]

    return df_in