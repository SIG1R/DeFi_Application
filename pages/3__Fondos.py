# >>> Importing libraries <<<
import streamlit as st
from components.instruments import Found
from components.utils import graph_data
import pandas as pd
import os
import altair as al
import datetime as dt 

archivo_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'stocks_list.csv')
stocks_available = pd.read_csv(archivo_csv)

founds_instances = dict()


st.markdown('#### Selección de parámetros')

stock_name, market_name = st.columns(2)
# Select stocks
with stock_name:


    founds_selected = st.multiselect('Seleccione los fondos',
                           stocks_available['Company Name']) 
    
    start_date = st.date_input(
        'Fecha de inicio',
        format = 'DD/MM/YYYY',
        value = dt.date(2024,1,1)
    )
    
    Rate_actual = st.number_input('Tasa actual')/100

# Select market index
with market_name:
    index_market = st.selectbox(
            'Seleccione el índice del mercado',
            ["^GSPC", "^DJI", "^IXIC", "^NYA", "^RUT", "^FTSE", "^N225"],
    )

    end_date = st.date_input(
        'Fecha de cierre',
        format = 'DD/MM/YYYY'
        )

    Rate_free = st.number_input('Tasa libre de riesgo')/100



for found_name in founds_selected:

    stock_symbol = stocks_available[stocks_available['Company Name']==found_name] 
    stock_symbol = stock_symbol['Symbol'].to_list()[0]

    founds_instances[found_name] = Found(stock_symbol, index_market)
    founds_instances[found_name].get_data(start_date, end_date)
    founds_instances[found_name].calculate_returns()
    founds_instances[found_name].capm(Rate_free, Rate_actual)


graph = graph_data('Stock', 'Beta', 'Alpha')

for key in founds_instances.keys():

    row = {'Stock': [key],
           'Beta': [founds_instances[key].beta],
           'Alpha': [founds_instances[key].alpha]
    }
    graph.add_row(pd.DataFrame(row))



beta_chart = graph.bar_chart('Stock', 'Beta', 'Gráfico de distribución de betas')
alpha_chart = graph.bar_chart('Stock', 'Alpha', 'Gráfico de distribución de alphas de Jensen')


jensen, betas = st.columns(2)

with jensen:

    st.altair_chart(beta_chart)
    
with betas:
    st.altair_chart(alpha_chart)
