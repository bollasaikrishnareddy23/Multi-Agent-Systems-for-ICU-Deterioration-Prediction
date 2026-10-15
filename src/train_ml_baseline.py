import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


FEATURES = [
    "anchor_age",
    "gender",

    "creatinine_max_24h",
    "creatinine_trend_24h",
    "bun_max_24h",
    "urine_output_24h",
    "dialysis_flag_24h",

    "heart_rate_max_24h",
    "map_min_24h",
    "sbp_min_24h",
    "resp_rate_max_24h",
    "spo2_min_24h",
    "temperature_max_24h",
    "temperature_min_24h",

    "mechanical_ventilation_flag_24h",
    "oxygen_support_flag_24h",
    "fio2_max_24h",
    "peep_max_24h",
]

TARGET = "hospital_expire_flag"


def main():
    input_path = "data/sample_features.csv"
    df = pd.read_csv(input_path)

    df = df.dropna(subset=[TARGET])

    X = df[FEATURES]
    y = df[TARGET].astype(int)

    numeric_features = [c for c in FEATURES if c != "gender"]
    categorical_features = ["gender"]

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features)
        ]
    )

    model = LogisticRegression(max_iter=1000, class_weight="balanced")

    clf = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1": float(f1_score(y_test, y_pred, zero_division=0)),
        "auroc": float(roc_auc_score(y_test, y_prob)),
        "auprc": float(average_precision_score(y_test, y_prob)),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }

    Path("results").mkdir(exist_ok=True)
    with open("results/ml_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
