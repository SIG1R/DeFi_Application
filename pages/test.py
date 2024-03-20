import pandas as pd
import altair as alt
import streamlit as st

# Supongamos que 'stocks_instances' es un diccionario que contiene los datos de las acciones

# Crear un DataFrame con los datos de todas las acciones
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

# Crear un heatmap
heatmap = alt.Chart(source).mark_rect().encode(
    alt.X('month(Date):O', title='Month'),
    alt.Y('Symbol:O', title='Symbol'),
    color=alt.Color('mean(Price):Q', scale=alt.Scale(scheme='viridis'), title='Mean Price')
).properties(
    width=800,
    height=400,
    title='Heatmap of Mean Prices by Month and Symbol'
)

# Mostrar el heatmap
st.write('## Heatmap of Mean Prices by Month and Symbol')
st.altair_chart(heatmap)

