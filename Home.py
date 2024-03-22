import streamlit as st


st.markdown("""
# Aplicativo financiero
¡Bienvenido a nuestro aplicativo de análisis financiero!

En el mundo cada vez más complejo de las inversiones, entender y evaluar los diferentes instrumentos financieros es crucial para tomar decisiones informadas y maximizar el potencial de retorno. Es en este contexto que nace nuestro proyecto, un aplicativo diseñado para brindar análisis detallados de una amplia gama de instrumentos financieros, incluyendo bonos, acciones y fondos de inversión.

Nuestra plataforma proporciona a los usuarios una herramienta poderosa para evaluar y comparar diferentes opciones de inversión. Desde la valoración de bonos corporativos hasta el análisis fundamental de acciones, nuestro aplicativo ofrece una variedad de herramientas y métricas para ayudar a los inversores a tomar decisiones informadas y estratégicas.

Además de ofrecer análisis detallados de instrumentos financieros individuales, nuestro aplicativo también permite a los usuarios realizar comparaciones entre diferentes activos, evaluar el rendimiento histórico, y proyectar posibles escenarios futuros. Todo esto se presenta de manera clara y accesible, facilitando la comprensión incluso para aquellos que son nuevos en el mundo de las inversiones.

Ya sea que seas un inversor experimentado en busca de información detallada o un principiante que busca aprender más sobre el mercado financiero, nuestro aplicativo está diseñado para satisfacer tus necesidades. Únete a nosotros mientras exploramos el emocionante mundo de las inversiones y te ayudamos a alcanzar tus objetivos financieros.

¡Comienza a explorar ahora y lleva tus inversiones al siguiente nivel!
""")



st.sidebar.success('Seleccione algún instrumento financiero 👆')

import streamlit as st
import streamlit.components.v1 as components

components.html(
    """
        <a href="https://www.instagram.com/_sigir_/" class="twitter-share-button" 
        data-text="Check my cool Streamlit Web-App🎈" 
        data-url="https://streamlit.io"
        data-show-count="false">
        data-size="Large" 
        data-hashtags="streamlit,python"
        Tweet
        </a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
)





