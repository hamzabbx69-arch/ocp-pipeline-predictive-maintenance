import streamlit as st
import pandas as pd
from ml_predictive_maintenance import predict_anomaly, calculate_rul

st.set_page_config(page_title="OCP Digital Twin", layout="wide")

# Titre avec style professionnel
st.markdown("""
    <h1 style='text-align: center; color: #2e7d32;'>🏭 OCP Jorf Lasfar — Digital Twin & PHM</h1>
    <hr>
""", unsafe_allow_html=True)

df = pd.read_csv("industrial_predictive_maintenance_data.csv")

# Sidebar stylée
st.sidebar.header("🛠 Configuration")
idx = st.sidebar.slider("Perte de Charge (Delta P)", 0, len(df)-1, 0)
row = df.iloc[idx]

# Calculs
delta_p = row['delta_p']
rul = calculate_rul(delta_p)
status, _ = predict_anomaly(delta_p, row['delta_p_rolling_mean'])

# Bloc des métriques (Ligne du haut)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Réf. Baseline", "4.60 bar")
col2.metric("Delta P Actuel", f"{delta_p:.2f} bar")
col3.metric("Surpression", "0.00 bar")
col4.metric("Précision IA", "99.57 %")

st.markdown("<br>", unsafe_allow_html=True)

# Bloc Diagnostic structuré
with st.container():
    st.subheader("🧠 Diagnostic de l'État & Décision")
    c_diag1, c_diag2 = st.columns(2)
    c_diag1.success(f"🟢 État: {status}")
    c_diag2.info(f"📅 RUL Estimée: {rul} Jours")

st.markdown("<br>", unsafe_allow_html=True)

# Analyse Temporelle (Les graphiques)
st.subheader("📈 Analyse Temporelle (Données Historiques)")
g1, g2 = st.columns(2)
g1.line_chart(df['delta_p'])
g2.line_chart(df['RUL_days'])
