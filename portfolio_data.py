import yfinance as yf
import pandas as pd

def fetch_data(tickers_by_category, start_date, end_date):
    all_data = []
    for category, tickers in tickers_by_category.items():
        if category == "Stocks":
            data = fetch_stock_data(tickers, start_date, end_date)
        elif category == "Bonds":
            data = fetch_bond_data(tickers, start_date, end_date)
        elif category == "Commodities":
            data = fetch_commodity_data(tickers, start_date, end_date)
        elif category == "ETFs":
            data = fetch_etf_data(tickers, start_date, end_date)
        elif category == "Currencies":
            data = fetch_currency_data(tickers, start_date, end_date)
        elif category == "Indexes":
            data = fetch_index_data(tickers, start_date, end_date)
        else:
            # print(f"No data fetcher for category: {category}")
            continue
        all_data.append(data)

    combined_data = pd.concat(all_data, axis=1)
    return combined_data


def fetch_stock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

def fetch_bond_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data

def fetch_commodity_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    return data



def fetch_etf_data(tickers, start_date, end_date):
    pass

def fetch_currency_data(tickers, start_date, end_date):
    pass

def fetch_index_data(tickers, start_date, end_date):
    pass