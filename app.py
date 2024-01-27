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
ISSUE_DATE, EXPIRATION_DATE = st.columns(2)

with ISSUE_DATE: # Set issue_date input
    issue_date = st.date_input('Fecha de emisión')

with EXPIRATION_DATE: # Set expiration_date input
    expiration_date = st.date_input('Fecha de vencimiento')


#st.write(type(fecha_fin))
if st.button('calcular'):
    
    st.write(val.zero_coupon(0.1, expiration_date, issue_date))
