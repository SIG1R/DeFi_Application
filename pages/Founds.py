import streamlit as st
from elements.Found import *
import pandas as pd

with st.sidebar:
    st.multiselect('Seleccione los fondos', ['fds','fasdf'])



st.write('# Modelo CAMP')
f = Found()
st.write(f'Nombre del fondo {f.name}')


