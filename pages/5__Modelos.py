from components.utils import *



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

st.latex('V(t,T) = S_{0} N(d_{1}) - e^{-r(T-t)} K N(d_{2})')

with Model_BS:


# INICIO



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


    if st.button('Calcular opción'):

        current_option = Option(
                            spot_price, strike_price,
                            expiration_time, interval_time,
                            volatility, risk_free
                            )



    if not ("current_option" in globals()):
        st.warning('Todo está tan tranquilo 🥱... clickea el botón justo arriba para calcular modelo binomial.')

    else:

            
        current_option.compute_UD()
        current_option.compute_risk_neutral()

        condition = current_option.D<(current_option.risk_free+1) and (current_option.risk_free+1) < current_option.U


        formula, info_box = st.columns(2)

        with formula:
            st.latex(f'''{round(current_option.D, 2)} <
                     {round(current_option.risk_free+1, 2)} <
                     {round(current_option.U, 2)}''')

        with info_box:
            if condition:
                st.success('No hay arbitraje, el análisis siguiente tiene coherencia')

            else:
                st.error('Hay arbitraje, no sigua pues')

        st.write(f'Price Spot: {current_option.spot}')
        st.write(f'Price Strike: {current_option.strike}')
        st.write(f'Volatility: {current_option.volatility}')
        st.write(f'Risk Free: {current_option.risk_free}')
        st.write(f'Expiration: {current_option.expiration}')
        st.write(f'Interval: {current_option.interval}')
        st.write(f'U: {current_option.U}')
        st.write(f'D: {current_option.D}')
        st.write(f'Prob risk neutral: {current_option.risk_neutral}')

# FIN




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
