def mechanical_ventilation_agent(row):
    score = 0
    reasons = []

    mech_vent = row.get("mechanical_ventilation_flag_24h", 0)
    oxygen_support = row.get("oxygen_support_flag_24h", 0)
    fio2_max = row.get("fio2_max_24h", None)
    peep_max = row.get("peep_max_24h", None)

    if mech_vent == 1:
        score += 3
        reasons.append("patient is mechanically ventilated")

    if fio2_max is not None and fio2_max >= 0.6:
        score += 2
        reasons.append("high oxygen requirement")

    if peep_max is not None and peep_max >= 8:
        score += 1
        reasons.append("high PEEP")

    if oxygen_support == 1:
        score += 1
        reasons.append("oxygen or respiratory support required")

    if score >= 4:
        risk = "high"
    elif score >= 2:
        risk = "medium"
    else:
        risk = "low"

    return {
        "agent": "Mechanical Ventilation Agent",
        "risk": risk,
        "score": score,
        "reasons": reasons
    }
