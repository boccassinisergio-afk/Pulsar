import re
import os
import json
import csv

# ------- FILES DEFINITION -------

data_dir = "data"
csv_projects = "projects.csv"
csv_skills = "skills.csv"
json_name = "data.json"
FIELDNAMES = ["sezione", "nome", "tipo", "piattaforma", "tecnologie", "argomento", "stato", "link", "data"]
SKILL_FIELDNAMES = ["tecnologia", "occorrenze"]

# -------- FILES INITIALIZE -------

def initialize_json():

    default_data = {"portfolio": {
                    "software": [],
                    "contenuti": []}
                    }
    
    if not os.path.exists(json_name):
        with open(json_name, "w") as file:
            json.dump(default_data, file, indent=4)

def initialize_csvs():
    if not os.path.exists(csv_projects):
        with open(csv_projects, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
    if not os.path.exists(csv_skills):
        with open(csv_skills, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=SKILL_FIELDNAMES)
            writer.writeheader()

# ------- MAIN --------

def main():
    initialize_json()
    initialize_csvs()
    patterns = load_all_patterns(data_dir)

    while True:
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("            PULSAR        ")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("1. Aggiungi software")
        print("2. Aggiungi contenuto")
        print("3. Esporta CSV")
        print("4. Leggi report")
        print("5. Esci")

        scelta = input("\nScelta: ").strip()
        
        if scelta == "1":
            print("\nDescrivi il software in testo libero.")
            print("Suggerimento: includi nome (chiamato X), tecnologie (python, json...),")
            print("stato (completato / in corso), link (https://...)")
            print("Esempio: ho creato un tool chiamato Signal usando python e json,")
            print("è completato, link https://github.com/boccassinisergio-afk/Pulsar\n")
            string = input("→ ")
            dati_fissi = extract_data(string)
            dati_pattern = extract(string, patterns)
            dati_fissi["tecnologie"] = [
                tech
                for categoria in dati_pattern.values()
                for tech in categoria
            ]
            save_portfolio(dati_fissi, "software")
        elif scelta == "2":
            print("\nDescrivi il contenuto pubblicato.")
            print("Suggerimento: includi titolo tra virgolette, piattaforma (social LinkedIn),")
            print("data, link")
            print("Esempio: ho pubblicato \"Il mio primo tool Python\" su social linkedin,")
            print("link https://linkedin.com/post/123\n")
            string = input("→ ")
            dati_fissi = extract_data(string)
            dati_pattern = extract(string, patterns)
            dati_fissi["argomento"] = dati_pattern.get("techs", [])
            save_portfolio(dati_fissi, "contenuti")
        elif scelta == "3":
            export_csv()
        elif scelta == "4":
            read_report()
        elif scelta == "5":
            break
        else:
            print("Scelta non valida.")

# ------    EXTRACTOR    ---------

def extract_data(testo):
    data_to_export = {}

    string = testo.lower().strip()

    link_str = re.search(r"https?://[^\s]+", string)
    if link_str:
        data_to_export.update({"link":link_str.group()})
    
    piattaforma = re.search(r"(?:piattaforma|social)\s+(\w+)", string)
    if not piattaforma:
        piattaforma_fallback = re.search(r"\bsu\s+(linkedin|twitter|x|instagram)\b", string)
        if piattaforma_fallback:
            data_to_export.update({"piattaforma": piattaforma_fallback.group(1)})
    if piattaforma:
        data_to_export.update({"piattaforma": piattaforma.group(1)})

    status = re.search(r"\b(completato|in corso|wip|terminato|finito)\b", string)
    if status:
        data_to_export.update({"stato":status.group(1)})

    nome = re.search(r"(?:chiamato|si chiama|nome)\s+([a-zA-Z0-9_\- ]+)", string)
    if nome:
        data_to_export.update({"nome":nome.group(1)})
    
    titolo = re.search(r'"([^"]+)"', string)
    if not titolo:
        titolo_fallback = re.search(r"(?:titolo|post)[:\s]+(\w[\w\s]+?)(?:\s+su\s|\s+in\s|$)", string)
        if titolo_fallback:
            data_to_export.update({"titolo":titolo_fallback.group(1)})
    if titolo:
        data_to_export.update({"titolo":titolo.group(1)})

    data = re.search(r"(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})|(\d{2}[\/\-]\d{4})|(\d{4}[\/\-]\d{2})", string)
    if not data:
        data_fallback = re.search(r"((?:gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+\d{4})", string)
        if data_fallback:
            data_to_export.update({"data":data_fallback.group()})
    if data:
        data_to_export.update({"data":data.group()})

    tipo = re.search(r"\b(tool|progetto)\b", string)
    if tipo:
        data_to_export.update({"tipo":tipo.group(1)})

    return data_to_export

# ------- STORAGE ---------

def save_portfolio(dati, sezione):
    try:
        with open(json_name, "r") as file_old:
            existing_data = json.load(file_old)

        existing_data["portfolio"][sezione].append(dati)

        with open(json_name, "w") as file:
            json.dump(existing_data, file, indent=4)

        print(f"\n✓ Entry salvata in '{sezione}' correttamente.")

    except FileNotFoundError:
        print("Errore: file non trovato.")
        return 
    except json.JSONDecodeError:
        print("Errore: file JSON corrotto.")
        return
    except PermissionError:
        print("Errore: file in uso da un altro processo.")
        return


# -------- EXPORT ----------

def export_csv():

    skills = {}
    try:
        with open(json_name, "r") as existing_file:
            data = json.load(existing_file)
        with open(csv_projects, "a", newline="") as csv_pj:
            writer = csv.DictWriter(csv_pj, fieldnames=FIELDNAMES, extrasaction='ignore')

            for entry in data['portfolio']['software']:
                row = dict(entry)
                row['sezione'] = 'software'   
                row['tecnologie'] = ', '.join(row.get('tecnologie', []))
                writer.writerow(row)

            for entry in data['portfolio']['contenuti']:
                row = dict(entry)
                row['sezione'] = 'contenuti'
                row['nome'] = row.pop('titolo', '') 
                writer.writerow(row)

        with open(csv_skills, "a", newline="") as csv_sk:
            writer = csv.DictWriter(csv_sk, fieldnames=SKILL_FIELDNAMES, extrasaction='ignore')

            # ------ OCCORRENZE -------

            for row in data['portfolio']['software']:
                for tecnologia in row.get('tecnologie', []):
                    skills[tecnologia] = skills.get(tecnologia, 0) + 1
            for tecnologia, occorrenze in skills.items():
                writer.writerow({"tecnologia": tecnologia, "occorrenze": occorrenze})

    except FileNotFoundError:
        print("Errore: file non trovato.")
        return 
    except json.JSONDecodeError:
        print("Errore: file JSON corrotto.")
        return 
    except PermissionError:
        print("Errore: file in uso da un altro processo.")
        return
    
    print(f"\n✓ Esportazione completata:")
    print(f"  → {csv_projects}")
    print(f"  → {csv_skills}")

# ----------- READ REPORT -------------

def read_report():
    try:
        with open(json_name, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Errore: file non trovato.")
        return
    except json.JSONDecodeError:
        print("Errore: file JSON corrotto.")
        return
    print("\n━━━━━━━━━━━━━━━ SOFTWARE ━━━━━━━━━━━━━━━")
    for entry in data['portfolio']['software']:
        tecnologie = ', '.join(entry.get('tecnologie', []))
        print(f"Data: {entry.get('data','N/D')} | Nome: {entry.get('nome','N/D')} | Tecnologie: {tecnologie} | Link: {entry.get('link','N/D')}")
    print("\n━━━━━━━━━━━━━━━ CONTENUTI ━━━━━━━━━━━━━━━")
    for entry in data['portfolio']['contenuti']:
        print(f"Data: {entry.get('data','N/D')} | Titolo: {entry.get('titolo','N/D')} | Piattaforma: {entry.get('piattaforma','N/D')} | Link: {entry.get('link','N/D')}")

# -------- DYNAMIC DICT SECTION -------------- NUOVA

def load_all_patterns(data_dir):

    if not os.path.exists(data_dir):
        print(f"[WARN] cartella '{data_dir}' non trovata, nessun pattern caricato.")
        return {}
    
    patterns = {}

    for filename in os.listdir(data_dir):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(data_dir, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[WARN] {filename} ignorato: {e}")
            continue

        label = data["label"]
        keywords = data["keywords"]

        keywords_sorted = sorted(keywords, key=len, reverse=True)

        pattern_str = r"\b(" + "|".join(re.escape(k) for k in keywords_sorted) + r")\b"
        patterns[label] = re.compile(pattern_str, re.IGNORECASE)

    return patterns

def extract(text, patterns):
    results = {}

    for label, compiled_pattern in patterns.items():
        matches = compiled_pattern.findall(text)
        results[label] = sorted(set(m.lower() for m in matches))

    return results


main()


    