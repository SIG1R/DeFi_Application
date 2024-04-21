# Numerical
import numpy as np
import datetime as dt
import pandas as pd
import yfinance as yf
import statsmodels.api as sm

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt




class Bond:

    def __init__(self, type_bond = 'Con Cupon',
                 issue_date = dt.date(2024,1,25), expiration_date = dt.date(2027,11,3),
                 face_rate = 5.75, market_value = 10.19):
        """
        Inicializador de la clase bonos, establece variables de instancia características
        de un bono las cuales son:
        - type_bond             establece el tipo de bono (con cupón o sin cupón)
        - face_rate
        - market_value          indica la tasa de interés a la que se negocia el bono en la actualidad
        - issue_date            referencia la fecha en la cual el bono fue emitidio
        - expiration_date       referencia la fecha de vencimiento del bono
        """

        # Asegurarse de que las fechas no tengan problemas temporales
        assert issue_date <= expiration_date, 'La fecha de emisión del bono no puede ser mayor que la fecha de vencimiento'

        self.type_bond = type_bond # Tipo de bono (con o sin cupón)
        
        # Almacenar las variables de instancia sobre las tasas de interés del bono
        self.face_rate = face_rate
        self.market_value = market_value

        # Almacenar las variables de instancia sobre las fechas del bono
        self.issue_date = issue_date
        self.expiration_date = expiration_date
        
        # Instancias base
        self.total_payments = 0
        self.total_payments = 0
        self.payments_dates = np.array([])
        self.cash_flow = np.array([])
        self.present_cash_flow = np.array([])


        # Auto inicializar métodos
        self.get_payments_dates()
        self.get_daily_rate()
        self.get_cash_flow()
        self.build_dataframe()
        self.get_duration()
        self.get_convexity()


    def update(self):
        """
        Método que permite la actualización de un bono, es decir, al mínimo
        cambio en alguna variable de instacia sobre la instancia del bono
        se re-ejecutan los métodos asociados al bono y por ende, se
        re-asignan las variables de instancia
        """
        
        self.get_payments_dates()
        self.get_daily_rate()
        self.get_cash_flow()
        self.build_dataframe()
        self.get_duration()
        self.get_convexity()

    def get_payments_dates(self):
        """
        Método que cálcula las siguientes fechas de cobro del bono y lo almacena en una
        variable de instancia
        """

        TODAY_ = dt.date.today()

        if self.type_bond == 'Zero Cupon':
            self.payments_dates = np.array([self.expiration_date]) # Se almacenan las fechas en una variable de instancia
        else:

            payments_dates = [
                    dt.date(self.issue_date.year+i,self.expiration_date.month,self.expiration_date.day) # Las fechas de cobro son anuales
                    for i in range(1+self.expiration_date.year - self.issue_date.year) # Se obtienen la cantidad de años de diferencia y se le suma 1 
                    ]                                                         # para que el año de vencimiento se incluya en el ciclo for

            payments_dates = [date for date in payments_dates if date > TODAY_] # Se elimina la primera fecha en caso de que ya se haya reclamado el cupón

            self.payments_dates = payments_dates # Se almacenan las fechas en una variable de instancia
        self.total_payments = len(self.payments_dates)


    def get_daily_rate(self):
        """
        Método que permite la conversión de tasas de interés del bono anual a diario
        """

        daily_fract = 1/365                         # Razón sobre la que se efectuará el cambio (diario)
        r = (1+self.market_value/100)**daily_fract  # Se efectua la conversión de tasas
        r = 100*(r-1)                          # Convierte en valor porcentual
        r = round(r, 3)                        # Se redondea la tasa a tres decimales
        self.daily_rate = r                        # Se almacena en una variable de instancia

    def get_cash_flow(self):
        """
        Método que cálcula el flujo de caja del bono
        """
        
        if self.type_bond == 'Zero Cupon':
            self.cash_flow = np.array([self.face_rate+100])

        else:

           # ----- Getting cash flow -----
            cash_flow = self.face_rate * np.ones(len(self.payments_dates)-1)
            self.cash_flow = np.append(cash_flow, self.face_rate + 100)

        # ----- Getting cash flow in present value -----
        present_cash_flow = np.array([])
        base = 1+self.daily_rate/100
        for index,element in enumerate(self.cash_flow):
            aux_ = base**((self.payments_dates[index] - self.issue_date).days)
            aux_ = self.cash_flow[index]/aux_
            present_cash_flow = np.append(present_cash_flow, round(aux_,3))

        self.present_cash_flow = present_cash_flow

    
    def get_valuation(self):
        """
        Método que cálcula la valuación de un bono dependiendo del tipo de
        bono (con cupón o sin cupón)
        """

        power = (self.expiration_date - self.issue_date).days # Para cualquiera de los 2 tipos de bonos, la potencia de la fórmula es la mísma

        if self.type_bond == 'Zero Cupon': # Sí el bono es de tipo zero-coupon
            self.valuation = np.e**(-self.daily_rate/100*power)

        else: # Sí el bono es de tipo con cupón
            rate = self.market_value/100
            basic_form = 1+rate**power           
            left = self.face_rate*(basic_form -1)/(basic_form*rate)
            right = 100/basic_form

            self.valuation = left + right

    def get_duration(self):

        self.duration = sum(self.dataframe['N° pago * Valor presente FC'])/sum(self.dataframe['Valor presente FC'])

    def get_convexity(self):
        aux = sum(self.dataframe['N° pago^2 * Valor presente FC'])/sum(self.dataframe['N° pago * Valor presente FC'])

        self.convexity = round(aux/sum(self.cash_flow),3)


    def change_price(self, basic_points):
        
        self.generic_convexity = -self.duration*basic_points + 0.5*self.convexity*basic_points**2    
        self.generic_duration = -self.duration*basic_points






    def build_dataframe(self):
        '''
        Método que construye el DataFrame de flujo de caja
        '''

        self.index = np.array([i for i  in range(1,self.total_payments+1)])
    
        self.dataframe = pd.DataFrame({
            'Fecha': self.payments_dates,
            'FC': self.cash_flow,
            'Valor presente FC': self.present_cash_flow
        }, index=self.index)

        self.dataframe['N° pago * Valor presente FC'] =  self.index*self.dataframe['Valor presente FC']

        self.dataframe['N° pago^2 * Valor presente FC'] =  self.index**2*self.dataframe['Valor presente FC']





