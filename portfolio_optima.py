import pandas as pd
import numpy as np

# Simulated Annealing Implementation
def simulated_annealing_portfolio(
        assets, expected_returns, covariance_matrix, 
        risk_free_rate=0, max_iter=1000, initial_temperature=100, 
        cooling_rate=0.99, max_allocation=0.5, min_allocation=0.0):
    num_assets = len(assets)
    current_portfolio = np.random.dirichlet(np.ones(num_assets))
    current_sharpe = calculate_sharpe(current_portfolio, expected_returns, covariance_matrix, risk_free_rate)
    best_portfolio = current_portfolio
    best_sharpe = current_sharpe
    temperature = initial_temperature

    for _ in range(max_iter):
        new_portfolio = make_move(current_portfolio, min_allocation, max_allocation)
        new_portfolio /= np.sum(new_portfolio)
        new_sharpe = calculate_sharpe(new_portfolio, expected_returns, covariance_matrix, risk_free_rate)
        if accept_move(current_sharpe, new_sharpe, temperature):
            current_portfolio = new_portfolio
            current_sharpe = new_sharpe
        if new_sharpe > best_sharpe:
            best_portfolio = new_portfolio
            best_sharpe = new_sharpe
        temperature *= cooling_rate

    return best_portfolio, best_sharpe

def calculate_sharpe(portfolio, expected_returns, covariance_matrix, risk_free_rate):
    portfolio_return = np.dot(portfolio, expected_returns)
    portfolio_risk = np.sqrt(np.dot(portfolio, np.dot(covariance_matrix, portfolio)))
    return (portfolio_return - risk_free_rate) / portfolio_risk

def make_move(portfolio, min_allocation, max_allocation):
    new_portfolio = portfolio + np.random.uniform(-0.01, 0.01, size=len(portfolio))
    return np.clip(new_portfolio, min_allocation, max_allocation)

def accept_move(current_sharpe, new_sharpe, temperature):
    if new_sharpe > current_sharpe:
        return True
    else:
        probability = np.exp((new_sharpe - current_sharpe) / temperature)
        return np.random.rand() < probability

if __name__ == "__main__":
    filename = "asset_data.csv"
    
    print(f"Wczytywanie danych z pliku: {filename}")
    data = pd.read_csv(filename, index_col=0, parse_dates=True)
    
    returns = data.pct_change().dropna()
    expected_returns = returns.mean() * 252  # Annualized
    covariance_matrix = returns.cov() * 252  # Annualized
    
    print("\nOczekiwane roczne zwroty:\n", expected_returns)
    print("\nMacierz kowariancji (roczna):\n", covariance_matrix)
    
    tickers = data.columns
    print("\nOptymalizacja portfela...")
    optimal_portfolio, optimal_sharpe = simulated_annealing_portfolio(
        assets=tickers,
        expected_returns=expected_returns.values,
        covariance_matrix=covariance_matrix.values,
        risk_free_rate=0.02,
        max_iter=1000,
        initial_temperature=100,
        cooling_rate=0.95,
        max_allocation=0.5
    )
    
    print("\nOptymalny portfel:")
    for ticker, allocation in zip(tickers, optimal_portfolio):
        print(f"{ticker}: {allocation:.2%}")
    print(f"\nOptymalny wskaźnik Sharpe'a: {optimal_sharpe:.4f}")