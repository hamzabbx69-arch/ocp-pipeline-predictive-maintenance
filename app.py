import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ml_predictive_maintenance import predict_anomaly, calculate_rul

st.set_page_config(page_title="OCP Pipeline Digital Twin", layout="wide")

st.title("🏭 OCP Jorf Lasfar — Pipeline Predictive Maintenance")
st.markdown("### 🌐 Industrial Digital Twin Framework (OpenFOAM & Machine Learning)")
st.write("---")

# Load compiled industrial dataset
df = pd.read_csv("industrial_predictive_maintenance_data.csv")

# Sidebar - Real-time Simulation Controls
st.sidebar.header("🎛️ Simulation Time-Step Control")
time_step = st.sidebar.slider("Select OpenFOAM Mesh Time-Step Sequence", min_value=0, max_value=3, value=0)

# Filter data based on selected configuration
current_data = df[df['time_step'] == time_step].iloc[0]

# Metrics Display
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Inlet Pressure (Pin)", value=f"{current_data['Pin']:.2f} bar")
with col2:
    st.metric(label="Outlet Pressure (Pout)", value=f"{current_data['Pout']:.2f} bar")
with col3:
    delta_p = current_data['Pin'] - current_data['Pout']
    st.metric(label="Pressure Drop (ΔP)", value=f"{delta_p:.2f} bar", delta=f"{delta_p - 1.2:.2f} bar vs Baseline")
with col4:
    st.metric(label="Flow Velocity (VTSS)", value=f"{current_data['VTSS']:.2f} m/s")

st.write("---")

# Analytics & AI Diagnostics
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Real-Time Sensor Diagnostics")
    
    # 1. Delta P Diagram
    fig_p = px.line(df, x='time_step', y=(df['Pin'] - df['Pout']), title="Pressure Drop (ΔP) Trend Analysis", labels={'y': 'ΔP (bar)', 'time_step': 'Time-Step'})
    fig_p.add_scatter(x=[time_step], y=[delta_p], mode='markers', marker=dict(size=12, color='red'), name='Current State')
    st.plotly_chart(fig_p, use_container_width=True)
    
    # 2. VTSS (Velocity) Diagram
    fig_v = px.line(df, x='time_step', y='VTSS', title="Flow Velocity (VTSS) Profile", labels={'VTSS': 'Velocity (m/s)', 'time_step': 'Time-Step'})
    fig_v.add_scatter(x=[time_step], y=[current_data['VTSS']], mode='markers', marker=dict(size=12, color='blue'), name='Current Velocity')
    st.plotly_chart(fig_v, use_container_width=True)

with col_right:
    st.subheader("🧠 Predictive Health Monitoring (PHM)")
    
    # AI Prediction Core
    input_features = np.array([[current_data['Pin'], current_data['Pout'], current_data['VTSS']]])
    status, confidence = predict_anomaly(input_features)
    
    if status == "Healthy":
        st.success(f"✅ Operational Status: HEALTHY ({confidence*100:.1f}% Confidence)")
    elif status == "Degraded":
        st.warning(f"⚠️ Operational Status: DEGRADED (Micro-Clogging Detected) ({confidence*100:.1f}% Confidence)")
    else:
        st.error(f"🚨 Operational Status: CRITICAL FAILURE / CLOGGING ({confidence*100:.1f}% Confidence)")
        
    # Remaining Useful Life (RUL) Prognostics
    rul_hours = calculate_rul(delta_p)
    st.markdown("### ⏳ Remaining Useful Life Prognostic")
    st.info(f"**Estimated RUL:** {rul_hours} Hours remaining before absolute clogging threshold.")
    st.progress(max(0, min(int(rul_hours / 120 * 100), 100)))

st.write("---")
st.caption("Developed as an Advanced Engineering Tool for OCP Industrial Slurry Asset Optimization.")
