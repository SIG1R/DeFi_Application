# >>> Importing libraries <<<
# Base
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import datetime as dt
import os
from components.instruments import Stock as Stock
from components.utils import graph_data

# Numericals and data
import numpy as np
import yfinance as yf
import pandas as pd

# Visualizations
import matplotlib.pyplot as plt
import altair as alt


archivo_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'stocks_list.csv')
stocks_available = pd.read_csv(archivo_csv)

stocks_instances = dict()


st.write('#### Establezca las caracteristicas de las acciones')

stock_symbol_list = st.multiselect(
    'Seleccione las acciones a analizar',
    stocks_available['Company Name']
)

for stock_name in stock_symbol_list:

    stock_symbol = stocks_available[stocks_available['Company Name']==stock_name] 
    stock_symbol = stock_symbol['Symbol'].to_list()[0]

    stocks_instances[stock_symbol] = Stock(stock_symbol)


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
for key in stocks_instances.keys():
    
    
    st.metric(
            label = key,
            value = round(stocks_instances[key].history['Close'][-1],4), 
            delta = round(stocks_instances[key].history['Close'][-1]
                      -stocks_instances[key].history['Close'][-2],4)
    )

        #st.table(stocks_instances[key].history)


    
source = graph_data('Symbol', 'Date', 'Returns')

for key in stocks_instances.keys():

    # Get cumulative returns
    stock_data = stocks_instances[key].cumulative_returns

    # Create new transaction
    # Symbo, Date, Returns
    row = {
        'Symbol': key,
        'Date': stock_data['Date'],
        'Returns': stock_data['Close']
    }
    
    # Adding transaction to dataframe
    source.add_row(pd.DataFrame(row))

# Plotting line chart (trend returns)
trend_chart = source.trend_chart('Date', 'Returns', 'Symbol', 'Crecimiento en los retornos acumulados')
st.altair_chart(trend_chart)








# Graph heatmap corr plot
df = pd.DataFrame()


for key in stock_symbol_list:


    stock_symbol = stocks_available[stocks_available['Company Name']==key] 
    stock_symbol = stock_symbol['Symbol'].to_list()[0]

    df[stock_symbol] = stocks_instances[stock_symbol].cumulative_returns['Close']
correlation = df.corr(method='pearson')
correlation = correlation.stack().reset_index()
correlation.columns = ['S1','S2','Correlation']

# Crear el heatmap con Altair
heatmap = alt.Chart(correlation).mark_rect().encode(
    x='S1:O',
    y='S2:O',
    color='Correlation:Q'
).properties(
    width=500,
    height=400,
    title='Correlation Heatmap of Fruits'
)

# Rotar etiquetas del eje x para una mejor visualización
heatmap = heatmap.configure_axisX(labelAngle=-45)

# Display the chart
st.altair_chart(heatmap)

