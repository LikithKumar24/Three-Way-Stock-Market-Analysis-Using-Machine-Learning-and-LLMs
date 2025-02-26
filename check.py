import yfinance as yf
ticker = yf.Ticker("AAPL")
df = ticker.history(period="max")  # Fetches all available historical data
print(df.head())
