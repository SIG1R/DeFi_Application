# >>> Importing libraries <<<
import streamlit as st
from Components.instruments import Found
import pandas as pd
import os

archivo_csv = os.path.join(os.path.dirname(__file__), '..', 'data', 'stocks_list.csv')
stocks_available = pd.read_csv(archivo_csv)

stocks_instances = dict()



# >>> Creating settings sesion <<<
with st.expander('Parámetros'):

    # Select stocks
    found = st.multiselect('Seleccione los fondos',
                           stocks_available['Symbol']) 
    
    # Select market index
    index_market = st.selectbox(
            'Seleccione el índice del mercado',
            ["^GSPC", "^DJI", "^IXIC", "^NYA", "^RUT", "^FTSE", "^N225"],
    )


    f = Found(found, index_market)

st.write('# Modelo CAMP')
st.write(f'Nombre del fondo {f.found}')
st.write(f'Nombre del índice {f.index_market}')
st.write(f'Resultado beta {f.beta}')


