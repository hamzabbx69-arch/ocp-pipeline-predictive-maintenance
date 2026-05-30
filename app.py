import streamlit as st
import pandas as pd
import numpy as np
from ml_predictive_maintenance import predict_anomaly

st.title("OCP Digital Twin")

# تحميل الداتا
df = pd.read_csv("industrial_predictive_maintenance_data.csv")

# عرض أول 3 أعمدة (بلاصت ما نكتبو السميات)
idx = st.slider("Étape", 0, len(df)-1, 0)
row = df.iloc[idx]

# العرض (بإستعمال الأرقام ديال الأعمدة 0, 1, 2)
st.metric("Pin", f"{row[0]:.2f} bar")
st.metric("Pout", f"{row[1]:.2f} bar")
st.metric("VTSS", f"{row[2]:.2f} m/s")

# الموديل
status, _ = predict_anomaly(np.array([[row[0], row[1], row[2]]]))
st.write(f"### État: {status}")
