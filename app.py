import streamlit as st
import valuation as val
import sensitivity_measures as sm

st.write("""
# Bond calculator
Establecer características del bono
""")

# Setting type of bond
type_bond = st.selectbox(
    'Tipo de bono',
    ('Zero Cupon', 'Cupon Bond')
)

# Setting dates about the bond
ISSUE_DATE, EXPIRATION_DATE = st.columns(2)

with ISSUE_DATE: # Set issue_date input
    issue_date = st.date_input('Fecha de emisión')

with EXPIRATION_DATE: # Set expiration_date input
    expiration_date = st.date_input('Fecha de vencimiento')


# Setting rates about the bond
ISSUE_RATE, ACTUAL_RATE = st.columns(2)

with ISSUE_RATE: # Set issue_rate input
    issue_rate = st.number_input('Tasa de emisión') / 100

with ACTUAL_RATE: # Set actual_date input
    actual_rate = st.number_input('Tasa de mercado') / 100

#st.write(type(fecha_fin))
if st.button('calcular'):

    #st.write(val.zero_coupon(0.1, expiration_date, issue_date))
    #st.write(f'Siguientes cobros del cupón {sm.duration(expiration_date,0)}')
    daily_rate = sm.convertion_rate(actual_rate)*100
    st.write(f'La tasa diaria es {daily_rate}')
    st.write(f'{sm.duration(expiration_date, 5.75, daily_rate)}')
