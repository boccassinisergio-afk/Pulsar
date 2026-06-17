import re
import os
import json
import csv

class Entry:

    """Base class representing a portfolio entry with a date and a link.

    Attributes:
        data (str): The date associated with the entry.
        link (str): The URL related to the entry.
    """

    def __init__(self, data: str, link: str) -> None:
        self.data = data
        self.link = link

    def to_dict(self) -> dict[str, str]:

        """Serialize base entry fields to a dictionary.

        Returns:
            dict: A dictionary with 'data' and 'link' keys.
        """

        return {"data": self.data,
                "link": self.link
                }


class Software(Entry):

    """Represents a software project entry in the PULSAR portfolio.

    Inherits from Entry and adds project-specific metadata.

    Attributes:
        tipo (str): The project type (e.g. 'tool', 'progetto').
        nome (str): The project name.
        tecnologie (list[str]): Technologies used in the project.
        stato (str): Current project status (e.g. 'completato', 'in corso').
    """

    def __init__(self, data: str, tipo: str, nome: str, tecnologie: list[str], stato: str, link: str) -> None:
        super().__init__(data, link)
        self.tipo = tipo
        self.nome = nome
        self.tecnologie = tecnologie
        self.stato = stato


    def to_dict(self) -> dict[str, str | list[str]]:

        """Serialize the software entry to a dictionary, extending the base fields.

        Returns:
            dict: A dictionary with all Entry fields plus tipo, nome, tecnologie, and stato.
        """

        inherited_dict = super().to_dict()
        inherited_dict['tipo'] = self.tipo 
        inherited_dict['nome'] = self.nome
        inherited_dict['tecnologie'] = self.tecnologie
        inherited_dict['stato'] = self.stato
        return inherited_dict 
    
    @classmethod
    def from_dict(cls, incoming_dict: dict[str, str | list[str]]) -> "Software":

        """Create a Software instance from a dictionary, using .get() for safe access.

        Args:
            incoming_dict (dict): A dictionary with software entry fields.

        Returns:
            Software: A new instance populated with dictionary data.
        """

        return cls(data = incoming_dict.get('data', ""),
                   tipo = incoming_dict.get('tipo', ""),
                   nome = incoming_dict.get('nome', ""),
                   tecnologie = incoming_dict.get('tecnologie', []),
                   stato = incoming_dict.get('stato', ""),
                   link = incoming_dict.get('link', "")
                   )

    def __str__(self) -> str:

        """Return a formatted single-line string representation of the software entry."""

        return f"Data: {self.data} | Tipo: {self.tipo} | Nome: {self.nome} | Tecnologie: {', '.join(self.tecnologie)} | Stato: {self.stato} | Link: {self.link}"

class Contenuto(Entry):

    """Represents a published content entry in the PULSAR portfolio.

    Inherits from Entry and adds content-specific metadata.

    Attributes:
        titolo (str): The content title.
        argomento (list[str]): Topics or technologies covered.
        piattaforma (str): The platform where the content was published (e.g. 'linkedin').
    """

    def __init__(self, data: str, titolo: str, argomento: list[str], piattaforma: str, link: str) -> None:
        super().__init__(data, link)
        self.titolo = titolo
        self.argomento = argomento
        self.piattaforma = piattaforma 

    def to_dict(self) -> dict[str, str | list[str]]:

        """Serialize the content entry to a dictionary, extending the base fields.

        Returns:
            dict: A dictionary with all Entry fields plus titolo, argomento, and piattaforma.
        """

        inherited_dict = super().to_dict()
        inherited_dict['titolo'] = self.titolo
        inherited_dict['argomento'] = self.argomento
        inherited_dict['piattaforma'] = self.piattaforma
        return inherited_dict
    
    @classmethod
    def from_dict(cls, incoming_dict: dict[str, str | list[str]]) -> "Contenuto":

        """Create a Contenuto instance from a dictionary, using .get() for safe access.

        Args:
            incoming_dict (dict): A dictionary with content entry fields.

        Returns:
            Contenuto: A new instance populated with dictionary data.
        """

        return cls(
            data = incoming_dict.get('data', ""),
            titolo = incoming_dict.get('titolo', ""),
            argomento = incoming_dict.get('argomento', []),
            piattaforma = incoming_dict.get('piattaforma', ""),
            link = incoming_dict.get('link', "")
        )

    def __str__(self) -> str:

        """Return a formatted single-line string representation of the content entry."""

        return f"Data: {self.data} | Titolo: {self.titolo} | Argomento: {', '.join(self.argomento)} | Piattaforma: {self.piattaforma} | Link: {self.link}"
    
# ------- FILES DEFINITION -------

data_dir = "data"
csv_projects = "projects.csv"
csv_skills = "skills.csv"
json_name = "data.json"
FIELDNAMES = ["sezione", "nome", "tipo", "piattaforma", "tecnologie", "argomento", "stato", "link", "data"]
SKILL_FIELDNAMES = ["tecnologia", "occorrenze"]

# -------- FILES INITIALIZE -------

