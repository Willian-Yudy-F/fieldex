# FielDex 🦅

> **Gotta learn 'em all.**
> A daily knowledge "Pokédex" — every card is visible, but a card only joins the reader's local Trainer Profile after they solve a logic/math challenge.

FielDex is a learning-in-public project: a personal commitment to learn something new every single day, turn it into a polished collectible card, and keep a public, growing dex of it all. The full gallery is open for reading; the collection profile is earned through small reasoning puzzles and saved locally in the user's browser. The name is a play on **Pokédex** — but instead of catching creatures, I'm catching knowledge — with a small nod to *o Timão* (the club's nickname, "a Fiel", founded in **1910**).

## Why this exists

Three goals in one project:

1. **Learn consistently.** One entry a day, no exceptions. The dex grows; so does the habit.
2. **Practice real skills.** Python (content + image generation), data modeling (the dex as a JSON database), and frontend (the gallery), all version-controlled with a daily commit streak.
3. **Share something useful.** Each entry becomes a card I can post on social media — and readers can collect it by solving a small logic challenge.
4. **Make progress feel personal.** Readers can create a local Trainer Profile, collect cards, earn type badges, and keep their streak on their own device.

## What's inside

| File | What it does |
|------|--------------|
| `fieldex.json` | The dex — the database of every captured entry |
| `generate_card.py` | Renders a Pokédex-style trading card (PNG) for any entry, ready to post |
| `add_entry.py` | Interactive CLI to add a new entry and auto-generate its card |
| `index.html` | The web gallery — browse the whole collection, filter by type, view details (GitHub Pages) |
| `cards/` | All generated card images |

## How a "capture" works

Each entry is typed (like a Pokémon type) and has a rarity. The web gallery shows every card by default, but local profile progress only advances after the reader creates a Trainer Profile and answers that card's deterministic logic/math puzzle.

Progress is saved with `localStorage`, so it belongs to that browser/device:

- trainer name, mark and home base
- collected card IDs and capture dates
- current streak
- earned type badges

There is no backend account yet; clearing browser storage or switching devices starts a fresh local profile.

- **Types:** probability · math · logic · history · geography · data · security · corinthians
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
Link: willian-yudy-f.github.io
```

## Roadmap

- [ ] 30-day streak
- [ ] 100 entries
- [ ] Auto-post cards to social via API
- [ ] Search + full-text filtering in the gallery
- [ ] A "random capture" button (your daily review flashcard)

---

*Built with Python and a lot of curiosity. Since 1910.* 🦅
