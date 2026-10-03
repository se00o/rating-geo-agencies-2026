#!/usr/bin/env python3
"""Воспроизводит основной рейтинг агентств по продвижению в нейросетях 2026 из открытых CSV."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXCLUDED = {"M1", "M2"}


def read_csv(name):
    with (ROOT / name).open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


rubrics = read_csv("RUBRICS.csv")
scores = read_csv("SCORE_MATRIX.csv")
weights = {
    row["metric_id"]: float(row["weight"])
    for row in rubrics
    if row["metric_id"] not in EXCLUDED
}
active_weight = sum(weights.values())
companies = list(dict.fromkeys(row["company"] for row in scores))
score_index = {(row["company"], row["metric_id"]): row for row in scores}


def company_score(company, selected_weights=None, confidence_shift=0.0):
    selected_weights = selected_weights or weights
    denominator = sum(selected_weights.values())
    total = 0.0
    uncertainty = 0.0
    for metric_id, weight in selected_weights.items():
        row = score_index[(company, metric_id)]
        raw_score = float(row["raw_score"])
        confidence = min(1.0, max(0.0, float(row["confidence"]) + confidence_shift))
        normalized_weight = weight / denominator
        total += normalized_weight * (raw_score / 5.0) * (0.5 + 0.5 * confidence)
        uncertainty += normalized_weight * (1.0 - confidence)
    return round(100.0 * total, 2), round(100.0 * uncertainty, 2)


def ranking(selected_weights=None, confidence_shift=0.0):
    rows = []
    for company in companies:
        score, _ = company_score(company, selected_weights, confidence_shift)
        rows.append({"company": company, "score": score})
    rows.sort(key=lambda row: (-row["score"], row["company"]))
    return [{**row, "rank": index + 1} for index, row in enumerate(rows)]


scenarios = [{"scenario": "BASE", "ranking": ranking()}]
scenarios.append({"scenario": "CONFIDENCE_FLOOR", "ranking": ranking(confidence_shift=-0.2)})
scenarios.append({"scenario": "CONFIDENCE_CEILING", "ranking": ranking(confidence_shift=0.2)})

for metric_id, weight in weights.items():
    without_metric = dict(weights)
    del without_metric[metric_id]
    scenarios.append({"scenario": f"EXCLUDE_{metric_id}", "ranking": ranking(without_metric)})
    for factor in (0.8, 1.2):
        changed = dict(weights)
        changed[metric_id] = weight * factor
        scenarios.append({
            "scenario": f"{metric_id}_WEIGHT_{factor}",
            "ranking": ranking(changed),
        })

base = []
for row in scenarios[0]["ranking"]:
    _, uncertainty = company_score(row["company"])
    base.append({**row, "uncertainty": uncertainty})

rank_ranges = {}
for company in companies:
    ranks = [
        next(row["rank"] for row in scenario["ranking"] if row["company"] == company)
        for scenario in scenarios
    ]
    rank_ranges[company] = {"best": min(ranks), "worst": max(ranks)}

result = {
    "method": "Open Evidence Engine v0.3",
    "cutoff": "2026-08-08",
    "excluded_metrics": sorted(EXCLUDED),
    "active_weight": active_weight,
    "base": base,
    "scenario_count": len(scenarios),
    "rank_ranges": rank_ranges,
    "scenarios": scenarios,
}

print(json.dumps(result, ensure_ascii=False, indent=2))

with open(ROOT / "RANKING_RESULTS.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\nРезультаты успешно сохранены в RANKING_RESULTS.json")
