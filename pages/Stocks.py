import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

from elements.Stock import *


stocks_available = pd.read_csv('stocks_list.csv')


with st.sidebar:

    st.write('#### Establezca las caracteristicas de las acciones')

    stock_symbol_list = st.multiselect(
        'Seleccione las acciones a analizar',
        stocks_available['Symbol']
    )

    for symbol in stock_symbol_list:
        company_name = stocks_available[stocks_available['Symbol']==symbol]['Company Name']
        yf.Ticker(symbol)
        symbol = Stock(symbol, company_name)

for symbol in stock_symbol_list:
    st.write(f'La acción con symbolo {symbol}')
