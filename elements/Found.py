import yfinance as yf
import numpy as np
import pandas as pd
import statsmodels.api as sm
from .Bond import *


class Found(Bond):
    
    def __init__(self, found, index):
        self.found = found
        self.index_market = index
        # Fetch historical data
        asset_data = yf.download(self.found, start="2019-01-01", end="2024-01-01")
        market_index_data = yf.download(self.index_market, start="2019-01-01", end="2024-01-01")

        # Calculate returns
        asset_returns = asset_data['Adj Close'].pct_change().dropna()
        market_returns = market_index_data['Adj Close'].pct_change().dropna()

        # Add a constant to the independent variable (market returns)
        X = sm.add_constant(market_returns)

        # Fit the regression model
        model = sm.OLS(asset_returns, X)
        results = model.fit()

        # Extract beta (slope coefficient) from the regression results
        self.beta = results.params[1]
