# PULSAR

> Synapse tracks what you learn. Pulsar tracks what you create.

PULSAR is a CLI tool that extracts structured data from free-text descriptions of your projects and published content, no manual field-by-field input. Paste a sentence, get a structured record.

Part of a two-tool personal knowledge system:
- **[Synapse]** → maps concepts and learning progress (internal connections)
- **Pulsar** → tracks software built and content published (outward emissions)

---

## How it works

```
data/*.json (skill config)  →  patterns compiled at runtime
You paste free text         →  regex extracts fields + skill categories  →  saved to portfolio.json  →  export to CSV anytime

```

**Input**
```
ho creato un tool chiamato Pulsar usando python e json,
è completato, link https://github.com/sergio/pulsar
```

**Extracted automatically**
```json
{
  "nome": "Pulsar",
  "tecnologie": ["python", "json"],
  "stato": "completato",
  "link": "https://github.com/sergio/pulsar",
  "tipo": "tool"
}
```

---

## Features

- **Data-driven skill extraction** - skill categories loaded from external JSON files, patterns compiled at runtime, no hardcoded lists
- **Auto-extraction via regex** — name, technologies, date, status, link, platform
- **Two entry types** — software projects and published content (LinkedIn, X)
- **Persistent JSON storage** — entries accumulate across sessions
- **CSV export** — `projects.csv` (all entries) + `skills.csv` (technologies aggregated by count)
- **Terminal report** — readable summary of all saved entries
- **Error handling** — graceful messages for missing or corrupted files

---

## Usage

```bash
python pulsar.py
```

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          PULSAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Aggiungi software
2. Aggiungi contenuto
3. Esporta CSV
4. Leggi report
5. Esci
```

## Skill categories

PULSAR loads skill patterns from the `data/` folder at startup. Each file defines one category:

```json
{
  "label": "techs",
  "keywords": ["python", "sql", "bash", "git"]
}
```

| File | Label | Purpose |
|---|---|---|
| `techs.json` | `techs` | languages and core tools |
| `frameworks.json` | `frameworks` | libraries and frameworks |
| `cloud_providers.json` | `cloud` | cloud platforms and services |

To add a new technology, edit the relevant JSON file. To add a new category, drop a new `.json` file into `data/`. No code changes needed.

---

## Input guide

PULSAR reads natural language. Include the right keywords and it extracts the rest.

### Software entry

| Field | Keyword pattern | Example |
|---|---|---|
| Name | `chiamato X` / `si chiama X` | `chiamato Pulsar` |
| Technologies | mention them directly | `python`, `json`, `csv` |
| Status | use the word directly | `completato` / `in corso` / `wip` |
| Link | any URL | `https://github.com/...` |
| Type | use the word directly | `tool` / `progetto` |
| Date | any standard format | `05/2025` / `maggio 2025` |

**Example input:**
```
ho creato un tool chiamato Pulsar usando python e json, è completato,
link https://github.com/sergio/pulsar, maggio 2025
```

### Content entry

| Field | Keyword pattern | Example |
|---|---|---|
| Title | wrap in quotes `"..."` | `"Il mio primo tool Python"` |
| Platform | `social X` / `su linkedin` | `su linkedin` |
| Link | any URL | `https://linkedin.com/...` |
| Date | any standard format | `05/2025` |

**Example input:**
```
ho pubblicato "Il mio primo tool Python" su linkedin,
link https://linkedin.com/post/123, maggio 2025
```

---

## Output files

### `portfolio.json`
```json
{
  "portfolio": {
    "software": [
      {
        "nome": "Pulsar",
        "tipo": "tool",
        "tecnologie": ["python", "json"],
        "stato": "completato",
        "link": "https://github.com/sergio/pulsar",
        "data": "maggio 2025"
      }
    ],
    "contenuti": []
  }
}
```

### `projects.csv`
| sezione | nome | tipo | tecnologie | stato | link | data |
|---|---|---|---|---|---|---|
| software | Pulsar | tool | python, json | completato | https://... | maggio 2025 |

### `skills.csv`
| tecnologia | occorrenze |
|---|---|
| python | 3 |
| json | 2 |

---

## Requirements

- Python 3.10+
- Standard library only (`re`, `os`, `json`, `csv`) — no installs needed

---

## Part of a larger roadmap

PULSAR was built as a practical learning project while completing CS50P by Harvard university and transitioning into AI development. It covers regex, JSON, CSV, file I/O, CLI design, and error handling, all from the Python standard library.
