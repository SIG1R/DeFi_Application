import datetime as dt
import numpy as np

TODAY = dt.date.today()

def convertion_rate(actual_rate):

    return -1+(1+actual_rate)**(1/365)

def duration(expiration_date, FCB, daily_rate):

    # Getting the next expirations coupons of the bond
    dates = [dt.date(TODAY.year+i,expiration_date.month,expiration_date.day) for i in range(1+expiration_date.year - TODAY.year)]
    if dates[0] < TODAY: del dates[0]
    dates = np.array(dates)
    
    # Getting FCB
    fcb = [FCB] * (len(dates) -1)
    fcb.append(100+FCB)
    fcb = np.array(fcb)
    fcb_total = sum(fcb)

    # Getting VPFCB
    vpfcb = np.array([])
    for num, date in enumerate(dates):

        new_num = (1+daily_rate)**((expiration_date-TODAY).days)
        vpfcb = np.append(vpfcb, new_num)

    vpfcb = fcb/vpfcb

    return dates, fcb, vpfcb

