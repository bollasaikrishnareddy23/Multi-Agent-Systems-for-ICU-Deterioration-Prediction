def vital_signs_agent(row):
    score = 0
    reasons = []

    heart_rate_max = row.get("heart_rate_max_24h", None)
    map_min = row.get("map_min_24h", None)
    sbp_min = row.get("sbp_min_24h", None)
    resp_rate_max = row.get("resp_rate_max_24h", None)
    spo2_min = row.get("spo2_min_24h", None)
    temperature_max = row.get("temperature_max_24h", None)
    temperature_min = row.get("temperature_min_24h", None)

    if heart_rate_max is not None and heart_rate_max > 120:
        score += 1
        reasons.append("very high heart rate")

    if map_min is not None and map_min < 65:
        score += 2
        reasons.append("low mean arterial pressure")

    if sbp_min is not None and sbp_min < 90:
        score += 1
        reasons.append("low systolic blood pressure")

    if resp_rate_max is not None and resp_rate_max > 30:
        score += 1
        reasons.append("high respiratory rate")

    if spo2_min is not None and spo2_min < 90:
        score += 2
        reasons.append("low oxygen saturation")

    abnormal_temp = False
    if temperature_max is not None and temperature_max >= 38.3:
        abnormal_temp = True
    if temperature_min is not None and temperature_min < 36:
        abnormal_temp = True

    if abnormal_temp:
        score += 1
        reasons.append("abnormal temperature")

    if score >= 4:
        risk = "high"
    elif score >= 2:
        risk = "medium"
    else:
        risk = "low"

    return {
        "agent": "Vital Signs Agent",
        "risk": risk,
        "score": score,
        "reasons": reasons
    }
