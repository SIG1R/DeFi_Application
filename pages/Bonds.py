import streamlit as st
from elements.Bond import *
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

bond = Bond()

with st.sidebar:

    st.write('#### Establezca las caracteristicas del bono')

    # Setting type of bond
    type_bond = st.radio(
        'Tipo de bono',
        ['Con Cupon', 'Zero Cupon'],
        horizontal = True
    )
    bond.type_bond=type_bond


    # Setting dates about the bond
    ISSUE_DATE, EXPIRATION_DATE = st.columns(2)

    with ISSUE_DATE: # Set issue_date input
    
        issue_date = st.date_input(
            'Fecha de emisión',
            format='DD/MM/YYYY',
            value=dt.date(2024,1,25),
        )
    
        bond.issue_date = issue_date # Update issue_date
        bond.update()

    with EXPIRATION_DATE: # Set expiration_date input
    
        expiration_date = st.date_input(
                'Fecha de vencimiento',
                format='DD/MM/YYYY',
                value=dt.date(2027,11,3)
         )

        bond.expiration_date = expiration_date # Update expiration_date
        bond.update()



    # Setting rates about the bond
    RATE_ISSUE_COLUMN, RATE_MARKET_COLUMN = st.columns(2)

    with RATE_ISSUE_COLUMN: # Set issue_rate input
    
        face_rate = st.number_input('Tasa facial (%)', value=5.75)
        bond.face_rate = face_rate # Update face_rate
        bond.update()

    with RATE_MARKET_COLUMN: # Set actual_date input
    
        market_rate = st.number_input('Tasa de mercado (%)', value=10.19)
        bond.market_rate = market_rate # Update market_rate
        bond.update()





st.write('## Flujo de caja')

st.write(bond.dataframe)


basic_points = np.linspace(-100,100, 100)

bond.change_price(basic_points)



st.write('## Convexidad - duración')
data = pd.DataFrame({
    'Duración': bond.generic_duration,
    'Convexidad': bond.generic_convexity    
})

#st.line_chart(data,x='Duración',color=['#27b4e3', '#ee7978'])

# Plot using Seaborn
sns.set(style="whitegrid")  # Optional: Set the style
fig, ax=plt.subplots()  # Optional: Set the figure size
sns.lineplot(data=data, ax=ax)
ax.set_xlabel('Puntos básicos')
ax.set_ylabel('Precio bono')
ax.set_title('Line Chart')
ax.legend(title='Variable', labels=['Duración', 'Convexidad'])  # Optional: Add legend
st.pyplot(fig)

#basic_points = st.number_input('Puntos básicos (%)') / 100

#st.write(type(fecha_fin))
#if st.button('calcular'):

    #st.write(val.zero_coupon(0.1, expiration_date, issue_date))
    #st.write(f'Siguientes cobros del cupón {sm.duration(expiration_date,0)}')
#    daily_rate = sm.convertion_rate(actual_rate)*100
    #st.write(f'{sm.duration_convexity(expiration_date, 5.75, daily_rate)}')
    
#    duration, convexity = sm.duration_convexity(expiration_date, issue_rate, daily_rate)
#    change_price = sm.change_price_bond(duration, convexity, basic_points)

#    st.write(f'La tasa diaria es --> {daily_rate}')
#    st.write(f'La duración es --> {duration}\nLa convexidad es --> {convexity}')
#    st.write(f'El cambio de precio es -- >{change_price}')

#    t = np.linspace(-1, 1, 20)/100
#    y2 = sm.change_price_bond(duration, convexity, t)
    
#    st.line_chart(y2)
    
