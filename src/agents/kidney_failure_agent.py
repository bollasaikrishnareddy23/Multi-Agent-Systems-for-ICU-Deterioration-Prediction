def kidney_failure_agent(row):
    score = 0
    reasons = []

    creatinine_max = row.get("creatinine_max_24h", None)
    creatinine_trend = row.get("creatinine_trend_24h", None)
    bun_max = row.get("bun_max_24h", None)
    urine_output = row.get("urine_output_24h", None)
    dialysis_flag = row.get("dialysis_flag_24h", 0)

    if creatinine_max is not None and creatinine_max >= 2.0:
        score += 2
        reasons.append("high creatinine")

    if creatinine_trend is not None and creatinine_trend > 0.3:
        score += 1
        reasons.append("creatinine is increasing")

    if bun_max is not None and bun_max >= 40:
        score += 1
        reasons.append("high BUN")

    if urine_output is not None and urine_output < 500:
        score += 2
        reasons.append("low urine output")

    if dialysis_flag == 1:
        score += 3
        reasons.append("dialysis event")

    if score >= 4:
        risk = "high"
    elif score >= 2:
        risk = "medium"
    else:
        risk = "low"

    return {
        "agent": "Kidney Failure Agent",
        "risk": risk,
        "score": score,
        "reasons": reasons
    }
