import streamlit as st
import valuation as val

st.write("""
# Bond calculator
Establecer características del bono
""")

# Setting pages
if st.button("Settings"):
    st.switch_page("app.py")

if st.button("Sensitivity Measures"):
    st.switch_page("pages/test.py")


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



