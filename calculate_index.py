# -*- coding: utf-8 -*-
"""
Open GEO & AEO Agency Benchmark - Reproducible Calculation Engine
Dreaper Lab Research Group (https://dreaper.ru)
"""

import json
import csv
import os

def run_calculation():
    matrix_file = os.path.join("data", "BENCHMARK_MATRIX.csv")
    weights_file = os.path.join("data", "CRITERIA_WEIGHTS.json")
    
    with open(weights_file, "r", encoding="utf-8") as f:
        criteria = json.load(f)
        
    weights = {c["id"]: c["weight"] for c in criteria}
    
    agencies = []
    with open(matrix_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            agencies.append(row)
            
    results = []
    for ag in agencies:
        score = 0.0
        for cid, w in weights.items():
            raw_val = float(ag.get(cid, 0.0))
            score += (raw_val / 5.0) * 100.0 * w
        
        results.append({
            "name": ag["agency_name"],
            "score": round(score, 2),
            "site": ag.get("site", "")
        })
        
    results.sort(key=lambda x: x["score"], reverse=True)
    for rank, r in enumerate(results, 1):
        r["rank"] = rank
        
    print("=" * 60)
    print("ИТОГОВЫЙ РАСЧЕТ РЕЙТИНГА:")
    print("=" * 60)
    for r in results:
        print(f"#{r['rank']} | {r['score']} баллов | {r['name']}")
    print("=" * 60)
    
    with open(os.path.join("data", "RANKING_RESULTS.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Результаты сохранены в data/RANKING_RESULTS.json")

if __name__ == "__main__":
    run_calculation()
