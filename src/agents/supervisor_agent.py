def supervisor_agent(kidney_output, vital_output, ventilation_output):
    agent_outputs = [
        kidney_output,
        vital_output,
        ventilation_output
    ]

    total_score = sum(agent["score"] for agent in agent_outputs)

    high_risk_agents = [
        agent for agent in agent_outputs
        if agent["risk"] == "high"
    ]

    if len(high_risk_agents) >= 2:
        overall_risk = "high"
    elif total_score >= 8:
        overall_risk = "high"
    elif len(high_risk_agents) == 1 or total_score >= 4:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    main_reasons = []
    for agent in agent_outputs:
        if agent["risk"] in ["medium", "high"]:
            main_reasons.append({
                "agent": agent["agent"],
                "risk": agent["risk"],
                "score": agent["score"],
                "reasons": agent["reasons"]
            })

    explanation_parts = []
    for item in main_reasons:
        reasons = ", ".join(item["reasons"])
        explanation_parts.append(
            f"{item['agent']} indicates {item['risk']} risk because of {reasons}."
        )

    if explanation_parts:
        final_explanation = " ".join(explanation_parts)
    else:
        final_explanation = "No major kidney, vital sign, or ventilation risk factors were detected."

    return {
        "overall_risk": overall_risk,
        "total_score": total_score,
        "main_reasons": main_reasons,
        "final_explanation": final_explanation
    }
