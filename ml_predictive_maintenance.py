import numpy as np
import pandas as pd

# --- Les fonctions nécessaires pour l'interface ---
def predict_anomaly(input_features):
    # Logique simple pour le diagnostic basé sur le Delta P (input_features[0][2] = delta_p)
    delta_p = input_features[0][0] - input_features[0][1]
    if delta_p < 6.0:
        return "Healthy", 0.98
    elif delta_p < 10.0:
        return "Degraded", 0.85
    else:
        return "Critical", 0.99

def calculate_rul(delta_p):
    # Calcul simplifié du RUL basé sur le seuil critique (11.5 bar)
    failure_threshold = 11.5
    remaining = failure_threshold - delta_p
    return max(0, int(remaining * 10))

# --- Ton code de simulation existant ---
baseline_dp = 4.597485
# ... (باقي الكود ديالك كيبقى ف الملف)
