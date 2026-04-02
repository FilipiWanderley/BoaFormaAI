from datetime import datetime, timezone

from app.config import settings


def evaluate_ai_alerts(metrics_snapshot: dict) -> dict:
    alerts: list[dict] = []
    ai_calls = int(metrics_snapshot.get("ai_usage_count", 0))
    ai_errors = int(metrics_snapshot.get("ai_error_count", 0))
    ai_retries = int(metrics_snapshot.get("ai_retry_count", 0))
    operations = metrics_snapshot.get("ai_operations", {})

    if ai_calls >= settings.ai_alert_min_calls:
        error_rate = (ai_errors / ai_calls) * 100 if ai_calls else 0.0
        retry_rate = (ai_retries / ai_calls) * 100 if ai_calls else 0.0
        if error_rate >= settings.ai_alert_error_rate_pct:
            alerts.append(
                {
                    "code": "AI_ERROR_RATE_HIGH",
                    "severity": "high",
                    "value": round(error_rate, 2),
                    "threshold": settings.ai_alert_error_rate_pct,
                    "message": "Taxa de erro da IA acima do limite configurado.",
                }
            )
        if retry_rate >= settings.ai_alert_retry_rate_pct:
            alerts.append(
                {
                    "code": "AI_RETRY_RATE_HIGH",
                    "severity": "medium",
                    "value": round(retry_rate, 2),
                    "threshold": settings.ai_alert_retry_rate_pct,
                    "message": "Taxa de retries da IA acima do limite configurado.",
                }
            )

    for operation, stats in operations.items():
        avg_latency = float(stats.get("avg_latency_ms", 0.0))
        if avg_latency >= settings.ai_alert_avg_latency_ms:
            alerts.append(
                {
                    "code": "AI_LATENCY_HIGH",
                    "severity": "high",
                    "operation": operation,
                    "value": round(avg_latency, 2),
                    "threshold": settings.ai_alert_avg_latency_ms,
                    "message": "Latência média da IA acima do limite configurado.",
                }
            )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alerts": alerts,
        "has_alerts": len(alerts) > 0,
    }
