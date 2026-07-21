#!/usr/bin/env python3
"""Look up a food's nutrients (per 100g) in the local TACO table.

Usage:
    scripts/lookup_food.py <query> [--grams N] [--limit N]

Examples:
    scripts/lookup_food.py "arroz integral cozido"
    scripts/lookup_food.py "banana prata" --grams 120
"""
import argparse
import json
import unicodedata
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "taco.json"
STOPWORDS = {"de", "da", "do", "das", "dos", "e", "com", "sem", "a", "o"}


def normalize(text):
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def search(query, foods, limit=5):
    terms = [t for t in normalize(query).split() if t not in STOPWORDS]
    scored = []
    for food in foods:
        name = normalize(food["name"])
        if all(term in name for term in terms):
            scored.append((sum(name.count(term) for term in terms), food))
    scored.sort(key=lambda pair: (-pair[0], len(pair[1]["name"])))
    return [food for _, food in scored[:limit]]


def scale(food, grams):
    factor = grams / 100
    return {
        "name": food["name"],
        "grams": grams,
        "calories": round(food["calories"] * factor, 1) if food["calories"] is not None else None,
        "protein": round(food["protein"] * factor, 1) if food["protein"] is not None else None,
        "carbs": round(food["carbs"] * factor, 1) if food["carbs"] is not None else None,
        "fats": round(food["fats"] * factor, 1) if food["fats"] is not None else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Food name to search for (Portuguese, matches TACO descriptions)")
    parser.add_argument("--grams", type=float, default=100, help="Portion size in grams (default: 100)")
    parser.add_argument("--limit", type=int, default=5, help="Max number of matches to show")
    args = parser.parse_args()

    foods = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    matches = search(args.query, foods, args.limit)

    if not matches:
        print(f'No match found for "{args.query}"')
        return

    for food in matches:
        print(json.dumps(scale(food, args.grams), ensure_ascii=False))


if __name__ == "__main__":
    main()
