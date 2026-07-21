#!/usr/bin/env python3
"""Append a food item to a day in calorie-tracker.json (creating the day if needed).

Usage:
    scripts/log_food.py <name> --protein N --carbs N --fats N --calories N [--date YYYY-MM-DD]
"""
import argparse
import json
from datetime import date
from pathlib import Path

TRACKER_PATH = Path(__file__).resolve().parent.parent / "calorie-tracker.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", help="Food item name")
    parser.add_argument("--protein", type=float, required=True, help="Protein in grams")
    parser.add_argument("--carbs", type=float, required=True, help="Carbohydrates in grams")
    parser.add_argument("--fats", type=float, required=True, help="Fats in grams")
    parser.add_argument("--calories", type=float, required=True, help="Calories in kcal")
    parser.add_argument("--date", default=str(date.today()), help="Day date, YYYY-MM-DD (default: today)")
    args = parser.parse_args()

    tracker = json.loads(TRACKER_PATH.read_text(encoding="utf-8"))

    day = next((d for d in tracker["days"] if d["date"] == args.date), None)
    if day is None:
        day = {"date": args.date, "items": []}
        tracker["days"].append(day)
        tracker["days"].sort(key=lambda d: d["date"])

    day["items"].append({
        "name": args.name,
        "protein": args.protein,
        "carbs": args.carbs,
        "fats": args.fats,
        "calories": args.calories,
    })

    TRACKER_PATH.write_text(json.dumps(tracker, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f'Logged "{args.name}" on {args.date}.')


if __name__ == "__main__":
    main()
