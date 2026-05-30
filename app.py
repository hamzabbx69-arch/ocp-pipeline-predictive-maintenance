import streamlit as st
import pandas as pd
import numpy as np
from ml_predictive_maintenance import predict_anomaly, calculate_rul

st.set_page_config(page_title="OCP Digital Twin", layout="wide")
st.title("🏭 OCP Jorf Lasfar — Maintenance Prédictive")

df = pd.read_csv("industrial_predictive_maintenance_data.csv")

# Slider
idx = st.sidebar.slider("Sélectionner l'étape", 0, len(df)-1, 0)
row = df.iloc[idx]

# الحسابات (إستعمال الأرقام د الأعمدة 0:Pin, 1:Pout, 2:VTSS)
pin = row[0]
pout = row[1]
vtss = row[2]
delta_p = pin - pout
rul = calculate_rul(delta_p)

# العرض
col1, col2, col3, col4 = st.columns(4)
col1.metric("Pin", f"{pin:.2f} bar")
col2.metric("Pout", f"{pout:.2f} bar")
col3.metric("ΔP", f"{delta_p:.2f} bar")
col4.metric("RUL", f"{rul} Jours")

# الـ ML
status, conf = predict_anomaly(np.array([[pin, pout, vtss]]))
st.write(f"### État : {status} (Confiance: {conf*100:.1f}%)")
