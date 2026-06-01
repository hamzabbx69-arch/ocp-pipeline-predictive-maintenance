def calculate_rul(delta_p):
    # Logique simple pour le calcul de la RUL
    return max(0, 200 - int(delta_p * 10))

def predict_anomaly(delta_p, rolling_mean):
    # Version corrigée acceptant 2 arguments
    if delta_p > 10:
        return "Critical", 0.99
    elif delta_p > 7:
        return "Warning", 0.85
    else:
        return "Healthy", 0.95
