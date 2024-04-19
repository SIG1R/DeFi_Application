import streamlit as st
from components.instruments import Option
from components.stochastic import Black_Scholes as BS
from streamlit_extras.metric_cards import style_metric_cards as SMC
import os
import pandas as pd
import yfinance as yf
import numpy as np


archivo_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'stocks_list.csv')
stocks_available = pd.read_csv(archivo_csv)


st.write('# Merton')
st.write('## Definir las características de la opción')

stock_symbol = st.selectbox(
    'Seleccione las acciones a analizar',
    stocks_available['Symbol']
)

stock = yf.Ticker(stock_symbol)

stock_history = stock.history(period='1y')

returns = stock_history['Close'].pct_change()

volatility_t = np.std(returns, ddof=1)





# >>> Settings of the option <<<
col1, col2, col3 = st.columns(3)
col11, col22 = st.columns(2)

with col1:
    st.write('#### Tiempo')
    expiration_time = st.number_input('Fecha de vencimiento', value=4)
    interval_time = st.radio('Tiempo de expiración', ['Día', 'Semana', 'Mes', 'Año'], horizontal=True)

with col2:
    st.write('#### Precio')
    spot_price = st.number_input('Precio Spot', value=8.48)
    strike_price = st.number_input('Precio Strike', value=8.5)

with col3:
    st.write('#### Otros')
    #number_steps = st.number_input('Números de pasos en el árbol')
    volatility = st.number_input('Volatilidad', value=volatility_t)
    risk_free = st.number_input('Tasa libre de riesgo', value=5.29)
    type_option = st.radio('Tipo de opción', ['Call', 'Put'], horizontal=True)


with col11:
    lambd_ = st.number_input('Valor de lambda')

with col22:
    v_jump = st.number_input('Valor de la volatilidad de lambda')


current_option = Option(spot_price, strike_price,
                        expiration_time, interval_time,
                        volatility, risk_free 
                        )
    
current_option.compute_UD()
current_option.compute_risk_neutral()

MBS = BS(current_option)
val = MBS.merton(lambd_, v_jump, 100, type_option)

st.write(val)
