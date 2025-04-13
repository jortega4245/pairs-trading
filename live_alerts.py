# Stock Alerts In Real Time via Email

import os
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from alpaca.data.live import StockDataStream
from dotenv import load_dotenv
from pairs_utils import calculate_spread_and_zscore, detect_zscore_signal
import pandas as pd

# Load API keys and email credentials from .env
load_dotenv()
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

ticker1 = "V"
ticker2 = "MA"
window = 60  # Rolling window of 60 prices
price_data = {
    ticker1: [],
    ticker2: []
}

# Send email alert
def send_email_alert(subject, message):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Email alert sent!")
    except Exception as e:
        print("Failed to send email:", e)

# Main handler for incoming price updates
async def handle_data(data):
    symbol = data.symbol
    price = float(data.price)

    # Add price to rolling list
    if symbol in price_data:
        price_data[symbol].append(price)
        if len(price_data[symbol]) > window:
            price_data[symbol].pop(0)

    # Only calculate if we have enough data
    if all(len(price_data[t]) >= window for t in price_data):
        series1 = pd.Series(price_data[ticker1])
        series2 = pd.Series(price_data[ticker2])
        spread, zscore = calculate_spread_and_zscore(series1, series2)
        signal = detect_zscore_signal(zscore)

        latest_price1 = series1.iloc[-1]
        latest_price2 = series2.iloc[-1]
        latest_spread = spread.iloc[-1]
        latest_zscore = zscore.iloc[-1]

        print(f"Latest Z-score: {latest_zscore:.2f} | Signal: {signal}")

        if signal in ["long", "short"]:
            message = (
                f"Z-score alert for {ticker1}/{ticker2}: {signal.upper()}\n"
                f"Z-score: {latest_zscore:.2f}\n"
                f"{ticker1} Price: ${latest_price1:.2f}\n"
                f"{ticker2} Price: ${latest_price2:.2f}\n"
                f"Price Divergence: ${latest_spread:.2f}"
            )
            send_email_alert("Pairs Trading Alert", message)

# Connect to Alpaca real-time stream
def start_stream():
    stream = StockDataStream(ALPACA_API_KEY, ALPACA_SECRET_KEY)
    stream.subscribe_trades(handle_data, ticker1, ticker2)
    stream.run()

if __name__ == "__main__":
    send_email_alert("Test Alert", "Email alert system is working!")