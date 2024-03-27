import streamlit as st
from components.instruments import Option

# >>> Settings of the option <<<
st.write('## Definir las características de la opción')
col1, col2, col3 = st.columns(3)

with col1:
    st.write('#### Tiempo')
    expiration_time = st.number_input('Fecha de vencimiento')
    interval_time = st.radio('Tiempo de expiración', ['Día', 'Semana', 'Mes', 'Año'], horizontal=True)

with col2:
    st.write('#### Precio')
    spot_price = st.number_input('Precio Spot')
    strike_price = st.number_input('Precio Strike')

with col3:
    st.write('#### Otros')
    #number_steps = st.number_input('Números de pasos en el árbol')
    volatility = st.number_input('Volatilidad')
    risk_free = st.number_input('Tasa libre de riesgo')
    type_option = st.radio('Tipo de opción', ['Call', 'Put'], horizontal=True)

current_option = Option(spot_price, strike_price,
                        expiration_time, interval_time,
                        volatility, risk_free 
                        )
    
current_option.compute_UD()
current_option.compute_risk_neutral()
current_pay_off = current_option.pay_off(type_option, 40)

st.write(f'Price Spot: {current_option.spot}')
st.write(f'Price Strike: {current_option.strike}')
st.write(f'Volatility: {current_option.volatility}')
st.write(f'Risk Free: {current_option.risk_free}')
st.write(f'Expiration: {current_option.expiration}')
st.write(f'Interval: {current_option.interval}')
st.write(f'Type option: {type_option} --> pay-off {current_pay_off}')
st.write(f'U: {current_option.U}')
st.write(f'D: {current_option.D}')
st.write(f'Prob risk neutral: {current_option.risk_neutral}')





#st.write(func())
