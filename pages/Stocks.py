import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
from streamlit_extras.metric_cards import style_metric_cards


from elements.Stock import *


stocks_available = pd.read_csv('stocks_list.csv')

stocks_instances = dict()

with st.sidebar:

    st.write('#### Establezca las caracteristicas de las acciones')

    stock_symbol_list = st.multiselect(
        'Seleccione las acciones a analizar',
        stocks_available['Symbol']
    )
    
    for instance in stock_symbol_list:
        stocks_instances[instance] = Stock(instance)


    start_date_column, end_date_column = st.columns(2)

    with start_date_column:

        start_date = st.date_input(
            'Fecha de inicio',
            format = 'DD/MM/YYYY',
            value = dt.date(2024,1,1)
        )


    with end_date_column:

        end_date = st.date_input(
            'Fecha de cierre',
            format = 'DD/MM/YYYY'
    )

        
    for key in stocks_instances.keys():
        stocks_instances[key].get_data(start_date, end_date)
        stocks_instances[key].calculate_returns()


# Graph individual summary per stock
st.write('## Individual stock summary')
with st.expander('SHOW SUMMARY'):
    for key in stocks_instances.keys():
        
        st.write(f'### {key}')
        col1, col2, col3 = st.columns(3)
        col1.metric(
                label = 'Highest price',
                value = round(stocks_instances[key].history['High'][-1],4), 
                delta = round(stocks_instances[key].history['High'][-1]
                          -stocks_instances[key].history['High'][-2],4)
        )

        col2.metric(
                label = 'Lowest price',
                value = round(stocks_instances[key].history['Low'][-1],4), 
                delta = round(stocks_instances[key].history['Low'][-1]
                          -stocks_instances[key].history['Low'][-2],4)
        )

        col3.metric(
                label = 'Close price',
                value = round(stocks_instances[key].history['Close'][-1],4), 
                delta = round(stocks_instances[key].history['Close'][-1]
                          -stocks_instances[key].history['Close'][-2],4)
        )

        #st.table(stocks_instances[key].history)


# Graph line plot
st.write('## Trend history')
with st.expander('SHOW GRAPH'):
    st.write('Coming soon')
    
    for key in stocks_instances.keys():
        st.write(f'Closes prices of {key}')
        st.table(stocks_instances[key].cumulative_returns)

    #altair_trend_plot = stocks_instances['NVDA'].trend_plot()
    #st.altair_char(altair_trend_plot)

# Graph heatmap corr plot
st.write('## Correlation between closes prices')
with st.expander('SHOW GRAPH'):
    st.write('Coming soon')

#for key in stocks_instances.keys():
#    st.write(stocks_instances[key].ticker, start_date, end_date)
