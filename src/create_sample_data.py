import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

n = 300

df = pd.DataFrame({
    "subject_id": np.arange(100000, 100000 + n),
    "hadm_id": np.arange(200000, 200000 + n),
    "stay_id": np.arange(300000, 300000 + n),
    "anchor_age": np.random.randint(18, 90, n),
    "gender": np.random.choice(["M", "F"], n),

    "creatinine_max_24h": np.random.gamma(2.0, 0.8, n),
    "creatinine_first_24h": np.random.gamma(1.8, 0.7, n),
    "creatinine_last_24h": np.random.gamma(2.0, 0.8, n),
    "bun_max_24h": np.random.gamma(4.0, 8.0, n),
    "urine_output_24h": np.random.normal(1200, 600, n).clip(50, 3500),
    "dialysis_flag_24h": np.random.binomial(1, 0.05, n),

    "heart_rate_max_24h": np.random.normal(110, 25, n).clip(50, 220),
    "map_min_24h": np.random.normal(70, 15, n).clip(30, 120),
    "sbp_min_24h": np.random.normal(95, 20, n).clip(50, 160),
    "resp_rate_max_24h": np.random.normal(25, 8, n).clip(10, 60),
    "spo2_min_24h": np.random.normal(93, 5, n).clip(60, 100),
    "temperature_max_24h": np.random.normal(37.7, 0.9, n).clip(35, 42),
    "temperature_min_24h": np.random.normal(36.6, 0.7, n).clip(33, 39),

    "mechanical_ventilation_flag_24h": np.random.binomial(1, 0.30, n),
    "oxygen_support_flag_24h": np.random.binomial(1, 0.50, n),
    "fio2_max_24h": np.random.uniform(0.21, 1.0, n),
    "peep_max_24h": np.random.normal(6, 3, n).clip(0, 20),
})

df["creatinine_trend_24h"] = df["creatinine_last_24h"] - df["creatinine_first_24h"]

# Create a synthetic label correlated with clinical risk.
risk_score = (
    (df["creatinine_max_24h"] >= 2.0).astype(int) * 1.0 +
    (df["urine_output_24h"] < 500).astype(int) * 1.5 +
    (df["map_min_24h"] < 65).astype(int) * 1.5 +
    (df["spo2_min_24h"] < 90).astype(int) * 1.2 +
    (df["mechanical_ventilation_flag_24h"] == 1).astype(int) * 1.0 +
    (df["fio2_max_24h"] >= 0.6).astype(int) * 1.0
)

prob = 1 / (1 + np.exp(-(risk_score - 2.7)))
df["hospital_expire_flag"] = np.random.binomial(1, prob)

Path("data").mkdir(exist_ok=True)
df.to_csv("data/sample_features.csv", index=False)

print("Created data/sample_features.csv")
print(df.head())
