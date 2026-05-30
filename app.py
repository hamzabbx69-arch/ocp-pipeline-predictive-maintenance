import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ml_predictive_maintenance import predict_anomaly, calculate_rul

# Configuration de la page
st.set_page_config(page_title="OCP Digital Twin - Maintenance Prédictive", layout="wide")

st.title("🏭 OCP Jorf Lasfar — Maintenance Prédictive des Pipelines")
st.markdown("### 🌐 Système de Jumeau Numérique (Digital Twin) basé sur OpenFOAM & ML")
st.write("---")

# Chargement des données industrielles
df = pd.read_csv("industrial_predictive_maintenance_data.csv")

# Contrôle temporel de la simulation
st.sidebar.header("🎛️ Contrôle de la Simulation")
time_step = st.sidebar.slider("Sélectionner le pas de temps (Time-Step)", min_value=0, max_value=3, value=0)

current_data = df[df['time_step'] == time_step].iloc[0]

# Affichage des métriques clés
col1, col2, col3, col4 = st.columns(4)
col1.metric("Pression Entrée (Pin)", f"{current_data['Pin']:.2f} bar")
col2.metric("Pression Sortie (Pout)", f"{current_data['Pout']:.2f} bar")
delta_p = current_data['Pin'] - current_data['Pout']
col3.metric("Chute de Pression (ΔP)", f"{delta_p:.2f} bar")
col4.metric("Vitesse Flux (VTSS)", f"{current_data['VTSS']:.2f} m/s")

col_left, col_right = st.columns(2)

# Analyse des données
with col_left:
    st.subheader("📊 Analyse des Capteurs")
    # Graphique ΔP
    fig_p = px.line(df, x='time_step', y=(df['Pin']-df['Pout']), title="Évolution de la Chute de Pression (ΔP)")
    st.plotly_chart(fig_p, use_container_width=True)
    # Graphique Vitesse
    fig_v = px.line(df, x='time_step', y='VTSS', title="Profil de Vitesse du Flux (VTSS)")
    st.plotly_chart(fig_v, use_container_width=True)

# Diagnostic IA
with col_right:
    st.subheader("🧠 Diagnostic de Santé Prédictif (PHM)")
    input_features = np.array([[current_data['Pin'], current_data['Pout'], current_data['VTSS']]])
    status, confidence = predict_anomaly(input_features)
    
    st.write(f"**État Opérationnel :** {status} (Confiance : {confidence*100:.1f}%)")
    
    rul = calculate_rul(delta_p)
    st.info(f"**Durée de vie utile restante (RUL) :** {rul} heures")
    st.progress(max(0, min(int(rul / 120 * 100), 100)))

st.write("---")
st.caption("Développé pour l'optimisation des actifs industriels - Projet OCP.")
