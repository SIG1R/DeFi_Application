import streamlit as st
from components.instruments import Option
from components.stochastic import Black_Scholes as BS
from streamlit_extras.metric_cards import style_metric_cards as SMC
import os
import pandas as pd
import yfinance as yf
import numpy as np

Model_BS, Model_M = st.tabs(['Black Scholes', 'Merton'])

archivo_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'stocks_list.csv')
stocks_available = pd.read_csv(archivo_csv)

with Model_BS:
    # st.write('## Black and Scholes')

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

    current_option = Option(spot_price, strike_price,
                            expiration_time, interval_time,
                            volatility, risk_free 
                            )
        
    current_option.compute_UD()
    current_option.compute_risk_neutral()

    MBS = BS(current_option)

    MBS.pay_off(type_option)

    ds, Nds = st.columns(2)
    
    with ds:
        st.metric(label= 'd1', value=round(MBS.d1, 3))
        st.metric(label= 'd2', value=round(MBS.d2, 3))
    
    with Nds:
        st.metric(label= 'N(d1)', value=round(MBS.prob_d1, 3))
        st.metric(label= 'N(d2)', value=round(MBS.prob_d2, 3))

    st.metric(label= 'Pay off', value=round(MBS.payoff, 3))
    
    SMC()

with Model_M:
    st.write('## Merton')
