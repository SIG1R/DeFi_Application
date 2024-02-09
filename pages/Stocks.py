import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

from elements.Stock import *


stocks_available = pd.read_csv('stocks_list.csv')
stocks_to_use = []

with st.sidebar:

    st.write('#### Establezca las caracteristicas de las acciones')

    stock_symbol_list = st.multiselect(
        'Seleccione las acciones a analizar',
        stocks_available['Symbol']
    )

    for symbol in stock_symbol_list:
        company_name = stocks_available[stocks_available['Symbol']==symbol]['Company Name']
        yf.Ticker(symbol)
        stocks_to_use.append(Stock(symbol, company_name))




for stock in stocks_to_use:
    st.write(f'La acción con symbolo {stock.symbol}')


st.write('# Valoración de activos')
