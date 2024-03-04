import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


class Stock:
    '''
    This Class storage basic information about a Stock in the market
    as ticker (symbol), name and 
    '''

    def __init__(self, symbol):
        '''
        Init the method Stock with the symbol (str type) of a stock.
        some examples are: GOOGL, NVDA, AMZN...
        '''
        assert type(symbol) == str, 'Check the type of the initializer argument'

        self.ticker = symbol
        self.history = None
        self.close = None
        self.returns = None
        self.cumulative_returns = None

    def get_data(self, start_date, end_date):
        self.history = yf.download(self.ticker, start=start_date, end=end_date)
        self.close = self.history['Close']


    def calculate_returns(self):
        # Calculate daily percentage returns
        self.returns = self.close.pct_change()

        # Calculate cumulative returns
        self.cumulative_returns = (1 + self.returns).cumprod()

    def trend_plot(self):
        '''
        This method was made for return the altair config by implement it
        in streamlit framework.
        '''

        chart = alt.Chart(self.cumulative_returns).mark_line(color='blue').encode(
                    x=alt.X('index:T', title='Fecha'),  # Utilizar 'index:T' para indicar que se trata de una fecha
                    y=alt.Y(self.cumulative_returns['Close'], title='Cambios en el precio del bono'),
                    # Agregar leyenda para la duración
                    color=alt.value('#1ce5cc'),
                    opacity=alt.value(0.8),
                    #legend=alt.Legend(title='Duración')
        )


        return chart

    def plot_cumulative_returns(self):
        # Plotting cumulative returns for each stock
        fig, ax = plt.subplots()
        for ticker in self.tickers:
            plt.plot(self.cumulative_returns.index, self.cumulative_returns[ticker], label=ticker)
        ax.set_title('Stock Cumulative Returns Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Returns')
        ax.legend()
        return  fig

    def plot_corr(self):
        fig, ax = plt.subplots()
        corr = self.cumulative_returns.corr('spearman')

        sns.heatmap(corr, annot=True)

        return fig
