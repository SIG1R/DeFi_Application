import yfinance as yf


class Stock:


    def __init__(self, symbol=None, company=None):
        '''

        '''
        self.symbol = symbol
        self.company = company
        self.ticker = yf.Ticker(symbol)

    def closing_prices(self):
        self.close = self.history['Close']

    def get_history(self, start_date, end_date):
        self.history = yf.download(self.symbol, start=start_date, end=end_date)

    def calculate_returns(self):
        # Calculate daily percentage returns
        self.returns = self.close.pct_change()

    def calculate_cumulative_returns(self):
        # Calculate cumulative returns
        self.cumulative_returns = (1 + self.returns).cumprod()

    def plot_cumulative_returns(self):
        # Plotting cumulative returns for each stock
        plt.figure(figsize=(14, 7))
        for ticker in self.tickers:
            plt.plot(self.cumulative_returns.index, self.cumulative_returns[ticker], label=ticker)
        plt.title('Stock Cumulative Returns Over Time')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
        plt.show()
