# Exact Project Steps

## Phase 1: Access and setup

1. Create a PhysioNet account.
2. Complete required training.
3. Request access to MIMIC-IV.
4. Request BigQuery access.
5. Create a Google Cloud project.
6. Open BigQuery.
7. Confirm you can see:
   - `physionet-data.mimiciv_v3_1_hosp`
   - `physionet-data.mimiciv_v3_1_icu`

## Phase 2: Create cohort

Run:

```text
sql/01_create_cohort_bigquery.sql
```

This creates:

```text
your_project.your_dataset.cohort_icu_24h
```

## Phase 3: Create features

Run:

```text
sql/02_create_features_bigquery.sql
```

This creates:

```text
your_project.your_dataset.features_24h_3_agents
```

## Phase 4: Export CSV

Export the BigQuery table to CSV and save it locally as:

```text
data/mimic_features.csv
```

## Phase 5: Run rule-based agents

Edit:

```text
src/run_rule_based_agents.py
```

Change:

```python
input_path = "data/sample_features.csv"
```

to:

```python
input_path = "data/mimic_features.csv"
```

Then run:

```bash
python src/run_rule_based_agents.py
```

## Phase 6: Train ML baseline

Edit:

```text
src/train_ml_baseline.py
```

Change input path to:

```python
input_path = "data/mimic_features.csv"
```

Then run:

```bash
python src/train_ml_baseline.py
```

## Phase 7: Train 3 ML agents

Edit:

```text
src/train_3_ml_agents.py
```

Change input path to:

```python
input_path = "data/mimic_features.csv"
```

Then run:

```bash
python src/train_3_ml_agents.py
```

## Phase 8: Write report

Use this title:

```text
Explainable Multi-Agent ICU Deterioration Prediction Using MIMIC-IV
```

Use these sections:

1. Introduction
2. Dataset
3. Cohort selection
4. Feature extraction
5. Proposed 3-agent system
6. Supervisor agent
7. Experiments
8. Results
9. Discussion
10. Limitations
11. Conclusion
