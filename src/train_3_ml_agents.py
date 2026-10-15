import json
from pathlib import Path

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


TARGET = "hospital_expire_flag"

KIDNEY_FEATURES = [
    "creatinine_max_24h",
    "creatinine_trend_24h",
    "bun_max_24h",
    "urine_output_24h",
    "dialysis_flag_24h",
]

VITAL_FEATURES = [
    "heart_rate_max_24h",
    "map_min_24h",
    "sbp_min_24h",
    "resp_rate_max_24h",
    "spo2_min_24h",
    "temperature_max_24h",
    "temperature_min_24h",
]

VENT_FEATURES = [
    "mechanical_ventilation_flag_24h",
    "oxygen_support_flag_24h",
    "fio2_max_24h",
    "peep_max_24h",
]


def build_model():
    return Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])


def risk_class(prob):
    if prob >= 0.70:
        return "high"
    elif prob >= 0.30:
        return "medium"
    else:
        return "low"


def main():
    input_path = "data/sample_features.csv"
    df = pd.read_csv(input_path).dropna(subset=[TARGET])

    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=42,
        stratify=df[TARGET].astype(int)
    )

    y_train = train_df[TARGET].astype(int)
    y_test = test_df[TARGET].astype(int)

    agents = {
        "kidney": KIDNEY_FEATURES,
        "vital": VITAL_FEATURES,
        "ventilation": VENT_FEATURES
    }

    results = {}
    supervisor_train = pd.DataFrame(index=train_df.index)
    supervisor_test = pd.DataFrame(index=test_df.index)

    for name, features in agents.items():
        model = build_model()
        model.fit(train_df[features], y_train)

        train_prob = model.predict_proba(train_df[features])[:, 1]
        test_prob = model.predict_proba(test_df[features])[:, 1]

        supervisor_train[f"{name}_prob"] = train_prob
        supervisor_test[f"{name}_prob"] = test_prob

        results[f"{name}_auroc"] = float(roc_auc_score(y_test, test_prob))
        results[f"{name}_auprc"] = float(average_precision_score(y_test, test_prob))

    supervisor = build_model()
    supervisor.fit(supervisor_train, y_train)

    supervisor_prob = supervisor.predict_proba(supervisor_test)[:, 1]

    results["supervisor_auroc"] = float(roc_auc_score(y_test, supervisor_prob))
    results["supervisor_auprc"] = float(average_precision_score(y_test, supervisor_prob))

    output = test_df[["subject_id", "hadm_id", "stay_id", TARGET]].copy()
    output["kidney_prob"] = supervisor_test["kidney_prob"].values
    output["vital_prob"] = supervisor_test["vital_prob"].values
    output["ventilation_prob"] = supervisor_test["ventilation_prob"].values
    output["supervisor_prob"] = supervisor_prob
    output["supervisor_risk"] = [risk_class(p) for p in supervisor_prob]

    Path("results").mkdir(exist_ok=True)
    output.to_csv("results/three_ml_agent_predictions.csv", index=False)

    with open("results/three_ml_agent_metrics.json", "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))
    print("Saved results/three_ml_agent_predictions.csv")


if __name__ == "__main__":
    main()