def initialize_json() -> None:

    """Create the JSON portfolio file with default structure if it does not already exist."""

    default_data = {"portfolio": {
                    "software": [],
                    "contenuti": []}
                    }
    
    if not os.path.exists(json_name):
        with open(json_name, "w") as file:
            json.dump(default_data, file, indent=4)

def initialize_csvs() -> None:

    """Create the projects and skills CSV files with headers if they do not already exist."""

    if not os.path.exists(csv_projects):
        with open(csv_projects, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
    if not os.path.exists(csv_skills):
        with open(csv_skills, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=SKILL_FIELDNAMES)
            writer.writeheader()


def main() -> None:

    """Run the Pulsar CLI loop: initialize storage, load patterns, and dispatch user actions."""

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
            
            temporary_entry = Software.from_dict(dati_fissi)
            save_portfolio(temporary_entry, "software")

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
            temporary_entry = Contenuto.from_dict(dati_fissi)
            save_portfolio(temporary_entry, "contenuti")

        elif scelta == "3":
            export_csv()
        elif scelta == "4":
            read_report()
        elif scelta == "5":
            break
        else:
            print("Scelta non valida.")

# ------    EXTRACTOR    ---------

def extract_data(testo: str) -> dict[str, str]:

    """Extract structured fields from a free-text string using regex patterns.

    Parses the input for known fields including link, platform, status, name,
    title, date, and type. Falls back to secondary patterns when primary ones fail.

    Args:
        testo (str): The raw free-text input from the user.

    Returns:
        dict: A dictionary of extracted fields. Keys vary based on what was found
        (e.g. 'link', 'stato', 'nome', 'titolo', 'data', 'tipo', 'piattaforma').
    """

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

    nome = re.search(r"(?:chiamato|si chiama|nome)\s+([a-zA-Z0-9_\-]+)", string)
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

# -------- DYNAMIC DICT SECTION --------------

def load_all_patterns(data_dir: str) -> dict[str, re.Pattern[str]]:

    """Load and compile regex patterns from all JSON files in the given directory.

    Each JSON file must contain a 'label' (str) and a 'keywords' (list[str]) field.
    Keywords are sorted by length descending to prevent partial matches, then compiled
    into a single case-insensitive pattern per category.

    Args:
        data_dir (str): Path to the directory containing keyword JSON files.

    Returns:
        dict: A dictionary mapping each label to its compiled re.Pattern.
    """

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

def extract(text: str, patterns: dict[str, re.Pattern[str]]) -> dict[str, list[str]]:

    """Apply compiled patterns to a text and return matched keywords by category.

    Args:
        text (str): The input text to search.
        patterns (dict): Compiled patterns keyed by category label.

    Returns:
        dict: A dictionary mapping each label to a sorted list of unique lowercase matches.
    """

    results = {}

    for label, compiled_pattern in patterns.items():
        matches = compiled_pattern.findall(text)
        results[label] = sorted(set(m.lower() for m in matches))

    return results

# ------- STORAGE ---------

def save_portfolio(dati: Entry, sezione: str) -> None:

    """Append a portfolio entry to the appropriate section of the JSON file.

    Args:
        dati (Entry): A Software or Contenuto instance to save.
        sezione (str): The portfolio section to append to ('software' or 'contenuti').
    """

    temporary_entry = dati.to_dict()

    try:
        with open(json_name, "r") as file_old:
            existing_data = json.load(file_old)

        existing_data["portfolio"][sezione].append(temporary_entry)

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

def export_csv() -> None:

    """Export all portfolio entries to CSV files.

    Writes software and content entries to projects.csv, and computes
    technology occurrence counts for skills.csv.
    """

    skills = {}
    try:
        with open(json_name, "r") as existing_file:
            data = json.load(existing_file)
        with open(csv_projects, "w", newline="") as csv_pj:
            writer = csv.DictWriter(csv_pj, fieldnames=FIELDNAMES, extrasaction='ignore')
            writer.writeheader()

            for entry in data['portfolio']['software']:
                row = dict(entry)
                row['sezione'] = 'software'   
                row['tecnologie'] = ', '.join(row.get('tecnologie', []))
                writer.writerow(row)

            for entry in data['portfolio']['contenuti']:
                row = dict(entry)
                row['sezione'] = 'contenuti'
                row['nome'] = row.pop('titolo', '') 
                row['argomento'] = ', '.join(row.get('argomento', []))
                writer.writerow(row)

        with open(csv_skills, "w", newline="") as csv_sk:
            writer = csv.DictWriter(csv_sk, fieldnames=SKILL_FIELDNAMES, extrasaction='ignore')
            writer.writeheader()

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

def read_report() -> None:

    """Read and print all portfolio entries from the JSON file, grouped by section."""

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
        dict_to_object = Software.from_dict(entry)
        print(dict_to_object)
    print("\n━━━━━━━━━━━━━━━ CONTENUTI ━━━━━━━━━━━━━━━")
    for entry in data['portfolio']['contenuti']:
        dict_to_object = Contenuto.from_dict(entry)
        print(dict_to_object)


if __name__ == "__main__":
    main()

    