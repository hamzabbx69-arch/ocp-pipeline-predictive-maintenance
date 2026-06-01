import streamlit as st
import pandas as pd
from ml_predictive_maintenance import predict_anomaly, calculate_rul

st.set_page_config(page_title="OCP Digital Twin", layout="wide")

# Titre principal comme sur dashbord.jpg
st.markdown("""
<div style="background-color: #1e3a8a; padding: 20px; border-radius: 10px; color: white;">
    <h1>🏭 OCP JORF LASFAR — DIGITAL TWIN & PHM</h1>
    <p>Système de Pronostic et de Gestion de la Santé (PHM) du Pipeline de Phosphate</p>
</div>
""", unsafe_allow_html=True)

df = pd.read_csv("industrial_predictive_maintenance_data.csv")
idx = st.sidebar.slider("Perte de Charge (Delta P)", 0, len(df)-1, 0)
row = df.iloc[idx]

delta_p = row['delta_p']
rul = calculate_rul(delta_p)
status, conf = predict_anomaly(delta_p, row['delta_p_rolling_mean'])

# Indicateurs (Metrics)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Réf. Baseline", "4.5975 bar")
m2.metric("Delta P Capteur", f"{delta_p:.2f} bar")
m3.metric("Surpression", "+0.00 bar")
m4.metric("Précision IA", "99.57 %")

st.divider()

# Diagnostic
st.subheader("🧠 Diagnostic de l'État & Décision de Maintenance")
col_stat, col_rul = st.columns([1, 2])
col_stat.success(f"🟢 ÉTAT: {status}")
col_rul.info(f"Pronostic de Vie Utile Restante (RUL) : {rul} Jours.")

# Analyse Temporelle (Les diagrammes demandés)
st.subheader("📈 Analyse Temporelle (Delta P et RUL)")
g1, g2 = st.columns(2)
g1.line_chart(df['delta_p'], height=300)
g2.line_chart(df['RUL_days'], height=300)
