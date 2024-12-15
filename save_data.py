import yfinance as yf
import pandas as pd
from datetime import datetime
import ccxt

def fetch_stock_data(tickers, start_date, end_date):
    print(f"Pobieranie danych dla akcji: {tickers}...")
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

def fetch_bond_data(tickers, start_date, end_date):
    # W przykładzie obligacje są reprezentowane przez ETF-y na obligacje.
    print(f"Pobieranie danych dla obligacji (ETF): {tickers}...")
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

def fetch_commodity_data(tickers, start_date, end_date):
    # Surowce są reprezentowane przez ETF-y lub indeksy surowcowe dostępne w Yahoo Finance.
    print(f"Pobieranie danych dla surowców: {tickers}...")
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

# def fetch_crypto_data_ccxt(crypto_tickers, start_date, end_date):
#     """
#     Pobiera dane o kryptowalutach z giełdy przy użyciu ccxt
#     """
#     print(f"Pobieranie danych dla kryptowalut: {crypto_tickers}...")


def fetch_data(tickers_by_category, start_date, end_date, filename="asset_data.csv"):
    all_data = []
    for category, tickers in tickers_by_category.items():
        if category == "stocks":
            data = fetch_stock_data(tickers, start_date, end_date)
        elif category == "bonds":
            data = fetch_bond_data(tickers, start_date, end_date)
        elif category == "commodities":
            data = fetch_commodity_data(tickers, start_date, end_date)
        # elif category == "cryptocurrencies":
        #     data = fetch_crypto_data_ccxt(tickers, start_date, end_date)
        else:
            print(f"Nieobsługiwana kategoria: {category}")
            continue
        all_data.append(data)

    # Scal wszystkie dane w jeden DataFrame
    combined_data = pd.concat(all_data, axis=1)
    combined_data.to_csv(filename)
    print(f"Dane zapisane w pliku: {filename}")

# Definicja instrumentów finansowych do pobrania
tickers_by_category = {
    "stocks": ["AAPL", "MSFT", "GOOGL"],  # Akcje
    "bonds": ["IEF", "TLT", "SHY"],  # ETF-y obligacyjne
    "commodities": ["GLD", "SLV", "USO"],  # ETF-y na surowce (złoto, srebro, ropa)
    "cryptocurrencies": ["bitcoin", "ethereum", "litecoin"],  # Kryptowaluty (nazwa z CoinGecko)
}

# Daty do pobrania
start_date = "2023-01-01"
end_date = "2023-12-31"

# Pobranie danych
fetch_data(tickers_by_category, start_date, end_date, filename="diversified_asset_data.csv")