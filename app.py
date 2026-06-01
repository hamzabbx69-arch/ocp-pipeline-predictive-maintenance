import streamlit as st
import pandas as pd

# Configuration page
st.set_page_config(page_title="OCP Digital Twin", layout="wide")

# Titre professionnel
st.markdown("<h1 style='text-align: center;'>🏭 OCP Jorf Lasfar — Maintenance Prédictive</h1>", unsafe_allow_html=True)

# Chargement données
df = pd.read_csv("industrial_predictive_maintenance_data.csv")

# Sidebar
st.sidebar.header("Configuration")
idx = st.sidebar.slider("Étape (Simulation)", 0, len(df)-1, 0)
row = df.iloc[idx]

# Valeurs réelles de ton fichier
delta_p = row['delta_p']
rolling_mean = row['delta_p_rolling_mean']
gradient = row['delta_p_gradient']
rul = row['RUL_days']

# Logique de couleur dynamique
if delta_p > 8:
    color = "red"
    status = "CRITICAL - MAINTENANCE REQUISE"
elif delta_p > 6.5:
    color = "orange"
    status = "WARNING - SURVEILLANCE"
else:
    color = "green"
    status = "HEALTHY - NOMINAL"

# Affichage métriques avec couleurs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Delta P", f"{delta_p:.2f} bar")
col2.metric("Rolling Mean", f"{rolling_mean:.2f}")
col3.metric("Gradient", f"{gradient:.4f}")
col4.metric("RUL", f"{rul} Jours")

# Affichage état stylisé
st.markdown(f"""
<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 10px solid {color};">
    <h2 style="color: {color};">État actuel : {status}</h2>
</div>
""", unsafe_allow_html=True)

st.divider()

# Graphiques
c1, c2 = st.columns(2)
with c1:
    st.subheader("Évolution du Delta P")
    st.line_chart(df['delta_p'])
with c2:
    st.subheader("Évolution du RUL (Jours)")
    st.line_chart(df['RUL_days'])
