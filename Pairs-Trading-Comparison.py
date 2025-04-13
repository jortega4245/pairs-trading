# Pairs Trading Data Analysis

import pandas as pd
import numpy as np
import yfinance as yf
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

# -----------------------------
# Ticker Settings
ticker1 = ''
ticker2 = ''
start_date = ''
end_date = ''
# -----------------------------

def download_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end)
    close = df['Close']
    if isinstance(close, pd.DataFrame):
        close = close[ticker]
    return close

def calculate_log_returns(price_series):
    if isinstance(price_series, pd.DataFrame):
        price_series = price_series.iloc[:, 0]
    returns = np.log(price_series / price_series.shift(1)).dropna()
    returns.index = returns.index.tz_localize(None)  # strip timezone if any
    return returns

def calculate_spread_and_zscore(returns1, returns2):
    aligned1, aligned2 = returns1.align(returns2, join='inner')
    spread = aligned1 - aligned2
    mean = spread.mean()
    std = spread.std()
    zscore = (spread - mean) / std
    return spread, zscore

def plot_spread_and_zscore(spread, zscore, ticker1, ticker2):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

    # Spread plot
    ax1.plot(spread, label=f'Spread ({ticker1} - {ticker2})')
    ax1.axhline(spread.mean(), color='red', linestyle='--', label='Mean')
    ax1.set_title(f'Spread between {ticker1} and {ticker2}')
    ax1.set_ylabel("Log Return Spread")
    ax1.legend()
    ax1.grid(True)

    # Z-score plot
    ax2.plot(zscore, label='Z-score', color='purple')
    ax2.axhline(0, color='black', linestyle='--')
    ax2.axhline(1, color='green', linestyle='--', label='Z = ±1')
    ax2.axhline(-1, color='green', linestyle='--')
    ax2.axhline(2, color='orange', linestyle='--', label='Z = ±2')
    ax2.axhline(-2, color='orange', linestyle='--')
    ax2.set_title("Z-Score of Spread")
    ax2.set_ylabel("Z-Score")
    ax2.legend()
    ax2.grid(True)

    plt.xlabel("Date")
    plt.tight_layout()
    plt.show()

# Step 1: Download prices
close1 = download_data(ticker1, start_date, end_date)
close2 = download_data(ticker2, start_date, end_date)

# Step 2: Calculate log returns
returns1 = calculate_log_returns(close1)
returns2 = calculate_log_returns(close2)

# Step 3: Calculate spread and z-score
spread, zscore = calculate_spread_and_zscore(returns1, returns2)

# Step 4: ADF Test
if not spread.empty:
    adf_result = adfuller(spread)
    print(f"\nADF Statistic: {adf_result[0]}")
    print(f"p-value: {adf_result[1]}")

    if adf_result[1] < 0.05:
        print("The spread is stationary and suitable for pairs trading.")
    else:
        print("The spread is not stationary.")

# Step 5: Plot
plot_spread_and_zscore(spread, zscore, ticker1, ticker2)
