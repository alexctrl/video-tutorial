# video-tutorial

A simple calorie tracker.

- `calorie-tracker.schema.json` — JSON Schema for the tracker: a `name`, a list of `days`, each day parent to its logged food `items` (name, protein, carbs, fats, calories).
- `calorie-tracker.json` — the live tracker data file.
- `calorie-tracker.example.json` — a sample file showing the shape of the data.
- `data/taco.json` — Brazilian food composition table (TACO, NEPA/UNICAMP), nutrients per 100g, sourced from [marcelosanto/tabela_taco](https://github.com/marcelosanto/tabela_taco) (MIT).
- `scripts/lookup_food.py` — search `data/taco.json` for a food by (Portuguese) name and get its macros, optionally scaled to a portion size in grams.
- `scripts/log_food.py` — append a food item to a day in `calorie-tracker.json`, creating the day if it doesn't exist yet.

## Usage

```sh
python3 scripts/lookup_food.py "peito de frango grelhado" --grams 150
python3 scripts/log_food.py "Frango, peito, sem pele, grelhado" --protein 48 --carbs 0 --fats 3.7 --calories 238.8
```
