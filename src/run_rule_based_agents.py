import sys
import json
from pathlib import Path

import pandas as pd

# Allow imports when running as a script.
sys.path.append(str(Path(__file__).resolve().parent))

from agents.kidney_failure_agent import kidney_failure_agent
from agents.vital_signs_agent import vital_signs_agent
from agents.mechanical_ventilation_agent import mechanical_ventilation_agent
from agents.supervisor_agent import supervisor_agent


def clean_value(value):
    if pd.isna(value):
        return None
    return value


def row_to_dict(row):
    return {col: clean_value(row[col]) for col in row.index}


def run_prediction(row_dict):
    kidney_output = kidney_failure_agent(row_dict)
    vital_output = vital_signs_agent(row_dict)
    ventilation_output = mechanical_ventilation_agent(row_dict)

    supervisor_output = supervisor_agent(
        kidney_output,
        vital_output,
        ventilation_output
    )

    return kidney_output, vital_output, ventilation_output, supervisor_output


def main():
    input_path = "data/sample_features.csv"
    output_path = "results/rule_based_predictions.csv"

    df = pd.read_csv(input_path)

    predictions = []

    for _, row in df.iterrows():
        row_dict = row_to_dict(row)

        kidney, vital, ventilation, supervisor = run_prediction(row_dict)

        predictions.append({
            "subject_id": row_dict.get("subject_id"),
            "hadm_id": row_dict.get("hadm_id"),
            "stay_id": row_dict.get("stay_id"),
            "true_label": row_dict.get("hospital_expire_flag"),

            "kidney_risk": kidney["risk"],
            "kidney_score": kidney["score"],
            "kidney_reasons": "; ".join(kidney["reasons"]),

            "vital_risk": vital["risk"],
            "vital_score": vital["score"],
            "vital_reasons": "; ".join(vital["reasons"]),

            "ventilation_risk": ventilation["risk"],
            "ventilation_score": ventilation["score"],
            "ventilation_reasons": "; ".join(ventilation["reasons"]),

            "overall_risk": supervisor["overall_risk"],
            "total_score": supervisor["total_score"],
            "final_explanation": supervisor["final_explanation"]
        })

    result_df = pd.DataFrame(predictions)
    Path("results").mkdir(exist_ok=True)
    result_df.to_csv(output_path, index=False)

    print(f"Saved {output_path}")
    print(result_df.head(10))


if __name__ == "__main__":
    main()
