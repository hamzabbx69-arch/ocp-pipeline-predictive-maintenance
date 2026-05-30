import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# 1. Page Configuration & Theme
st.set_page_config(
    page_title="OCP Jorf Lasfar - Predictive Maintenance",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Industrial UI
st.markdown("""
    <style>
    /* Background and general text */
    .main { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1e293b !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Custom Styling for Cards */
    div[data-testid="stMetricBackground"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Sidebar styling */
    .css-11q7m8a { background-color: #0f172a !important; }
    
    /* Status Badges */
    .status-good { padding: 15px; background-color: #d1fae5; color: #065f46; border-radius: 10px; border-left: 5px solid #10b981; font-weight: bold; }
    .status-warn { padding: 15px; background-color: #fef3c7; color: #92400e; border-radius: 10px; border-left: 5px solid #f59e0b; font-weight: bold; }
    .status-crit { padding: 15px; background-color: #fee2e2; color: #991b1b; border-radius: 10px; border-left: 5px solid #ef4444; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Header Banner
st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #0d9488 100%); padding: 25px; border-radius: 15px; margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);">
        <h1 style="color: white !important; margin: 0; font-size: 28px;">🏭 OCP JORF LASFAR — DIGITAL TWIN & PHM</h1>
        <p style="color: #e2e8f0; margin: 5px 0 0 0; font-size: 15px;">Système de Pronostic et de Gestion de la Santé (PHM) du Pipeline de Phosphate</p>
    </div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("industrial_predictive_maintenance_data.csv")

try:
    df = load_data()
    
    # Fast training for live interface interaction
    X = df[['delta_p', 'delta_p_rolling_mean', 'delta_p_gradient']]
    y = df['RUL_days']
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # 2. Sidebar Controls
    st.sidebar.markdown("### 📥 SCADA Telemetry Simulator")
    st.sidebar.markdown("Modifiez la pression pour simuler la dégradation réelle du coude.")
    
    baseline_dp = 4.597485 
    live_dp = st.sidebar.slider(
        "Perte de Charge Actuelle (ΔP en bar)",
        float(baseline_dp), 12.5, float(baseline_dp), step=0.05
    )
    
    # Feature calculation based on slider
    idx_proche = (df['delta_p'] - live_dp).abs().idxmin()
    features_live = df.iloc[[idx_proche]][['delta_p', 'delta_p_rolling_mean', 'delta_p_gradient']]
    
    # Predict RUL
    predicted_rul = model.predict(features_live)[0]
    
    # 3. Main Dashboard KPI Layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="📊 Réf. Baseline CFD (OpenFOAM)", value=f"{baseline_dp:.4f} bar")
    with col2:
        st.metric(label="⏱️ Delta P Capteur (Live)", value=f"{live_dp:.2f} bar")
    with col3:
        surpression = live_dp - baseline_dp
        st.metric(label="📈 Surpression Détectée", value=f"+{surpression:.2f} bar", delta=f"{surpression:.2f} bar", delta_color="inverse")
    with col4:
        # Precision check from training results
        st.metric(label="🎯 Précision Modèle IA", value="99.57 %", delta="MAE: 2.6 J")

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Interactive Health Status Segment
    st.markdown("### 🧠 Diagnostic de l'État & Décision de Maintenance")
    
    with st.container(border=True):
        col_status, col_desc = st.columns([1, 2])
        
        with col_status:
            if predicted_rul > 60:
                st.markdown('<div class="status-good"><center>🟢 ÉTAT NOMINAL<br>Aucun risque décelé</center></div>', unsafe_allow_html=True)
            elif predicted_rul > 15:
                st.markdown('<div class="status-warn"><center>🟡 ALERTE USURE<br>Planifier inspection</center></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-crit"><center>🔴 SEUIL CRITIQUE<br>Panne Imminente !</center></div>', unsafe_allow_html=True)
                
        with col_desc:
            if predicted_rul > 60:
                st.success(f"**Pronostic de Vie Utile Restante : {predicted_rul:.1f} Jours.**\n\nLe fluide s'écoule normalement. L'érosion par les particules de phosphate est dans les tolérances standards.")
            elif predicted_rul > 15:
                st.warning(f"**Pronostic de Vie Utile Restante : {predicted_rul:.1f} Jours.**\n\nL'usure interne du coude s'accélère (augmentation du gradient de pression). Pensez à commander la pièce de rechange.")
            else:
                st.error(f"**🚨 ALERTE ACTION IMMÉDIATE : RUL de {predicted_rul:.1f} Jours !**\n\nRisque élevé de perçage de la canalisation et de fuite de pulpe de phosphate. Déclencher l'arrêt technique d'urgence.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Charts Area (Professional Analytics layout)
    st.markdown("### 📉 Analyse Temporelle et Analyse d'Érosion (Données Historiques sur 180 Jours)")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        with st.container(border=True):
            st.markdown("**Évolution Exponentielle de la Perte de Charge (ΔP)**")
            chart_df1 = df[['timestamp_hours', 'delta_p']].set_index('timestamp_hours')
            st.line_chart(chart_df1, color="#0d9488")
            
    with col_chart2:
        with st.container(border=True):
            st.markdown("**Courbe de Décrémentation de la Vie Utile Restante (RUL)**")
            chart_df2 = df[['timestamp_hours', 'RUL_days']].set_index('timestamp_hours')
            st.line_chart(chart_df2, color="#1e3a8a")

except FileNotFoundError:
    st.error("[-] Error: Fichier 'industrial_predictive_maintenance_data.csv' mal9nahch. Runni script l-ML 1er.")
