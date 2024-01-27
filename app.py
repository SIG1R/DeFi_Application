import streamlit as st
import valuation as val

st.write("""
# Bond calculator
Establecer características del bono
""")

# Setting type of bond
type_bond = st.selectbox(
    'Tipo de bono',
    ('Zero Cupon', 'Cupon Bond')
)

# Setting dates about the bond
issue_date, expiration_date = st.columns(2)

with issue_date: # Set issue_date input
    fecha_inicio = st.date_input('Fecha de emisión')

with expiration_date: # Set expiration_date input
    fecha_fin = st.date_input('Fecha de vencimiento')

#st.write(type(fecha_fin))
if st.button('calcular'):
    
    st.write((fecha_fin-fecha_inicio).days)
