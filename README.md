# Pulsar

> Synapse tracks what you learn. Pulsar tracks what you create.

![Pulsar demo](Pulsar-demo.gif)

PULSAR is a CLI tool that extracts structured data from free-text descriptions of your projects and published content, no manual field-by-field input. Paste a sentence, get a structured record.

Part of a two-tool personal knowledge system:
- **[Synapse]** maps concepts and learning progress (internal connections)
- **Pulsar** tracks software built and content published (outward emissions)

---

## How it works

```
data/*.json (skill config)  →  patterns compiled at runtime
You paste free text         →  regex extracts fields + skill categories
                            →  each record becomes a typed object (Software / Contenuto)
                            →  saved to data.json  →  export to CSV anytime
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

## Architecture

Each entry is not a loose dictionary but a typed object. A small class hierarchy models the two kinds of record, sharing what they have in common and diverging where they differ:

```
Entry (base)        data, link                       · to_dict()
├── Software        + tipo, nome, tecnologie, stato   · to_dict() · from_dict() · __str__()
└── Contenuto       + titolo, argomento, piattaforma  · to_dict() · from_dict() · __str__()
```

- **Inheritance**: `Entry` holds the fields common to every record (`data`, `link`); `Software` and `Contenuto` add their own and reuse the parent through `super()`.
- **Object/dict bridge**: `to_dict()` turns an object into a plain dict for JSON and CSV; `from_dict()` (a classmethod) rebuilds an object from a stored dict. Storage stays in plain JSON, the program works with real objects.
- **Polymorphism**: saving (`save_portfolio`) and reporting (`read_report`) call `to_dict()` and `print(obj)` without knowing the concrete type. Each object carries its own behavior, so the same line works for both kinds of entry.

---

## Features

- **Object-oriented design** - typed entry classes with inheritance and polymorphic serialization, not raw dictionaries
- **Data-driven skill extraction** - skill categories loaded from external JSON files, patterns compiled at runtime, no hardcoded lists
- **Auto-extraction via regex** - name, technologies, date, status, link, platform
- **Two entry types** - software projects and published content (LinkedIn, X)
- **Persistent JSON storage** - entries accumulate across sessions
- **CSV export** - `projects.csv` (all entries) + `skills.csv` (technologies aggregated by count)
- **Terminal report** - readable summary of all saved entries
- **Error handling** - graceful messages for missing or corrupted files

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

Pulsar loads skill patterns from the `data/` folder at startup. Each file defines one category:

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

Pulsar reads natural language. Include the right keywords and it extracts the rest.

### Software entry

| Field | Keyword pattern | Example |
|---|---|---|
| Name | `chiamato X` / `si chiama X` | `chiamato Pulsar` |
| Technologies | mention them directly | `python`, `json`, `csv` |
| Status | use the word directly | `completato` / `in corso` / `wip` |
| Link | any URL | `https://github.com/...` |
| Type | use the word directly | `tool` / `progetto` |
| Date | any standard format | `05/2025` / `maggio 2025` |

Note: a project name is read as a single token (no spaces), so `chiamato Pulsar` or `chiamato call-outcome-tracker` work; multi-word names with spaces are truncated to the first word.

**Example input:**
```
ho creato un tool chiamato Pulsar usando python e json, è completato,
link https://github.com/sergio/pulsar, maggio 2025
```

### Content entry

| Field | Keyword pattern | Example |
|---|---|---|
| Title | wrap in quotes `"..."` | `"Il mio primo tool Python"` |
| Topic | tech/skills mentioned, auto-detected | `python`, `git` |
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

### `data.json`
```json
{
  "portfolio": {
    "software": [
      {
        "data": "maggio 2025",
        "tipo": "tool",
        "nome": "Pulsar",
        "tecnologie": ["python", "json"],
        "stato": "completato",
        "link": "https://github.com/sergio/pulsar"
      }
    ],
    "contenuti": [
      {
        "data": "maggio 2025",
        "titolo": "Il mio primo tool Python",
        "argomento": ["python"],
        "piattaforma": "linkedin",
        "link": "https://linkedin.com/post/123"
      }
    ]
  }
}
```

### `projects.csv`
| sezione | nome | tipo | piattaforma | tecnologie | argomento | stato | link | data |
|---|---|---|---|---|---|---|---|---|
| software | Pulsar | tool | | python, json | | completato | https://... | maggio 2025 |
| contenuti | Il mio primo tool Python | | linkedin | | python | | https://... | maggio 2025 |

### `skills.csv`
| tecnologia | occorrenze |
|---|---|
| python | 3 |
| json | 2 |

---

## Requirements

- Python 3.10+
- Standard library only (`re`, `os`, `json`, `csv`), no installs needed

---

## Part of a larger roadmap

Pulsar was built as a practical learning project while completing CS50P by Harvard University and transitioning into AI development. It covers object-oriented design, regex, JSON, CSV, file I/O, CLI design, and error handling, all from the Python standard library.
