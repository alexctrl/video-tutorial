#!/usr/bin/env python3
"""Look up a food's nutrients (per 100g) in the local TACO table.

Checks data/food_index.json first for a previously saved match on this
query; falls back to a fuzzy search of the TACO table otherwise. Pass
--save to remember the top match for next time.

Usage:
    scripts/lookup_food.py <query> [--grams N] [--limit N] [--save]

Examples:
    scripts/lookup_food.py "arroz integral cozido"
    scripts/lookup_food.py "raw rice" --grams 100 --save
"""
import argparse
import json
import unicodedata
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "taco.json"
INDEX_PATH = Path(__file__).resolve().parent.parent / "data" / "food_index.json"
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


def load_index():
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return {}


def save_index_entry(query, food):
    index = load_index()
    index[normalize(query)] = {
        "query": query,
        "taco_id": food["id"],
        "taco_name": food["name"],
    }
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    parser.add_argument("--save", action="store_true", help="Save the top match to data/food_index.json")
    args = parser.parse_args()

    foods = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    by_id = {food["id"]: food for food in foods}

    index = load_index()
    cached = index.get(normalize(args.query))
    if cached is not None:
        print(json.dumps(scale(by_id[cached["taco_id"]], args.grams), ensure_ascii=False))
        print("(from data/food_index.json)")
        return

    matches = search(args.query, foods, args.limit)

    if not matches:
        print(f'No match found for "{args.query}"')
        return

    for food in matches:
        print(json.dumps(scale(food, args.grams), ensure_ascii=False))

    if args.save:
        save_index_entry(args.query, matches[0])
        print(f'Saved "{args.query}" -> "{matches[0]["name"]}" to data/food_index.json')


if __name__ == "__main__":
    main()
