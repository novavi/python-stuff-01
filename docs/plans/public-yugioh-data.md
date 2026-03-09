# Plan: public-yugioh-data

## Phase 1 — Download and Save All Yu-Gi-Oh Card Data

### Goal
Create a Python script that downloads all Yu-Gi-Oh card data from the public YGOPRODeck API and saves it as a local JSON file.

### Files to Create
| File | Location |
|------|----------|
| `retrieve-yugioh-data.py` | `public-yugioh-data/` |
| `public-yugioh-card-data.json` | `public-yugioh-data/` (created by the script) |

### API Details
- **Endpoint:** `https://db.ygoprodeck.com/api/v7/cardinfo.php`
- **No query parameters** — the bare endpoint returns all cards in the database, including Monster, Spell, and Trap cards.
- **Response format:** JSON with a top-level `"data"` key containing an array of card objects.

### Example card object structure (from `sample-card-data.json`)
```json
{
  "id": 88819587,
  "name": "Baby Dragon",
  "type": "Normal Monster",
  "atk": 1200,
  "def": 700,
  "level": 3,
  "attribute": "WIND",
  "card_sets": [...],
  "card_images": [...],
  "card_prices": [...]
}
```
Note: Spell and Trap cards will not have `atk`, `def`, or `level` fields.

### Implementation Notes
- Use **built-in Python modules only**: `urllib.request` (HTTP request), `json` (parse and save), and `os` (file path).
- Code style: simple, readable, appropriate for a 17-year-old CS pupil. No classes, no error handling, no abstractions.
- Both the script and the output JSON file live in the `public-yugioh-data/` folder.
- The script uses `os.path.dirname(os.path.abspath(__file__))` to determine its own location, so the JSON is always saved in the same folder as the script regardless of where the script is run from.
- A `User-Agent: Mozilla/5.0` header is required on the request — the API returns HTTP 403 if the default Python user-agent is used.
- The JSON file is pretty-printed with 2-space indentation (`indent=2` in `json.dump()`).
- The script is run manually by the user — Claude never executes it.

### Steps for Claude to implement
1. Create `public-yugioh-data/retrieve-yugioh-data.py` with the following logic:
   - Import `urllib.request`, `json`, and `os`
   - Define the API URL as a variable
   - Build a `Request` object with a `User-Agent` header
   - Make the HTTP request using `urllib.request.urlopen()`
   - Read and decode the response into a string
   - Parse the string into JSON with `json.loads()`
   - Determine the output path using `__file__`
   - Write the parsed data to `public-yugioh-card-data.json` using `json.dump()` with `indent=2`
2. The `public-yugioh-data/` folder is created manually — the script does not need to create it.

### Out of scope for Phase 1
- Any processing, filtering, or transformation of the data
- Downloading card images
- Pagination handling (the API returns all cards in a single response)

---

## Phase 2 — Download and Save Yu-Gi-Oh Card Images

### Goal
Create a Python script that reads the local `public-yugioh-card-data.json` file and downloads card images for each card, saving them into organised subfolders by image type.

### Files to Create
| File | Location |
|------|----------|
| `retrieve-yugioh-images.py` | `public-yugioh-data/` |
| `images/cards/<id>.jpg` | `public-yugioh-data/` (created by the script) |
| `images/cards_small/<id>.jpg` | `public-yugioh-data/` (created by the script) |
| `images/cards_cropped/<id>.jpg` | `public-yugioh-data/` (created by the script) |

### Input
- Reads `public-yugioh-card-data.json` from the same folder as the script (`public-yugioh-data/`)
- JSON structure: top-level `"data"` key containing an array of card objects
- Each card object has a `card_images` array; the script matches on `id` to find the correct image object

### Image URL structure (from `sample-card-data.json`)
```json
"card_images": [
  {
    "id": 88819587,
    "image_url":         "https://images.ygoprodeck.com/images/cards/88819587.jpg",
    "image_url_small":   "https://images.ygoprodeck.com/images/cards_small/88819587.jpg",
    "image_url_cropped": "https://images.ygoprodeck.com/images/cards_cropped/88819587.jpg"
  }
]
```
The filename in each URL (e.g. `88819587.jpg`) is used as the saved filename. The file extension is derived from the URL.

### URL-to-folder mapping
| Property | Save to folder |
|----------|---------------|
| `image_url` | `images/cards/` |
| `image_url_small` | `images/cards_small/` |
| `image_url_cropped` | `images/cards_cropped/` |

