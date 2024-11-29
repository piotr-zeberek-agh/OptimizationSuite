import yfinance as yf

def fetch_and_save_data(tickers, start_date, end_date, filename="asset_data.csv"):
    print(f"Pobieranie danych dla {tickers} od {start_date} do {end_date}...")
    
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    
    data.to_csv(filename)
    print(f"Dane zapisane w pliku: {filename}")

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "SPY", "BABA"]
    start_date = "2022-01-01"
    end_date = "2024-10-31"
    filename = "asset_data.csv"
    
    fetch_and_save_data(tickers, start_date, end_date, filename)

# AAPL - Apple Inc.
# MSFT - Microsoft Corporation
# GOOGL - Alphabet Inc. (Google)
# AMZN - Amazon.com Inc.
# TSLA - Tesla Inc.
# META - Meta Platforms, Inc.
# NVDA - NVIDIA Corporation
# NFLX - Netflix Inc.
# SPY - SPDR S&P 500 ETF Trust (ETF, który śledzi indeks S&P 500)
# BABA - Alibaba Group Holding Limited