import numpy as np
import datetime as dt

def zero_coupon(rate, expiration_date, issue_date = dt.date.today()):
    """
    rate -> tasa de interés (r)
    time -> tiempo que ha pasado
    total_duration -> tiempo de duración del bono
    """
    assert issue_date <= expiration_date, 'La duración del bono no puede ser menor que el tiempo transcurrido'

    time_diff = expiration_date - issue_date

    return np.e**(-rate*time_diff.days)




