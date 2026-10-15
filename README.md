# Multi-Agent Systems for ICU Deterioration Prediction

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn](https://img.shields.io/badge/library-scikit--learn-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bollasaikrishnareddy23/Multi-Agent-Systems-for-ICU-Deterioration-Prediction/blob/main/Copy_of_Multi_Agent_Project.ipynb)

A modular, clinically interpretable multi-agent artificial intelligence framework designed to predict in-hospital patient deterioration (mortality) during the initial 24 hours of Intensive Care Unit (ICU) admission.

---

## 📌 Project Architecture

Traditional clinical machine learning models operate as monolithic black boxes. This system divides patient monitoring into domain-specific clinical agents, each responsible for specialized pathophysiological organ indicators, coordinated by an ensemble supervisor agent:

                  Raw ICU Time-Series Data (24h)
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
         ┌────────────┐  ┌────────────┐  ┌────────────┐
         │   Kidney   │  │   Vital    │  │Ventilation │
         │   Agent    │  │   Signs    │  │   Agent    │
         └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
               │               │               │
               └───────────────┼───────────────┘
                               ▼
                   ┌──────────────────────┐
                   │   Supervisor Agent   │
                   └──────────┬───────────┘
                              ▼
               Final Risk Score & Explanation

### Specialized Clinical Agents
- **Kidney Failure Agent**: Evaluates renal perfusion and acute kidney injury risk using serum creatinine trajectory, blood urea nitrogen (BUN), and cumulative urine output.
- **Vital Signs Agent**: Tracks hemodynamic stability through continuous heart rate, mean arterial pressure (MAP), systolic blood pressure (SBP), respiratory rate, and body temperature.
- **Mechanical Ventilation Agent**: Assesses pulmonary decompensation based on mechanical ventilation status and elevated fraction of inspired oxygen (FiO2) requirements.
- **Supervisor Agent**: Aggregates risk signals from all three agents using both rule-based decision logic and a stacking classifier to deliver calibrated risk probabilities and natural-language explanations.

---

## 📊 Experimental Results

Evaluated on 4,000 patient records from the **PhysioNet 2012 Challenge Dataset** (in-hospital mortality task):

### 1. Overall System Comparison

| Model Architecture | Accuracy | Precision | Recall | F1-Score | AUROC | AUPRC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rule-Based 3-Agent System** | 0.4128 | 0.1677 | **0.8177** | 0.2783 | — | — |
| **Monolithic Baseline (Logistic Regression)** | 0.7175 | **0.2909** | 0.7207 | **0.4145** | **0.7659** | **0.2915** |
| **3 ML Agents + Supervisor Stacking** | **0.7188** | 0.2889 | 0.7027 | 0.4094 | 0.7439 | 0.2841 |

### 2. Individual ML Agent Performance

| Clinical Agent | AUROC | AUPRC | Primary Clinical Features |
| :--- | :---: | :---: | :--- |
| **Kidney Failure Agent** | **0.7279** | **0.2720** | Creatinine (min/max/mean/trend), BUN, Urine output |
| **Vital Signs Agent** | 0.6037 | 0.1823 | HR, MAP, SBP, DBP, Temp, SpO2, RespRate |
| **Mechanical Ventilation Agent** | 0.5845 | 0.1805 | MechVent status, FiO2 max/mean/trend |
| **Supervisor Meta-Classifier** | **0.7439** | **0.2841** | Ensemble probability aggregation |

---

## 📂 Repository Structure

```text
├── sql/
│   ├── 01_create_cohort_bigquery.sql     # Cohort definition & extraction logic
│   └── 02_create_features_bigquery.sql   # SQL-based 24h feature aggregation
├── src/
│   ├── agents/
│   │   ├── kidney_failure_agent.py       # Renal evaluation logic
│   │   ├── vital_signs_agent.py          # Hemodynamic assessment logic
│   │   ├── mechanical_ventilation_agent.py # Respiratory intervention logic
│   │   └── supervisor_agent.py           # Multi-agent coordinator
│   ├── create_sample_data.py             # Synthetic patient generation for testing
│   ├── run_rule_based_agents.py          # Rule-based pipeline execution
│   ├── train_ml_baseline.py              # Monolithic baseline training
│   └── train_3_ml_agents.py              # Distributed agent model training
├── Copy_of_Multi_Agent_Project.ipynb     # Complete end-to-end execution notebook
├── PROJECT_STEPS.md                      # Detailed step-by-step project guide
├── requirements.txt                      # Environment dependencies
└── README.md
```

---

## 🚀 Quickstart

### 1. Clone & Set Up Environment
```bash
git clone [https://github.com/bollasaikrishnareddy23/Multi-Agent-Systems-for-ICU-Deterioration-Prediction.git](https://github.com/bollasaikrishnareddy23/Multi-Agent-Systems-for-ICU-Deterioration-Prediction.git)
cd Multi-Agent-Systems-for-ICU-Deterioration-Prediction
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Pipeline
```bash
# Generate sample test data
python src/create_sample_data.py

# Run rule-based multi-agent pipeline
python src/run_rule_based_agents.py

# Train baseline and multi-agent stacking models
python src/train_ml_baseline.py
python src/train_3_ml_agents.py
```

---

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **Data Engineering**: Pandas, NumPy, Google Cloud BigQuery
- **Machine Learning**: Scikit-Learn, XGBoost
- **Evaluation**: AUROC, AUPRC, Stratified K-Fold cross-validation
