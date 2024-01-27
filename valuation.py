import numpy as np

def zero_coupon(rate, time, duration):
    """
    rate -> tasa de interés (r)
    time -> tiempo que ha pasado
    total_duration -> tiempo de duración del bono
    """

    time_diff = duration - time

    return np.e**(-rate*time_diff)



