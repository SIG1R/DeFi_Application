import streamlit as st
from Bond import *
import pandas as pd


st.write("""
# Bond calculator
Establecer características del bono
""")

bond = Bond()

# Setting type of bond
type_bond = st.radio(
    'Tipo de bono',
    ['Con Cupon', 'Zero Cupon']
)


# Setting dates about the bond
ISSUE_DATE, EXPIRATION_DATE = st.columns(2)

with ISSUE_DATE: # Set issue_date input
    issue_date = st.date_input(
            'Fecha de emisión',
            format='DD/MM/YYYY',
            value=dt.date(2024,1,25),
    )

with EXPIRATION_DATE: # Set expiration_date input
    expiration_date = st.date_input(
            'Fecha de vencimiento',
            format='DD/MM/YYYY',
            value=dt.date(2027,11,3)
    )


# Setting rates about the bond
RATE_ISSUE_COLUMN, RATE_MARKET_COLUMN = st.columns(2)

with RATE_ISSUE_COLUMN: # Set issue_rate input
    face_rate = st.number_input('Tasa facial (%)', value=5.75)

with RATE_MARKET_COLUMN: # Set actual_date input
    market_rate = st.number_input('Tasa de mercado (%)', value=10.19)

bond = Bond(
        type_bond,
        issue_date, expiration_date,
        face_rate, market_rate)

data_example = pd.DataFrame({
    'N° pago': [i for i  in range(1,bond.total_payments+1)],
    'Fecha': bond.payments_dates,
    'FC': bond.cash_flow_,
    'Valor presente FC': bond.present_cash_flow
})



data_example['N° pago * Valor presente FC'] =  data_example['N° pago']*data_example['Valor presente FC']

data_example['N° pago^2 * Valor presente FC'] =  data_example['N° pago']**2*data_example['Valor presente FC']

bond.update(data_example)
st.write(data_example)


st.write(f'La duración del bono es {bond.duration} años')


st.write(f'La convexidad del bono es {bond.convexity}')


basic_points = np.linspace(-100,100, 100)

changes = bond.change_price(basic_points)

st.line_chart(changes)



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
    
