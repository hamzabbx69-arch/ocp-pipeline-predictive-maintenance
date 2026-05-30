# 🏭 OCP Jorf Lasfar — Pipeline Predictive Maintenance (Digital Twin)

📊 **Un Système de Pronostic et de Gestion de la Santé (PHM) hybride combinant la simulation CFD (OpenFOAM) et l'Intelligence Artificielle (Machine Learning) pour prédire l'érosion des conduites de phosphate.**

---

## 🚀 Aperçu du Projet

Dans les installations industrielles de l'**OCP Jorf Lasfar**, le transport de la pulpe de phosphate à travers les pipelines provoque une érosion sévère par impact particulaire, en particulier au niveau des coudes de tuyauterie. 

Ce projet implémente un **Jumeau Numérique (Digital Twin)** capable de :
1. Établir une baseline hydrodynamique via une simulation CFD.
2. Générer un dataset de dégradation basé sur des lois d'usure physiques.
3. Entraîner un modèle de Machine Learning pour prédire le **RUL (Remaining Useful Life)**.
4. Fournir une **Interface HMI/SCADA Interactive** pour assister les opérateurs dans la prise de décision.

---

## 🛠️ Technologies Utilisées

* **Simulation Numérique :** OpenFOAM (v2406) — Résolution des équations de Navier-Stokes pour obtenir la perte de charge (Delta P).
* **Langage & Data Science :** Python 3.12, Pandas, NumPy.
* **Machine Learning :** Scikit-Learn (Random Forest Regressor).
* **Interface Graphique :** Streamlit Framework (UI/UX Industrielle Premium).

---

## 📐 Architecture du Pipeline (Data Flow)

```
[ OpenFOAM CFD ] ──> Extraction de la Baseline (Delta P) ──> [ 1500 Data Points ]
                                                               │
                                                               ▼
[ Streamlit UI ] <── Prédiction en Temps Réel <── [ Modèle Random Forest ]
```

---

## 🎯 Performances du Modèle d'IA

Le modèle de régression basé sur l'algorithme **Random Forest** a été entraîné après une phase de *Feature Engineering* (calcul de moyennes mobiles et de gradients de pression). Les résultats obtenus sont extrêmement précis :

* **R2 Score (Précision globale) :** 99.57 %
* **Mean Absolute Error (MAE) :** 2.624 Jours

> ℹ️ **Impact Industriel :** Une erreur moyenne de seulement ~2.6 jours sur un cycle d'usure de 180 jours permet une planification chirurgicale des arrêts techniques à Jorf Lasfar, évitant ainsi les pannes catastrophiques en pleine production.

---

## 📦 Installation et Utilisation

### 1. Clonage du Projet
```bash
git clone https://github.com/votre-username/ocp-pipeline-predictive-maintenance.git
cd ocp-pipeline-predictive-maintenance
```

### 2. Installation des Dépendances
```bash
pip3 install -r requirements.txt
```

### 3. Génération des Données et Entraînement
```bash
python3 src/ml_predictive_maintenance.py
```

### 4. Lancement du Dashboard Interactif
```bash
python3 -m streamlit run src/app.py
```
Ouvrez ensuite votre navigateur sur `http://localhost:8501` pour interagir avec le Jumeau Numérique.
