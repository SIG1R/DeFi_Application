from components.utils import *



import streamlit as st
from components.instruments import Option
from components.stochastic import Black_Scholes as BS
from streamlit_extras.metric_cards import style_metric_cards as SMC
import os
import pandas as pd
import yfinance as yf
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


archivo_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'stocks_list.csv')
stocks_available = pd.read_csv(archivo_csv)



archivo_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'stocks_list.csv')
stocks_available = pd.read_csv(archivo_csv)

# >>> Settings of the option <<<

st.markdown('#### Defina las características del mercado')


grid_stock = st.columns(2)

with grid_stock[0]: # Stock symbol and volatility inputs into the column
    stock_name = st.selectbox(
        'Seleccione la acción',
        stocks_available['Company Name']
    )

    stock_symbol = stocks_available[stocks_available['Company Name']==stock_name] 
    stock_symbol = stock_symbol['Symbol'].to_list()[0]


    stock = yf.Ticker(stock_symbol)

    stock_history = stock.history(period='1y')

    returns = stock_history['Close'].pct_change()

    volatility = np.std(returns, ddof=1)


    spot_price = stock_history['Close'][-1]


    volatility = st.number_input('Volatilidad',
                                    value=volatility
                                    )
    
with grid_stock[1]: # Risk free and spot price inputs into the column
    risk_free = st.number_input('Tasa libre de riesgo',
                                value=0.0,
                                step=1.,
                                format = '%.2f'
                                )
    spot_price = st.number_input('Precio Spot', value=spot_price)


# >>> Settings of the option <<<
st.markdown('#### Definir las características de la opción')

st.info(f'''**Nota:** Para conocer más sobre las opciones de **{stock_name}** tranzadas actualmente en el mercado, puede hacer click
        [aquí](https://finance.yahoo.com/quote/{stock_symbol}/options/)''')


grid_option = st.columns(2)

with grid_option[0]:
    expiration_time = st.number_input('Fecha de vencimiento', value=0)
    interval_time = st.radio('Tiempo de expiración', ['Semana', 'Mes', 'Año'], horizontal=True)

with grid_option[1]:
    strike_price = st.number_input('Precio Strike', value=0)
    type_option = st.radio('Tipo de opción', ['Call', 'Put'], horizontal=True)

# When the button is clicked, this's activated
if st.button('Calcular opción'):

    # Create a instance of Option
    current_option = Option(
                        spot_price, strike_price,
                        expiration_time, interval_time,
                        volatility, risk_free
                        )

    # Cumpote U and D
    current_option.compute_UD()
    
    # Convert the risk neutral to daily, weekly...
    current_option.compute_risk_neutral()

    # Create a instance of Black and Scholes
    MBS = BS(current_option)

    # Compute the pay-off
    MBS.pay_off(type_option)
    ds, Nds = st.columns(2) # Get the ds and N(ds) inherit of pay-off


    with ds:
        st.metric(label= 'd1', value=round(MBS.d1, 3))
        st.metric(label= 'd2', value=round(MBS.d2, 3))
    
    with Nds:
        st.metric(label= 'N(d1)', value=round(MBS.prob_d1, 3))
        st.metric(label= 'N(d2)', value=round(MBS.prob_d2, 3))

    st.metric(label= 'Pay off', value=round(MBS.payoff, 3))
    
    SMC()
    
    condition = current_option.D<(current_option.risk_free+1) and (current_option.risk_free+1) < current_option.U


    formula, info_box = st.columns(2)

    with info_box:
        if condition:
            st.success('No hay arbitraje, el análisis siguiente tiene coherencia')

        else:
            st.error('Hay arbitraje, no sigua pues')


if not ("current_option" in globals()):
    st.warning('Todo está tan tranquilo 🥱... clickea el botón justo arriba para calcular modelo Black and Scholes.')



