# OCP Pipeline Predictive Maintenance — Industrial Digital Twin

An industrial-grade Digital Twin framework designed for OCP Jorf Lasfar, combining Computational Fluid Dynamics (CFD) simulation data with Predictive Analytics to monitor pipeline health, predict cloggings, and prevent pressure-induced failures in real-time.

---

## Overview
Industrial pipelines transporting slurry undergo severe stress, leading to degradation, micro-cloggings, or catastrophic pressure drops. This project establishes a bridge between physical fluid simulations and AI by leveraging OpenFOAM data to train high-fidelity Machine Learning Models, all served through an interactive, production-ready Streamlit Dashboard.

### Key Features
- CFD-to-ML Data Pipeline: Integrates fluid dynamics parameters from OpenFOAM solver sequences.
- Predictive Health Monitoring (PHM): Real-time anomaly detection (Healthy vs. Degraded vs. Critical).
- Industrial SCADA-like UI: A modern dashboard mimicking control-room monitoring systems.

---

## Architecture & Data Flow
1. Physics Layer (OpenFOAM): Simulates multi-phase flow behaviors across distinct operational configurations.
2. Analytics Layer (Python & ML): Evaluates structural anomalies against a strict physical baseline (healthy_baseline.csv).
3. Visualization Layer (Streamlit): Translates model probabilities into clear risk heatmaps and sensor trends.

---

## Repository Structure
- app.py : Streamlit Dashboard Core Application
- ml_predictive_maintenance.py : ML Model Training & Evaluation Logic
- analyze_maintenance.py : Feature Engineering & Delta Analysis
- healthy_baseline.csv : Nominal reference state metrics
- requirements.txt : Python dependencies
- README.md : Project Documentation

---

## Quick Start & Deployment

1. Installation:
   git clone https://github.com/hamzabbx69-arch/ocp-pipeline-predictive-maintenance.git
   cd ocp-pipeline-predictive-maintenance
   pip3 install -r requirements.txt

2. Running the Digital Twin Dashboard:
   python3 -m streamlit run app.py

Open your browser and navigate to http://localhost:8502 to interact with the interface.

---
*Developed as part of an Engineering Initiative for industrial asset optimization.*
