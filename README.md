# Pulsar

**🇮🇹 Italiano | [🇬🇧 English](#english)**

> Synapse traccia ciò che impari. Pulsar traccia ciò che crei.

![Pulsar demo](Pulsar-demo.gif)

PULSAR è un tool CLI che estrae dati strutturati da descrizioni in testo libero dei tuoi progetti e contenuti pubblicati, senza input manuale campo per campo. Incolla una frase, ottieni un record strutturato.

Parte di un sistema di conoscenza personale a due strumenti:
- **[Synapse]** mappa concetti e progressi di apprendimento (connessioni interne)
- **Pulsar** traccia software costruito e contenuti pubblicati (emissioni verso l'esterno)

---

## Come funziona

```
data/*.json (config delle skill)  →  pattern compilati a runtime
Incolli testo libero               →  la regex estrae campi + categorie di skill
                                    →  ogni record diventa un oggetto tipizzato (Software / Contenuto)
                                    →  salvato in data.json  →  esportabile in CSV in qualsiasi momento
```

**Input**
```
ho creato un tool chiamato Pulsar usando python e json,
è completato, link https://github.com/sergio/pulsar
```

**Estratto automaticamente**
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

## Architettura

Ogni voce non è un dizionario slegato ma un oggetto tipizzato. Una piccola gerarchia di classi modella i due tipi di record, condividendo ciò che hanno in comune e differenziandosi dove serve:

```
Entry (base)        data, link                       · to_dict()
├── Software        + tipo, nome, tecnologie, stato   · to_dict() · from_dict() · __str__()
└── Contenuto       + titolo, argomento, piattaforma  · to_dict() · from_dict() · __str__()
```

- **Ereditarietà**: `Entry` contiene i campi comuni a ogni record (`data`, `link`); `Software` e `Contenuto` aggiungono i propri e riutilizzano il genitore tramite `super()`.
- **Ponte oggetto/dizionario**: `to_dict()` trasforma un oggetto in un dizionario semplice per JSON e CSV; `from_dict()` (un classmethod) ricostruisce un oggetto da un dizionario salvato. Lo storage resta in JSON semplice, il programma lavora con oggetti reali.
- **Polimorfismo**: il salvataggio (`save_portfolio`) e il report (`read_report`) chiamano `to_dict()` e `print(obj)` senza conoscere il tipo concreto. Ogni oggetto porta con sé il proprio comportamento, quindi la stessa riga funziona per entrambi i tipi di voce.

---

## Funzionalità

- **Design orientato agli oggetti** - classi di voci tipizzate con ereditarietà e serializzazione polimorfica, non dizionari grezzi
- **Estrazione di skill data-driven** - categorie di skill caricate da file JSON esterni, pattern compilati a runtime, nessuna lista hardcoded
- **Auto-estrazione tramite regex** - nome, tecnologie, data, stato, link, piattaforma
- **Due tipi di voce** - progetti software e contenuti pubblicati (LinkedIn, X)
- **Storage JSON persistente** - le voci si accumulano tra le sessioni
- **Esportazione CSV** - `projects.csv` (tutte le voci) + `skills.csv` (tecnologie aggregate per conteggio)
- **Report da terminale** - riepilogo leggibile di tutte le voci salvate
- **Gestione degli errori** - messaggi chiari per file mancanti o corrotti

---

## Utilizzo

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

## Categorie di skill

Pulsar carica i pattern delle skill dalla cartella `data/` all'avvio. Ogni file definisce una categoria:

```json
{
  "label": "techs",
  "keywords": ["python", "sql", "bash", "git"]
}
```

| File | Etichetta | Scopo |
|---|---|---|
| `techs.json` | `techs` | linguaggi e tool principali |
| `frameworks.json` | `frameworks` | librerie e framework |
| `cloud_providers.json` | `cloud` | piattaforme e servizi cloud |

Per aggiungere una nuova tecnologia, modifica il file JSON relativo. Per aggiungere una nuova categoria, inserisci un nuovo file `.json` in `data/`. Nessuna modifica al codice necessaria.

---

## Guida all'input

Pulsar legge il linguaggio naturale. Includi le parole chiave giuste e il tool estrae il resto.

### Voce software

| Campo | Pattern parola chiave | Esempio |
|---|---|---|
| Nome | `chiamato X` / `si chiama X` | `chiamato Pulsar` |
| Tecnologie | menzionale direttamente | `python`, `json`, `csv` |
| Stato | usa direttamente la parola | `completato` / `in corso` / `wip` |
| Link | qualsiasi URL | `https://github.com/...` |
| Tipo | usa direttamente la parola | `tool` / `progetto` |
| Data | qualsiasi formato standard | `05/2025` / `maggio 2025` |

Nota: il nome di un progetto viene letto come un singolo token (senza spazi), quindi `chiamato Pulsar` o `chiamato call-outcome-tracker` funzionano; i nomi multi-parola con spazi vengono troncati alla prima parola.

**Esempio di input:**
```
ho creato un tool chiamato Pulsar usando python e json, è completato,
link https://github.com/sergio/pulsar, maggio 2025
```

### Voce contenuto

| Campo | Pattern parola chiave | Esempio |
|---|---|---|
| Titolo | racchiuso tra virgolette `"..."` | `"Il mio primo tool Python"` |
| Argomento | tech/skill menzionate, rilevate automaticamente | `python`, `git` |
| Piattaforma | `social X` / `su linkedin` | `su linkedin` |
| Link | qualsiasi URL | `https://linkedin.com/...` |
| Data | qualsiasi formato standard | `05/2025` |

**Esempio di input:**
```
ho pubblicato "Il mio primo tool Python" su linkedin,
link https://linkedin.com/post/123, maggio 2025
```

---

## File di output

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

## Requisiti

- Python 3.10+
- Solo libreria standard (`re`, `os`, `json`, `csv`), nessuna installazione richiesta

---

## Parte di una roadmap più ampia

Pulsar è stato costruito come progetto di apprendimento pratico durante il completamento di CS50P della Harvard University e la transizione verso lo sviluppo AI. Copre design orientato agli oggetti, regex, JSON, CSV, file I/O, design CLI e gestione degli errori, tutto dalla libreria standard di Python.

<br><br>

---
---

<a name="english"></a>

# Pulsar

**[🇮🇹 Italiano](#pulsar) | 🇬🇧 English**

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