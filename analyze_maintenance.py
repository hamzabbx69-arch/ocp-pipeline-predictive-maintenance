import os

# Path d l-fichier text dyal l-capteurs li creeh OpenFOAM
data_file = "postProcessing/capteursPression/0/p"

if not os.path.exists(data_file):
    print("[-] Error: Fichier d les capteurs mal9nahch! Check postProcessing/")
    exit()

print("[+] Processing OpenFOAM Data for Predictive Maintenance...")

times = []
p_inlet = []
p_outlet = []
delta_p = []

# 9rayat l-fichier line b line o t-7yad d l-comments (#)
with open(data_file, 'r') as f:
    for line in f:
        if line.startswith('#') or not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 3:
            t = float(parts[0])
            p1 = float(parts[1]) # Capteur d l-entrée (Inlet)
            p2 = float(parts[2]) # Capteur d la sortie (Outlet)
            dp = p1 - p2         # Perte de charge (Delta P)
            
            times.append(t)
            p_inlet.append(p1)
            p_outlet.append(p2)
            delta_p.append(dp)

# Affichage d les résultats techniques d la baseline
print(f"\n[+] Total Data Points Collected: {len(times)}")
print(f"[+] Initial Delta P: {delta_p[0]:.6f}")
print(f"[+] Final Delta P (Healthy State Baseline): {delta_p[-1]:.6f}")

# Sauvegarde d l-data f un fichier CSV structured professional
csv_file = "healthy_baseline.csv"
with open(csv_file, 'w') as out:
    out.write("time,p_inlet,p_outlet,delta_p\n")
    for i in range(len(times)):
        out.write(f"{times[i]},{p_inlet[i]},{p_outlet[i]},{delta_p[i]}\n")

print(f"\n[+] Succès: Data d la baseline t-sauvegarda f '{csv_file}'!")
