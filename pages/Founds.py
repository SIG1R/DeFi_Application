import streamlit as st
from Components.instruments import Found
import pandas as pd

with st.sidebar:
    found = st.multiselect('Seleccione los fondos', ['KO','TLSA'])
    index_market = st.multiselect('Seleccione el índice del mercado',
                                  ["^GSPC", "^DJI", "^IXIC", "^NYA", "^RUT", "^FTSE", "^N225"],
                    )


    f = Found(found, index_market)

st.write('# Modelo CAMP')
st.write(f'Nombre del fondo {f.found}')
st.write(f'Nombre del índice {f.index_market}')
st.write(f'Resultado beta {f.beta}')


