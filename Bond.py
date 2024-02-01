import numpy as np

class Bond:

    def __init__(self, type_bond,
                 date_issue, date_expiration,
                 face_value,market_value):
        
        self.type_bond = type_bond # Tipo de bono (con o sin cupón)
        
        # Valores o tasas de interés del bono
        self.face_value = face_value        # Cuando fue emitido
        self.market_value = market_value    # Cuando se toma la medición
        self.daily_value = 0                # Conversión a tasa diaria

        # Fechas correspondientes a
        self.date_issue = date_issue            # Cuando fue emitido
        self.date_expiration = date_expiration  # Cuando vence
    
    def daily_rate(self):
        
        daily_fract = 1/365
        result = (1+self.market_value)**daily_fract
        result = 100*(result-1)
        result = round(result, 3)
        self.daily_value = result

    def valuation(self, zero_coupon = True):
        
        power = (self.date_expiration - self.date_issue).days

        if zero_coupon: # Sí el bono es de tipo Zero cupón
            return np.e**(-self.daily_value*power)
        else: # Sí el bono es de tipo con cupón
            pass

    def duration(self):
        pass

    def convexity(self):
        pass

    def change_price(self):
        pass
