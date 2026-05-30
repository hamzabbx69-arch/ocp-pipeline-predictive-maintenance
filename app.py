import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ml_predictive_maintenance import predict_anomaly, calculate_rul

st.set_page_config(page_title="OCP Digital Twin", layout="wide")
st.title("🏭 OCP Jorf Lasfar — Pipeline Predictive Maintenance")

# تحميل الداتا
df = pd.read_csv("industrial_predictive_maintenance_data.csv")

# --- Debugging: هاد السطر غيورينا سميات الأعمدة فـ الباج د السيت ---
st.write("### Debug: Colonnes trouvées dans le CSV:")
st.write(df.columns.tolist())

# نختارو صف واحد بـ index (بلا ما نعتامدو على 'time_step')
st.sidebar.header("🎛️ Contrôle")
idx = st.sidebar.slider("Sélectionner l'étape", min_value=0, max_value=len(df)-1, value=0)
current_data = df.iloc[idx]

# العرض (بـ إستعمال الأسامي اللي غتخرج لينا ف الـ Debug)
# إذا طلع ليك خطأ هنا، يعني السمية ف الـ CSV فيها شي فراغ أو ختلاف
st.write("Données de la ligne sélectionnée:")
st.write(current_data)
