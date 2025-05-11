from pathlib import Path
import re
from urllib.parse import urlparse

# Fichier d'entrée et de sortie
input_files = [
    Path("nicoles_masterUBL.txt"),
    Path("nicoles_ubl.txt"),
    Path("combined_list.txt"),
]
output_folder = Path("ADP")


def extract_domain(line: str) -> str:
    line = line.strip()

    # Ignore commentaires/lignes vides
    if not line or line.startswith("#"):
        return ""

    # Nettoyage avant parsing
    line = re.sub(r"^\*+://", "", line)  # *://
    line = re.sub(r"^\*+\.", "", line)  # *.
    line = line.split("/")[0]  # enlève le chemin

    # Ajoute un protocole pour urlparse si besoin
    parsed = urlparse("http://" + line if "://" not in line else line)
    domain = parsed.netloc or parsed.path.split("/")[0]

    domain = domain.lower().strip()

    # Supprime les ports ou identifiants éventuels
    domain = domain.split("@").pop()
    domain = domain.split(":")[0]

    # Autorise IP OU domaine valide
    if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", domain) and not re.match(r"^(\d{1,3}\.){3}\d{1,3}$", domain):
        print(f"\u26d4 Ignored (non valid) : {line} -> {domain}")
        return ""

    return f"||{domain}^"


def main():
    output_folder.mkdir(parents=True, exist_ok=True)

    for input_file in input_files:
        output_file = output_folder / f"{input_file.stem}.txt"
        if not input_file.exists():
            print(f"Fichier {input_file} introuvable.")
            continue

        with input_file.open(encoding="utf-8") as f:
            lines = f.readlines()

        converted = [extract_domain(line) for line in lines]
        filtered = sorted(set(line for line in converted if line))

        output_file.write_text("\n".join(filtered), encoding="utf-8")
        print(f"\u2705 List converted into {output_file} ({len(filtered)} domaines)")


if __name__ == "__main__":
    main()
