🔁 Pairs Trading Engine with Live Alerts

This project provides a full pipeline for pairs trading — including statistical testing, visualization, and real-time alerts via email when trade signals are triggered.

Developed in Python with support for live Alpaca data, this project includes tools to:

    Evaluate pair stationarity (ADF test)

    Monitor and compute rolling Z-scores

    Trigger live trade alerts via email

    Visualize spread and signal strength

    Customize and test pairs easily

📁 Project Structure
File	Description
live_alerts.py	Main live trading alert system (requires Alpaca API + .env)
pairs_utils.py	Helper functions: ADF test, Z-score, spread, signal detection
Pairs-Trading-Comparison.py	Offline analysis: fetch historical data, test pair stability, visualize spread/z-score
⚙️ Setup
1. Install Requirements

pip install pandas numpy yfinance statsmodels matplotlib python-dotenv alpaca-py

2. Create a .env File

You'll need to create a .env file in the same directory with the following content:

ALPACA_API_KEY=your_alpaca_api_key

ALPACA_SECRET_KEY=your_alpaca_secret_key

EMAIL_ADDRESS=youremail@gmail.com

EMAIL_PASSWORD=your_email_app_password

EMAIL_TO=destination_email@example.com

    Note: Use an App Password if you're using Gmail.

🚀 Running the Project
▶ Live Alerts

Run the live alerting system (with real-time Alpaca price feed):

python3 live_alerts.py

You’ll receive an email when a Z-score threshold (default ±2.0) is crossed for your configured pair.
📊 Offline Pair Testing

Edit the following variables in Pairs-Trading-Comparison.py:

ticker1 = "TICKER SYMBOL 1"

ticker2 = "TICKER SYMBOL 2"

start_date = "YYYY-MM-DD"

end_date = "YYYY-MM-DD"

Then run:

python3 Pairs-Trading-Comparison.py

This will:

    Fetch data from Yahoo Finance

    Compute spread and Z-score

    Run an Augmented Dickey-Fuller test

    Plot results

📈 Strategy Summary

    Log Returns: Used to normalize price data.

    ADF Test: Determines if the spread is stationary (requirement for mean-reversion).

    Z-Score: Signals when price divergence becomes statistically significant.

        Z > 2 → SHORT the spread

        Z < -2 → LONG the spread

📚 About

Built as a self-directed project to explore quantitative trading, statistical arbitrage, and real-time financial data processing.
