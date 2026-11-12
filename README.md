# FielDex 🦅

[![CI](https://github.com/Willian-Yudy-F/fieldex/actions/workflows/ci.yml/badge.svg)](https://github.com/Willian-Yudy-F/fieldex/actions/workflows/ci.yml)

A learning-in-public project that turns short lessons into collectible knowledge cards.
The public gallery currently contains 42 entries across probability, maths, history,
geography, data, security and football topics.

**Live gallery:** https://willian-yudy-f.github.io/fieldex/

## In plain English

Every card explains one idea, why it matters and a few tags. Anyone can read the gallery.
A reader can also create a local profile and solve a deterministic logic or maths challenge
to add cards to their browser-based collection.

The profile is not a server account. Trainer name, collected cards, badges and streak are
stored in `localStorage` on that device. Clearing site data or changing browsers starts a
new local collection.

## What this project demonstrates

- a versioned JSON content model;
- validation and a guided content-entry CLI in Python;
- deterministic Pillow-based card generation for social images;
- a framework-free HTML/CSS/JavaScript gallery;
- local-only progress with no backend account;
- a generated JavaScript fallback that remains in sync with the JSON source;
- automated checks and card rebuilding through GitHub Actions.

## Project structure

```text
fieldex.json          source of truth for all entries
fieldex_core.py       shared schema validation
build_data_js.py      generates the offline JavaScript fallback
generate_card.py      renders PNG cards
add_entry.py          guided CLI with rollback on generation failure
fieldex-data.js       generated fallback for file/offline use
index.html            public gallery and local collection experience
cards/                generated card images
tests/                data, HTML and JavaScript checks
```

## Data model

Each entry requires a contiguous numeric ID, ISO date, supported category and rarity,
non-empty title/fact/explanation and a list of tags.

```json
{
  "id": 1,
  "date": "2026-06-07",
  "category": "probability",
  "rarity": "rare",
  "title": "The Birthday Paradox",
  "fact": "In a room of 23 people, a shared birthday is already likely.",
  "why": "The number of pairs grows much faster than the number of people.",
  "tags": ["statistics", "counterintuitive"]
}
```

Some entries also include visualisation metadata and English translations. The World Cup
guide in the gallery includes its own visible source links. Older cards do not yet carry a
per-entry source field; adding citations to the core schema is the main content-quality
improvement still required.

## Add and generate cards

Create an environment and install the rendering dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then use one of the supported commands:

```bash
# guided entry creation, validation and card generation
python add_entry.py

# rebuild the browser fallback after editing JSON directly
python build_data_js.py

# regenerate one card or every card
python generate_card.py 42
python generate_card.py --all
```

If guided generation fails, `add_entry.py` restores the original JSON instead of leaving
a half-created entry.

## Preview locally

```bash
python -m http.server 8000
```

Open `http://localhost:8000/`.

## Quality checks

```bash
python -m unittest discover -s tests -v
node tests/validate-script.mjs
python build_data_js.py
git diff --exit-code fieldex-data.js
```

CI runs these checks on Python 3.11 and 3.13. A separate workflow rebuilds the cards and
offline data when the JSON or generator changes.

## Current limitations

- Local progress does not sync across devices.
- Challenge difficulty is not calibrated.
- Card rendering uses Arial on macOS and DejaVu Sans on Linux, so small typography
  differences remain possible across platforms.
- Many older entries still need a structured citation field.
- “Daily” describes the learning format; it is not a claim that a card has been published
  without interruption every calendar day.

## Next improvements

- Add `sources` to every entry and display citations in each card detail.
- Add full-text search across translated content.
- Add a random review mode for previously collected cards.
- Publish an export/import option for local progress without creating an account.

---

Built by [Willian Yudy Futema](https://github.com/Willian-Yudy-F) ·
[Portfolio](https://willian-yudy-f.github.io/) ·
[LinkedIn](https://www.linkedin.com/in/willian-yudy-futema/)
