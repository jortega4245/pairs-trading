import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

def calculate_log_returns(price_series: pd.Series) -> pd.Series:
    if isinstance(price_series, pd.DataFrame):
        price_series = price_series.iloc[:, 0]
    returns = np.log(price_series / price_series.shift(1)).dropna()
    returns.index = returns.index.tz_localize(None)
    return returns

def calculate_spread_and_zscore(series1: pd.Series, series2: pd.Series):
    aligned1, aligned2 = series1.align(series2, join='inner')
    spread = aligned1 - aligned2
    mean = spread.mean()
    std = spread.std()
    zscore = (spread - mean) / std
    return spread, zscore

def adf_test(series: pd.Series):
    result = adfuller(series)
    return {
        'adf_stat': result[0],
        'p_value': result[1],
        'critical_values': result[4],
        'stationary': result[1] < 0.05
    }

def detect_zscore_signal(zscore_series: pd.Series, upper_thresh=2.0, lower_thresh=-2.0):
    latest_z = zscore_series.iloc[-1]
    if latest_z > upper_thresh:
        return 'short'
    elif latest_z < lower_thresh:
        return 'long'
    else:
        return 'neutral'