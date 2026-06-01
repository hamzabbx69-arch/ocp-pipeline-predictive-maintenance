import streamlit as st
import pandas as pd
from ml_predictive_maintenance import predict_anomaly, calculate_rul

st.set_page_config(layout="wide")
st.title("🏭 OCP Jorf Lasfar — Maintenance Prédictive")

df = pd.read_csv("industrial_predictive_maintenance_data.csv")
idx = st.sidebar.slider("Étape", 0, len(df)-1, 0)
row = df.iloc[idx]

# Utilisation des colonnes trouvées
delta_p = row['delta_p']
rolling_mean = row['delta_p_rolling_mean']
gradient = row['delta_p_gradient']
rul = calculate_rul(delta_p)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Delta P", f"{delta_p:.2f} bar")
col2.metric("Rolling Mean", f"{rolling_mean:.2f}")
col3.metric("Gradient", f"{gradient:.4f}")
col4.metric("RUL", f"{rul} Jours")