### Script behaviour
- `top1_only = True` — boolean flag at the top of the script; when `True` only the first card in the `data` array is processed (for testing); when `False` all cards are processed
- For each card: find the `card_images` entry whose `id` matches the card's top-level `id`, then download and save all three images
- Images are downloaded as binary files using `urllib.request.urlopen()` and saved with `open(path, "wb")`
- No `User-Agent` header on requests initially — test without first
- Output folders are created by the script using `os.makedirs()` with `exist_ok=True`
- The script is run manually by the user — Claude never executes it

### Implementation Notes
- Use **built-in Python modules only**: `urllib.request`, `json`, `os`
- Code style: simple, readable, appropriate for a 17-year-old CS pupil. No classes, no error handling, no abstractions.

### Steps for Claude to implement
1. Create `public-yugioh-data/retrieve-yugioh-images.py` with the following logic:
   - Import `urllib.request`, `json`, and `os`
   - Define `top1_only = True` near the top
   - Use `__file__` to determine the script's directory
   - Open and read `public-yugioh-card-data.json` from the script directory
   - Parse JSON and extract the `data` array
   - Slice to first 1 item if `top1_only` is `True`
   - Create the three output folders using `os.makedirs()` with `exist_ok=True`
   - Iterate over cards; for each card:
     - Find the matching `card_images` object by `id`
     - For each of the three image URLs: extract filename from URL, download binary content, save to the correct folder
2. Output folders are created by the script — no manual setup needed

### Extension: Error Handling
Some image URLs return HTTP 404 (not found), causing `urllib.request.urlopen()` to raise a `urllib.error.HTTPError` exception, which terminates the script before all images are downloaded.

**Solution:** Wrap each of the three image download/save blocks in a `try/except urllib.error.HTTPError` block. If the request fails, print a "Not found" message and continue to the next step (either the next image type for the same card, or the next card). `urllib.error` must be imported alongside `urllib.request`.

This pattern is applied identically to all three image types (`image_url`, `image_url_small`, `image_url_cropped`):
```python
try:
    image_data = urllib.request.urlopen(yugioh_image_url).read()
    with open(yugioh_image_file_path, "wb") as f:
        f.write(image_data)
    print("Save", yugioh_image_file_path)
except urllib.error.HTTPError:
    print("Not found", yugioh_image_file_path)
```

---

## Phase 3 — Load Yu-Gi-Oh Card Data into SQLite

### Goal
Create a SQL setup script to define the database tables, and a Python script to read `public-yugioh-card-data.json` and insert all card data into a SQLite database.

### Files to Create
| File | Location |
|------|----------|
| `table-setup.sql` | `public-yugioh-data/` |
| `load-yugioh-data.py` | `public-yugioh-data/` |

---

### Installing SQLite on Mac

SQLite comes pre-installed on macOS. To verify it is available, run:
```
sqlite3 --version
```
If it is not found, install it via Homebrew:
```
brew install sqlite
```

---

### Database Tables

#### Table: `card`
Stores one row per Yu-Gi-Oh card. Image URLs and prices are stored directly on this table (first entry from `card_images` and `card_prices` arrays respectively).

| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Auto-generated row ID |
| `card_passcode_id` | INTEGER UNIQUE | From JSON `id` field (referred to as a "passcode" in the API docs) — unique constraint prevents duplicate rows on re-run. Named `card_passcode_id` rather than `card_id` to avoid confusion with `card_set_link.card_id`, which is a foreign key to `card.id` |
| `name` | TEXT | |
| `type` | TEXT | e.g. `"Spell Card"`, `"Effect Monster"` |
| `human_readable_card_type` | TEXT | From `humanReadableCardType` |
| `frame_type` | TEXT | From `frameType` |
| `desc` | TEXT | Card description |
| `race` | TEXT | e.g. `"Dragon"`, `"Continuous"` |
| `archetype` | TEXT | Nullable |
| `attribute` | TEXT | Nullable — monster cards only (e.g. `"DARK"`) |
| `atk` | INTEGER | Nullable — monster cards only |
| `def` | INTEGER | Nullable — monster cards only |
| `level` | INTEGER | Nullable — monster cards only |
| `scale` | INTEGER | Nullable — Pendulum cards only |
| `linkval` | INTEGER | Nullable — Link monsters only |
| `linkmarkers` | TEXT | Nullable — Link monsters only; stored as comma-separated string (e.g. `"Left,Right,Bottom"`) |
| `typeline` | TEXT | Nullable; stored as comma-separated string (e.g. `"Beast,Effect"`) |
| `pend_desc` | TEXT | Nullable — Pendulum cards only |
| `monster_desc` | TEXT | Nullable — Pendulum cards only |
| `ygoprodeck_url` | TEXT | |
| `image_url` | TEXT | From first matching object in `card_images` |
| `image_url_small` | TEXT | From first matching object in `card_images` |
| `image_url_cropped` | TEXT | From first matching object in `card_images` |
| `price_cardmarket` | TEXT | From first object in `card_prices` |
| `price_tcgplayer` | TEXT | From first object in `card_prices` |
| `price_ebay` | TEXT | From first object in `card_prices` |
| `price_amazon` | TEXT | From first object in `card_prices` |
| `price_coolstuffinc` | TEXT | From first object in `card_prices` |
| `ban_tcg` | TEXT | Nullable — from `banlist_info` |
| `ban_ocg` | TEXT | Nullable — from `banlist_info` |
| `ban_goat` | TEXT | Nullable — from `banlist_info` |
| `created_at` | TEXT DEFAULT (datetime('now')) | Auto-set by SQLite to current UTC datetime on insert — no value needed in Python INSERT |

