import argparse
import json


def evaluate_cost(current_cost: float, budget_limit: float) -> dict:
    usage_percent = (current_cost / budget_limit) * 100 if budget_limit > 0 else 0
    status = "ok"
    if usage_percent >= 100:
        status = "critical"
    elif usage_percent >= 80:
        status = "warning"
    return {
        "current_cost_usd": round(current_cost, 2),
        "budget_limit_usd": round(budget_limit, 2),
        "usage_percent": round(usage_percent, 2),
        "status": status,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-cost", type=float, required=True)
    parser.add_argument("--budget-limit", type=float, required=True)
    args = parser.parse_args()

    result = evaluate_cost(args.current_cost, args.budget_limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if result["status"] in {"warning", "critical"}:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