class Found:
    
    def __init__(self, found_name:str, index_market:str):
        '''
        Initialize a Found instance with the basic information about a found

        Arguments:
            - found_name: Is the name of you found to analize
            - index_market: Is the index of the market that you want analize
        '''

        self.found_name = found_name
        self.index_market = index_market

    def get_data(self, start_date, end_date):
        '''
        This method enables download the historical data of the found
        and the index market, both in the same interval dates.
        '''

        # Download found historical data
        self.found_data = yf.download(
                self.found_name,
                start = start_date,
                end = end_date
        )

        # Download index market historical data
        self.market_data = yf.download(
                self.index_market,
                start = start_date,
                end = end_date
        )
        
    def calculate_returns(self):
        '''
        This method compute the cumulative returns of your found and market.
        '''

        # Percentaje daily change
        self.found_returns = self.found_data['Close'].pct_change()
        self.market_returns =  self.market_data['Close'].pct_change()

        # Cumulative returns
        self.found_cum_returns = (1 + self.found_returns).cumprod().reset_index()
        self.market_cum_returns = (1 + self.market_returns).cumprod().reset_index()

    def capm(self, Rate_free, Rate_actual):
        '''
        Compute the beta and Jensen' alpha.
        '''

        # Computing beta
        covariance = self.found_returns.cov(self.market_returns)
        variance = self.market_returns.var()

        self.beta = covariance/variance

        # Computing Jensen's alpha
        self.alpha = Rate_actual - Rate_free + self.beta*(self.market_returns.mean() - Rate_free)

















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
        self.cumulative_returns = (1 + self.returns).cumprod().reset_index()

    def trend_plot(self):
        '''
        This method was made for return the altair config by implement it
        in streamlit framework.
        '''

        chart = alt.Chart(self.cumulative_returns).mark_line(color='blue').encode(
                    x=alt.X('Date', title='Fecha'),  # Utilizar 'index:T' para indicar que se trata de una fecha
                    y=alt.Y('Close', title='Cambios en el precio del bono'),
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




class Option:

    def __init__(self,                      # Auto reference
                 spot, strike,              # Prices
                 expiration, interval,      # Time of the options
                 volatility, risk_free):    # Extras
        '''
        This function create a instance about a option instrument.
        '''

        # Saving variables instances
        self.spot          = spot
        self.strike        = strike
        self.expiration    = expiration
        self.interval      = interval
        self.volatility    = volatility
        self.risk_free     = risk_free

        # >>> Converting the risk_free <<<
        if (self.interval == 'Semana'):
            self.risk_free = (1 + self.risk_free/100)**(1/52)-1
            self.risk_free *= 100





    @staticmethod
    def pay_off(type_option:str, price:float, strike:float):
        '''
        Compute and return the pay-off of your option depending
        of call or put type option.

        ¡Remember the equation!
        - V(S,t) = max{S - strike_price, 0} -> Call type option
        - V(S,t) = max{strike_price - S, 0} -> Put type option
        '''

        if type_option == 'Call':
            # max{S-K, 0}
            return max(price - strike, 0)

        # If type_option is Put
        # max{K-S, 0}
        return max(strike - price, 0)

    def compute_UD(self):
        '''
        Return D, U changes in the price:

        U = e^(σ*√t)
        D = e^(-σ*√t) = 1/U
        '''

        # Computation the exponential part (σ*√t)
        exponent = self.volatility

        if (self.interval == 'Semana'):
            exponent *= np.sqrt(5)

        elif (self.interval == 'Mes'):
            exponent *= np.sqrt(20)

        elif (self.interval == 'Año'):
            exponent *= np.sqrt(250)

        self.U = np.exp(exponent)
        self.D = 1/self.U

    def convert_rate(self):


        if (self.expiration == 0):
            pass

        if (self.interval == 'Semana'):
            self.new_rate = (1 + self.risk_free)**(1/52)-1
        
        elif (self.interval == 'Mes'):
            self.new_rate = (1 + self.risk_free)**(1/52)-1



    def compute_risk_neutral(self):
        '''
        Compute the risk neutral probability
        '''
        
        # Compute the risk neuetral probability
        numerator = (1 + self.risk_free) - self.D
        denominator = self.U - self.D

        self.risk_neutral = numerator/denominator
