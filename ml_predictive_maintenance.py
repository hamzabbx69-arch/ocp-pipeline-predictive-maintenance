import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

print("[+] Phase 1: Génération de la Data de Dégradation (Industrial SCADA Simulation)...")

# Fixer la baseline OpenFOAM dyalna
baseline_dp = 4.597485

# Paramètres de la simulation (180 jours, mesure chaque heure)
jours = 180
mesures_par_jour = 24
total_points = jours * mesures_par_jour

time_hours = np.arange(total_points)

# Simulation de la dégradation exponentielle (L'érosion d tuyauterie d OCP)
degradation_rate = 0.00022
noise = np.random.normal(0, 0.15, total_points) 
delta_p_simulated = baseline_dp + 1.2 * np.exp(degradation_rate * time_hours) + noise

# Seuil Critique de sécurité d la panne
failure_threshold = 11.5
failure_indices = np.where(delta_p_simulated >= failure_threshold)[0]

if len(failure_indices) > 0:
    failure_time = failure_indices[0]
else:
    failure_time = total_points - 1

print(f"[+] Pipe failure simulated at hour: {failure_time} ({failure_time // 24} days)")

# Tronquer la data
time_hours = time_hours[:failure_time]
delta_p_simulated = delta_p_simulated[:failure_time]

# Calcul de la Target: RUL (Remaining Useful Life) en jours
rul_days = (failure_time - time_hours) / 24.0

# DataFrame Pandas
df = pd.DataFrame({
    'timestamp_hours': time_hours,
    'delta_p': delta_p_simulated,
    'RUL_days': rul_days
})

print("\n[+] Phase 2: Feature Engineering (Calcul des indicateurs glissants)...")
df['delta_p_rolling_mean'] = df['delta_p'].rolling(window=24, min_periods=1).mean()
df['delta_p_gradient'] = np.gradient(df['delta_p_rolling_mean'])

print("\n[+] Phase 3: Préparation des données pour le Machine Learning...")
X = df[['delta_p', 'delta_p_rolling_mean', 'delta_p_gradient']]
y = df['RUL_days']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\n[+] Phase 4: Entraînement du Modèle d'IA (Random Forest Regressor)...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("-" * 50)
print(f"[>] MODEL PERFORMANCE RESULTS:")
print(f"    - Mean Absolute Error (MAE): {mae:.3f} Days")
print(f"    - R2 Score (Accuracy): {r2 * 100:.2f}%")
print("-" * 50)

df.to_csv("industrial_predictive_maintenance_data.csv", index=False)
print("[+] Le dataset a été sauvegardé dans 'industrial_predictive_maintenance_data.csv'!")
