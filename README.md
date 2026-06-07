# FielDex 🦅

> **Gotta learn 'em all.**
> A daily knowledge "Pokédex" — every day I capture one fact, puzzle, or curiosity (probability, math, logic, history, geography… and the occasional Corinthians lore) and add it to the collection.

FielDex is a learning-in-public project: a personal commitment to learn something new every single day, turn it into a polished collectible card, and keep a public, growing dex of it all. The name is a play on **Pokédex** — but instead of catching creatures, I'm catching knowledge — with a small nod to *o Timão* (the club's nickname, "a Fiel", founded in **1910**).

## Why this exists

Three goals in one project:

1. **Learn consistently.** One entry a day, no exceptions. The dex grows; so does the habit.
2. **Practice real skills.** Python (content + image generation), data modeling (the dex as a JSON database), and frontend (the gallery), all version-controlled with a daily commit streak.
3. **Share something useful.** Each entry becomes a card I can post on social media — using social media to *build* instead of scroll.

## What's inside

| File | What it does |
|------|--------------|
| `fieldex.json` | The dex — the database of every captured entry |
| `generate_card.py` | Renders a Pokédex-style trading card (PNG) for any entry, ready to post |
| `add_entry.py` | Interactive CLI to add a new entry and auto-generate its card |
| `index.html` | The web gallery — browse the whole collection, filter by type, view details (GitHub Pages) |
| `cards/` | All generated card images |

## How a "capture" works

Each entry is typed (like a Pokémon type) and has a rarity:

- **Types:** probability · math · logic · history · geography · data · corinthians
- **Rarity:** common → uncommon → rare → epic → legendary

```json
{
  "id": 1,
  "date": "2026-06-07",
  "category": "probability",
  "rarity": "rare",
  "title": "The Birthday Paradox",
  "fact": "In a room of just 23 people, there's a 50% chance two share a birthday.",
  "why": "We compare every PAIR of people, not each person to one fixed date.",
  "tags": ["statistics", "counterintuitive"]
}
```

## Usage

```bash
# add a new entry (guided) and auto-generate its card
python add_entry.py

# regenerate one card by id
python generate_card.py 1

# regenerate every card
python generate_card.py --all
```

Then preview the gallery locally:

```bash
python -m http.server 8000
# open http://localhost:8000
```

## Roadmap

- [ ] 30-day streak
- [ ] 100 entries
- [ ] Auto-post cards to social via API
- [ ] Search + full-text filtering in the gallery
- [ ] A "random capture" button (your daily review flashcard)

---

*Built with Python and a lot of curiosity. Since 1910.* 🦅
