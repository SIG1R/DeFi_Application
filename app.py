import streamlit as st
from Bond import *
import pandas as pd

#import numpy as np
#import matplotlib.pyplot as plt

st.write("""
# Bond calculator
Establecer características del bono
""")

# Setting type of bond
type_bond = st.selectbox(
    'Tipo de bono',
    ('Zero Cupon', 'Con Cupon')
)


# Setting dates about the bond
ISSUE_DATE, EXPIRATION_DATE = st.columns(2)

with ISSUE_DATE: # Set issue_date input
    date_issue = st.date_input(
            'Fecha de emisión',
            format='DD/MM/YYYY',
            value=dt.date(2024,1,25)
    )

with EXPIRATION_DATE: # Set expiration_date input
    date_expiration= st.date_input(
            'Fecha de vencimiento',
            format='DD/MM/YYYY',
            value=dt.date(2027,11,3)
    )


# Setting rates about the bond
RATE_ISSUE_COLUMN, RATE_MARKET_COLUMN = st.columns(2)

with RATE_ISSUE_COLUMN: # Set issue_rate input
    face_value = st.number_input('Tasa facial (%)', value=5.75)

with RATE_MARKET_COLUMN: # Set actual_date input
    market_value = st.number_input('Tasa de mercado (%)', value=10.19)

bond = Bond(
        type_bond,
        date_issue, date_expiration,
        face_value, market_value)

st.write(f'El cupón es de tipo {bond.type_bond}')
st.write(f'El cupón es fue emitido en la fehca {bond.date_issue}')
st.write(f'El cupón se vence en la fehca {bond.date_expiration}')
st.write(f'El cupón tiene una tasa facial de {bond.face_value}')
st.write(f'El cupón tiene una tasa anual en el mercado de {bond.market_value}')
bond.daily_rate()
st.write(f'El cupón tiene una tasa diaria en el mercado de {bond.daily_value}')
bond.valuation()
st.write(f'El bono está valorado en {bond.valuation_now}')

bond.get_coupon_dates()
bond.cash_flow()

data_example = pd.DataFrame({
    'Fecha': bond.coupon_dates,
    'FCB': bond.cash_flow_
})


st.write(data_example)



#basic_points = st.number_input('Puntos básicos (%)') / 100

#st.write(type(fecha_fin))
#if st.button('calcular'):

    #st.write(val.zero_coupon(0.1, expiration_date, issue_date))
    #st.write(f'Siguientes cobros del cupón {sm.duration(expiration_date,0)}')
#    daily_rate = sm.convertion_rate(actual_rate)*100
    #st.write(f'{sm.duration_convexity(expiration_date, 5.75, daily_rate)}')
    
#    duration, convexity = sm.duration_convexity(expiration_date, issue_rate, daily_rate)
#    change_price = sm.change_price_bond(duration, convexity, basic_points)
    
#    st.write(f'La tasa diaria es --> {daily_rate}')
#    st.write(f'La duración es --> {duration}\nLa convexidad es --> {convexity}')
#    st.write(f'El cambio de precio es -- >{change_price}')

#    t = np.linspace(-1, 1, 20)/100
#    y2 = sm.change_price_bond(duration, convexity, t)
    
#    st.line_chart(y2)
    
