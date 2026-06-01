import streamlit as st
import pandas as pd

# Configuration page
st.set_page_config(page_title="OCP Dashboard Pro", layout="wide")

# Header Industriel
st.markdown("""
    <div style="background-color: #0f172a; padding: 25px; border-radius: 10px; color: white;">
        <h1 style="margin: 0;">🏭 OCP JORF LASFAR — DIGITAL TWIN & PHM</h1>
        <p style="margin: 0; opacity: 0.8;">Système de Pronostic et de Gestion de la Santé du Pipeline</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# Chargement données
df = pd.read_csv("industrial_predictive_maintenance_data.csv")

# Sidebar
st.sidebar.header("🛠 Configuration SCADA")
idx = st.sidebar.slider("Simulation Pression (Delta P)", 0, len(df)-1, 0)
row = df.iloc[idx]

# Données
delta_p = row['delta_p']
rul = row['RUL_days']
rolling_mean = row['delta_p_rolling_mean']
gradient = row['delta_p_gradient']

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Delta P Actuel", f"{delta_p:.2f} bar")
c2.metric("RUL Estimée", f"{int(rul)} Jours")
c3.metric("Rolling Mean", f"{rolling_mean:.2f}")
c4.metric("Gradient", f"{gradient:.4f}")

# Diagnostic Dynamique
if delta_p > 8:
    color, status = "#ef4444", "CRITICAL - MAINTENANCE IMMÉDIATE"
elif delta_p > 6.5:
    color, status = "#f59e0b", "WARNING - SURVEILLANCE REQUISE"
else:
    color, status = "#22c55e", "HEALTHY - ÉTAT NOMINAL"

st.markdown(f"""
    <div style="background-color: {color}; padding: 15px; border-radius: 8px; color: white; text-align: center;">
        <h2 style="margin:0;">STATUT SYSTÈME : {status}</h2>
    </div>
""", unsafe_allow_html=True)

# Analyse
st.markdown("<br><h3>📈 Analyse Temporelle</h3>", unsafe_allow_html=True)
g1, g2 = st.columns(2)
with g1:
    st.subheader("Courbe de Pression (Delta P)")
    st.line_chart(df['delta_p'])
with g2:
    st.subheader("Prédiction Vie Utile (RUL)")
    st.line_chart(df['RUL_days'])
