import yfinance as yf
import pandas as pd

def fetch_and_save_data(tickers, start_date, end_date, filename="asset_data.csv"):
    """
    Pobiera dane historyczne dla podanych aktywów i zapisuje je do pliku CSV.
    
    Parameters:
    - tickers: Lista symboli aktywów (np. ["AAPL", "MSFT"]).
    - start_date: Data początkowa w formacie "YYYY-MM-DD".
    - end_date: Data końcowa w formacie "YYYY-MM-DD".
    - filename: Nazwa pliku wyjściowego (domyślnie "asset_data.csv").
    """
    print(f"Pobieranie danych dla {tickers} od {start_date} do {end_date}...")
    
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    
    data.to_csv(filename)
    print(f"Dane zapisane w pliku: {filename}")

if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    start_date = "2022-01-01"
    end_date = "2024-10-31"
    filename = "asset_data.csv"
    
    fetch_and_save_data(tickers, start_date, end_date, filename)