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
    
from pymc_marketing.mmm.delayed_saturated_mmm import DelayedSaturatedMMM
from pymc_marketing.mmm.budget_optimizer import calculate_expected_contribution

add_page_title(layout="wide")

st.markdown("#")

warnings.filterwarnings("ignore")

az.style.use("arviz-darkgrid")

seed: int = sum(map(ord, "mmm"))
rng: np.random.Generator = np.random.default_rng(seed=seed)

name = "model/budget_optimizer_model_fin.nc"
mmm = DelayedSaturatedMMM.load(name)

data = pd.read_csv("data/data.csv")

sigmoid_params = mmm.compute_channel_curve_optimization_parameters_original_scale(
    method="michaelis-menten"
)

total_budget = st.number_input("Ingrese el presupuesto total en medios:", min_value=0, max_value=100000)

channels = ["inversion_digital", "inversion_tv", "inversion_impresa"]

# Ingresar los otros 3 valores
col1, col2, col3 = st.columns(3)
with col1:
    budget_per_digital = st.number_input("Presupuesto Digital:", min_value=0, max_value=total_budget, key=None)
with col2:
    budget_per_tv = st.number_input("Presupuesto Televisión:", min_value=0, max_value=total_budget, key=None)
with col3:
    budget_per_impresa = st.number_input("Presupuesto Impresa:", min_value=0, max_value=total_budget, key=None)

# Sumar los valores
suma_valores = budget_per_digital + budget_per_tv + budget_per_impresa

initial_budget_dict = {'inversion_digital': budget_per_digital,
     'inversion_tv': budget_per_tv,
     'inversion_impresa': budget_per_impresa}

initial_contribution = calculate_expected_contribution(
        method="michaelis-menten", parameters=sigmoid_params, budget=initial_budget_dict
    )
    
# Initial budget & contribution dictionary
initial_scenario = {
        "initial_contribution": initial_contribution,
        "initial_budget": initial_budget_dict,
    }

platform_base_optimization = mmm.optimize_channel_budget_for_maximum_contribution(
        method="michaelis-menten",
        total_budget=total_budget,
        parameters=sigmoid_params,
        budget_bounds={"inversion_digital": [0, 20000], 
                       "inversion_tv": [0, 25000],
                      "inversion_impresa": [0, 18000]},
    )

# Comprobar si la suma supera el valor límite
if suma_valores > total_budget:
    st.error("No puede ingresar valores que superen el valor máximo de presupuesto.")
else:
    st.success("Los valores son válidos y no superan el límite de presupuesto.")
    cols, colt = st.columns(2)
    with cols:
        st.write(f"Tu presupuesto en medios es: {suma_valores} S/")
    with colt:
        st.write(f"Te quedan por agregar: {total_budget-suma_valores} S/")

    st.write("Escenario de contribuciones ajustado a tu presupuesto")
    st.pyplot(mmm.plot_budget_scenearios(
        base_data=initial_scenario, method="michaelis-menten", scenarios_data=[platform_base_optimization]
    ));

    # Interpretacion del ROI: contribucion en kg * precios soles / inversion soles
    # colroiop, colroiact = st.columns(2)
    # with colroiop:
    #     st.write("ROI óptimo")
    #     fig, ax = plt.subplots(figsize=(10, 5))
    #     (
    #     pd.Series(data=[platform_base_optimization['contribution'][0]*data['precios'].mean()/platform_base_optimization['budget'][0], 
    #                         platform_base_optimization['contribution'][1]*data['precios'].mean()/platform_base_optimization['budget'][1], 
    #                         platform_base_optimization['contribution'][2]*data['precios'].mean()/platform_base_optimization['budget'][2]], 
    #                   index=["ROI Digital", "ROI TV", "ROI Impresa"]).plot(
    #             kind="bar", color=["C0", "C1", "C2"], rot=0
    #         )
    #     )
    #     st.pyplot(fig);
    # with colroiact:
    #     st.write("ROI de tu presupuesto")
    #     #roi_optimo =  
    #     fig, ax = plt.subplots(figsize=(10, 5))
    #     (
    #         pd.Series(data=[sigmoid_params['inversion_digital'][0]*data['precios'].mean()/budget_per_digital, 
    #                         sigmoid_params['inversion_tv'][0]*data['precios'].mean()/budget_per_tv, 
    #                         sigmoid_params['inversion_impresa'][0]*data['precios'].mean()/budget_per_impresa], 
    #                   index=["ROI Digital", "ROI TV", "ROI Impresa"]).plot(
    #             kind="bar", color=["C0", "C1", "C2"], rot=0
    #         )
    #     )
    #     st.pyplot(fig);
        
    st.write(f"Recomendación de presupuesto óptimo y contribución esperada según tu presupuesto total")
    platform_base_optimization.columns = ['contribución óptima', 'inversión óptima']
    st.dataframe(platform_base_optimization);  
    
    cola, colb = st.columns(2)
    with cola:
        fig_opt_con = go.Figure(go.Bar(
            x=["inversion_digital", "inversion_tv", "inversion_impresa"],
            y=[sigmoid_params['inversion_digital'][0], 
               sigmoid_params['inversion_tv'][0], 
               sigmoid_params['inversion_impresa'][0]],
            orientation='v',
            marker=dict(color='#76D7C4'),
            text=[round(sigmoid_params['inversion_digital'][0], 2), 
                  round(sigmoid_params['inversion_tv'][0], 2), 
               round(sigmoid_params['inversion_impresa'][0], 2)],
            textposition='auto'
            ))
            
        fig_opt_con.update_layout(
                title='Valores óptimos de contribución',
                xaxis_title='Medios',
                yaxis_title='Contribución S/',
                width=320, 
                height=450
            )
        st.plotly_chart(fig_opt_con)
    
    with colb:
        fig_opt = go.Figure(go.Bar(
            x=[20000, 
               25000, 
               18000],
            y=["inversion_digital", "inversion_tv", "inversion_impresa"],
            orientation='h',
            marker=dict(color='skyblue'),
            text=[20000, 
               25000, 
               18000],  # Mostrar los valores en las barras
            textposition='auto'
            ))
        
        # Configurar el título del gráfico
        fig_opt.update_layout(
            title='Valores óptimos de inversión',
            xaxis_title='Inversión',
            yaxis_title='Medios',
            yaxis=dict(autorange='reversed'),  # Invertir el orden de las categorías
            width=450,  # Ancho del gráfico
            height=320
        )
        
        # Mostrar el gráfico en la aplicación de Streamlit
        st.plotly_chart(fig_opt)  
    
    # Use the function `calculate_expected_contribution` to estimate
    # the contribution of your initial budget based on the curve parameters.
    
    

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("---")