---

#### Table: `card_set`
Stores one row per unique card set (identified by `set_name`).

| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Auto-generated row ID |
| `set_name` | TEXT UNIQUE | e.g. `"Metal Raiders"` |
| `created_at` | TEXT DEFAULT (datetime('now')) | Auto-set by SQLite to current UTC datetime on insert — no value needed in Python INSERT |

---

#### Table: `card_set_link` *(junction / link table)*
Resolves the many-to-many relationship between `card` and `card_set`. A card can belong to many sets, and a set contains many cards.

`set_rarity`, `set_rarity_code`, `set_code` and `set_price` are stored here rather than in `card_set` because they describe the **relationship** between a specific card and a specific set, not the set itself. For example, the same card can appear in the same set at multiple different rarities, each with its own set code and price. Storing these fields in `card_set` would make it impossible to represent this.

**Duplicate prevention:** Because a card can appear in the same set at multiple rarities, a simple unique constraint on `(card_id, set_code)` is not sufficient to prevent duplicates on re-run. Instead, `load-yugioh-data.py` does a `SELECT` check against all six fields (`card_id`, `card_set_id`, `set_code`, `set_rarity`, `set_rarity_code`, `set_price`) before inserting, and only inserts if no matching row is found.

| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Auto-generated row ID |
| `card_id` | INTEGER | Foreign key → `card.id` |
| `card_set_id` | INTEGER | Foreign key → `card_set.id` |
| `set_code` | TEXT | e.g. `"MRD-061"` |
| `set_rarity` | TEXT | e.g. `"Common"` |
| `set_rarity_code` | TEXT | e.g. `"(C)"` |
| `set_price` | TEXT | |
| `created_at` | TEXT DEFAULT (datetime('now')) | Auto-set by SQLite to current UTC datetime on insert — no value needed in Python INSERT |

---

### `table-setup.sql`
SQL script to create all three tables. Run this once in SQLite before running the Python script.

To create the database and run the setup script:
```
sqlite3 public-yugioh-data/yugioh.db < public-yugioh-data/table-setup.sql
```
This creates `yugioh.db` in the `public-yugioh-data/` folder and sets up all tables.

To verify the tables were created:
```
sqlite3 public-yugioh-data/yugioh.db ".tables"
```

---

### `load-yugioh-data.py`

#### Logic
1. Import `json`, `os`, `sqlite3`
2. Use `__file__` to determine the script directory
3. Open and read `public-yugioh-card-data.json`
4. Connect to `yugioh.db` in the same directory
5. For each card in the `data` array:
   - Find the matching `card_images` object (where `card_images[i]["id"] == card["id"]`)
   - Take the first object from `card_prices`
   - Read `banlist_info` if present (all three fields are nullable)
   - Convert `typeline` and `linkmarkers` arrays to comma-separated strings if present
   - Insert a row into `card`
   - For each entry in `card_sets`:
     - Insert the `set_name` into `card_set` if it does not already exist
     - Look up the `card_set.id` for that `set_name`
     - Insert a row into `card_set_link`
6. Commit and close the connection

#### Code style
- Built-in Python modules only (`json`, `os`, `sqlite3`)
- Simple and readable — appropriate for a 17-year-old CS pupil
- No classes, no error handling
- Assign intermediate variables rather than chaining calls inline
- Ensure the code does not look AI-generated

---

### `.gitignore`
Add `public-yugioh-data/yugioh.db` to `.gitignore` so the database file is not committed to the repo.
