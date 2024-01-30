import datetime as dt
import numpy as np

TODAY = dt.date.today()

def convertion_rate(actual_rate):

    return -1+(1+actual_rate)**(1/365)

def duration_convexity(expiration_date, FCB, daily_rate):

    # Getting the next expirations coupons of the bond
    dates = [dt.date(TODAY.year+i,expiration_date.month,expiration_date.day) for i in range(1+expiration_date.year - TODAY.year)]
    if dates[0] < TODAY: del dates[0]
    
    # Getting FCB
    fcb = [FCB] * (len(dates) -1)
    fcb.append(100+FCB)
    fcb_total = sum(fcb)

    # Getting VPFCB
    vpfcb = []
    for num, date in enumerate(dates):

        new_num = fcb[num]/((1+daily_rate/100)**((date-TODAY).days))
        vpfcb.append(new_num)

    # Getting t*VPFCB
    t_vpfcb = []
    t_t_vpfcb = []
    for num, val in enumerate(vpfcb):
        t_vpfcb.append((num+1)*vpfcb[num])
        t_t_vpfcb.append((num+1)*(num+1)*vpfcb[num])

    duration = sum(t_vpfcb)/sum(vpfcb)
    convexity = sum(t_t_vpfcb)/sum(t_vpfcb)
    convexity = convexity/sum(vpfcb)

    return duration, convexity

def change_price_bond(duration, convexity, basic_points):
    
    calc = -duration*basic_points+(1/2)*convexity*(basic_points**2)
    return calc*100
