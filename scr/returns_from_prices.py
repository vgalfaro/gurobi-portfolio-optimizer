import pandas as pd

TRADING_DAYS = 252

data = pd.read_csv('close-values-1mo.csv', index_col=0, parse_dates=True)
returns = data.pct_change().dropna()

# annualized mu and sigma
mu: pd.Series= returns.mean() * TRADING_DAYS
sigma: pd.DataFrame = returns.cov() * TRADING_DAYS