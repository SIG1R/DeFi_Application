import numpy as np
import datetime as dt

class Bond:

    def __init__(self, type_bond,
                 date_issue, date_expiration,
                 face_value,market_value):
        
        assert date_issue < date_expiration, 'La fecha de emisión del bono no puede ser mayor que la fecha de vencimiento'

        self.type_bond = type_bond # Tipo de bono (con o sin cupón)
        
        # Valores o tasas de interés del bono
        self.face_value = face_value        # Cuando fue emitido
        self.market_value = market_value    # Cuando se toma la medición
        self.daily_value = 0                # Conversión a tasa diaria

        # Fechas correspondientes a
        self.date_issue = date_issue            # Cuando fue emitido
        self.date_expiration = date_expiration  # Cuando vence

        self.valuation_now = 0
    
    def get_coupon_dates(self):
        TODAY = dt.date.today()
        dates = [dt.date(TODAY.year+i,self.date_expiration.month,self.date_expiration.day) for i in range(1+self.date_expiration.year - TODAY.year)]
        if dates[0] < TODAY: del dates[0]
        self.coupon_dates = dates


    def daily_rate(self):
        """
        Convierte una tasa de interés anual en diaria
        """
        daily_fract = 1/365
        result = (1+self.market_value/100)**daily_fract
        result = 100*(result-1)
        result = round(result, 3)
        self.daily_value = result

    def cash_flow(self):
        flow = self.face_value * np.ones(len(self.coupon_dates)-1)
        self.cash_flow_ = np.append(flow, self.face_value + 100)
    
    def valuation(self):
        
        power = (self.date_expiration - self.date_issue).days

        if self.type_bond == 'Zero Cupon': # Sí el bono es de tipo zero-coupon
            self.valuation_now = np.e**(-self.daily_value/100*power)

        else: # Sí el bono es de tipo con cupón
            rate = self.market_value/100
            basic_form = 1+rate**((self.date_expiration - self.date_issue).days)
            
            left = self.face_value*(basic_form -1)/(basic_form*rate)
            right = 100/basic_form

            self.valuation_now = left + right

    def duration(self):
        pass

    def convexity(self):
        pass

    def change_price(self):
        pass
