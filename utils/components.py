import warnings
    
import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc as pm
import seaborn as sns
import streamlit as st
from st_pages import add_page_title, hide_pages
    
from pymc_marketing.mmm.delayed_saturated_mmm import DelayedSaturatedMMM

add_page_title(layout="wide")

st.markdown("#")

warnings.filterwarnings("ignore")

az.style.use("arviz-darkgrid")

seed: int = sum(map(ord, "mmm"))
rng: np.random.Generator = np.random.default_rng(seed=seed)

name = "model/budget_optimizer_model_fin.nc"
mmm = DelayedSaturatedMMM.load(name)

componentes = {
    "Volumen Base": [
        "intercept",
        "tendencia",
        "yearly_seasonality",
        "sin_order_1",
        "sin_order_2",
        "sin_order_3",
        "cos_order_1",
        "cos_order_2",
        "cos_order_3",
    ],
    "lanzamientos": ["lanzamientos"],
    "Canal inversion_tv": ["inversion_tv"],
    "Canal inversion_digital": ["inversion_digital"],
    "Canal inversion_impresa": ["inversion_impresa"],
    "Precios": ["precios"],
    "Promociones": ["promociones"],
}

#st.header('Contribución acumulada')
fig_2 = st.pyplot(mmm.plot_waterfall_components_decomposition(figsize=(8, 5)))

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("---")