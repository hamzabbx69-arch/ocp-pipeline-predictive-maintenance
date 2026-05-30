import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ml_predictive_maintenance import predict_anomaly, calculate_rul

st.set_page_config(page_title="OCP Digital Twin", layout="wide")
st.title("🏭 OCP Jorf Lasfar — Pipeline Predictive Maintenance")

# تحميل الداتا
df = pd.read_csv("industrial_predictive_maintenance_data.csv")

# إذا كان الـ CSV مافيهش 'time_step'، غنستعملو index ديال الصفوف مباشرة
# هاد الطريقة مضمونة ومكتعتمدش على سمية العمود
st.sidebar.header("🎛️ Contrôle")
idx = st.sidebar.slider("Sélectionner l'étape (Time-Step)", min_value=0, max_value=len(df)-1, value=0)
current_data = df.iloc[idx]

# العرض
col1, col2, col3, col4 = st.columns(4)
col1.metric("Pin", f"{current_data['Pin']:.2f} bar")
col2.metric("Pout", f"{current_data['Pout']:.2f} bar")
delta_p = current_data['Pin'] - current_data['Pout']
col3.metric("ΔP", f"{delta_p:.2f} bar")
col4.metric("VTSS", f"{current_data['VTSS']:.2f} m/s")

# الـ ML
input_features = np.array([[current_data['Pin'], current_data['Pout'], current_data['VTSS']]])
status, confidence = predict_anomaly(input_features)
st.write(f"### Diagnostic: {status} ({confidence*100:.1f}%)")
