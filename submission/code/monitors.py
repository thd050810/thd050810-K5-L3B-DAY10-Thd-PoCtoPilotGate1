def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def missing_delivery_date_rate(trials):
    incomplete = sum(
        any(event["type"] == "guard" and event.get("kind") == "missing_delivery_date" for event in trial["events"])
        for trial in trials
    )
    return incomplete / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,
    "missing_delivery_date_rate": missing_delivery_date_rate,
}
STARTER_MONITORS = ("escalation_rate",)
