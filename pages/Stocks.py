# >>> Importing libraries <<<
# Base
import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import datetime as dt
import os
from Components.instruments import Stock as Stock

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

with st.expander('Parámetros de las acciones'):

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
    
    source = pd.DataFrame({
            'Symbol': [],
            'Date': [],
            'Price': []

        })

    
    for key in stocks_instances.keys():

        stock_data = stocks_instances[key].cumulative_returns
        new_data = pd.DataFrame({
            'Date': stock_data['Date'],
            'Price': stock_data['Close'],
            'Symbol': key
        })
        source = pd.concat([source, new_data], ignore_index=True)

        #line += stocks_instances[key].trend_plot()
    base = alt.Chart(source).encode(
        alt.Color("Symbol").legend(None)
        )

    line = base.mark_line().encode(x="Date", y="Price")
    
    last_price = base.mark_circle().encode(
        alt.X("last_date['Date']:T"),
        alt.Y("last_date['Price']:Q")
        ).transform_aggregate(
            last_date="argmax(Date)",
            groupby=["Symbol"]
        )

    company_name = last_price.mark_text(align="left", dx=4).encode(text="Symbol")

    chart = (line + last_price + company_name).encode(
        x=alt.X().title("date"),
        y=alt.Y().title("price")
    )

    st.altair_chart(chart)

# Graph heatmap corr plot
st.write('## Correlation between closes prices')

df = pd.DataFrame()

with st.expander('SHOW GRAPH'):
    st.write('Coming soon')


    for key in stock_symbol_list:
        df[key] = stocks_instances[key].cumulative_returns['Close']
    correlation = df.corr(method='pearson')
    correlation = correlation.stack().reset_index()
    correlation.columns = ['S1','S2','Correlation']

    # Crear el heatmap con Altair
    heatmap = alt.Chart(correlation).mark_rect().encode(
        x='S1:O',
        y='S2:O',
        color='Correlation:Q'
    ).properties(
        width=400,
        height=400,
        title='Correlation Heatmap of Fruits'
    )

    # Rotar etiquetas del eje x para una mejor visualización
    heatmap = heatmap.configure_axisX(labelAngle=-45)

    # Display the chart
    st.write("Heatmap of Fruit Prices")
    st.altair_chart(heatmap)







