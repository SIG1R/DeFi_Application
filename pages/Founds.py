# >>> Importing libraries <<<
import streamlit as st
from Components.instruments import Found
import pandas as pd
import os
import altair as al
import datetime as dt 

archivo_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'stocks_list.csv')
stocks_available = pd.read_csv(archivo_csv)

founds_instances = dict()



# >>> Creating settings sesion <<<
with st.expander('Parámetros'):

    # Select stocks
    founds_selected = st.multiselect('Seleccione los fondos',
                           stocks_available['Symbol']) 
    
    # Select market index
    index_market = st.selectbox(
            'Seleccione el índice del mercado',
            ["^GSPC", "^DJI", "^IXIC", "^NYA", "^RUT", "^FTSE", "^N225"],
    )
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
    
    Rate_actual_column, Rate_free_column = st.columns(2)

    with Rate_actual_column:

        Rate_actual = st.number_input('Tasa actual')/100

    with Rate_free_column:


        Rate_free = st.number_input('Tasa libre de riesgo')/100

for found_name in founds_selected:

    founds_instances[found_name] = Found(found_name, index_market)
    founds_instances[found_name].get_data(start_date, end_date)
    founds_instances[found_name].calculate_returns()
    founds_instances[found_name].capm(Rate_free, Rate_actual)

    
to_graph = pd.DataFrame({
    'Stock': [],
    'Beta': [],
    'Alpha': []
})


for key in founds_instances.keys():

    row = [key, founds_instances[key].beta, founds_instances[key].alpha]
    to_graph.loc[len(to_graph)] = row

    st.write(f'{founds_instances[key].found_name}\t beta: {founds_instances[key].beta}\t alpha: {founds_instances[key].alpha}')

c = al.Chart(to_graph).mark_bar().encode(
        x='Stock',
        y='Beta')

st.altair_chart(c)


a = al.Chart(to_graph).mark_bar().encode(
        x='Stock',
        y='Alpha')

st.altair_chart(a)
