import warnings
    
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go
from st_pages import add_page_title, hide_pages

add_page_title(layout="wide")

st.markdown("#")

warnings.filterwarnings("ignore")

az.style.use("arviz-darkgrid")

seed: int = sum(map(ord, "mmm"))
rng: np.random.Generator = np.random.default_rng(seed=seed)

data = pd.read_csv("data/data.csv")

fig = go.Figure()

fig.add_trace(go.Scatter(x=data["date_week"], y=data["volumen"], mode='lines', name='Datos'))
fig.update_layout(xaxis_title='Tiempo',
                  yaxis_title='Volumen')

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)

st.dataframe(data)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("---")