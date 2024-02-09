import numpy as np
import datetime as dt
import pandas as pd

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
