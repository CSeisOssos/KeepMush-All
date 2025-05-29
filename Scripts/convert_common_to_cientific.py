import requests
import csv

def get_scientific_name(common_name):
    # Substitui underline por espaço
    name_query = common_name.replace("_", " ")

    # Consulta à API do iNaturalist
    url = "https://api.inaturalist.org/v1/search"
    params = {
        "q": name_query,
        "sources": "taxa",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json().get("results", [])
        for item in results:
            if item["record"]["rank"] in ["species", "subspecies", "variety"]:
                sci_name = item["record"]["name"]
                return sci_name
    return None

def convert_names(input_txt, output_csv):
    with open(input_txt, "r") as f:
        common_names = [line.strip() for line in f.readlines() if line.strip()]

    translated = []
    for name in common_names:
        scientific_name = get_scientific_name(name)
        print(f"{name.replace('_', ' ')} → {scientific_name}")
        translated.append([name, scientific_name or "Not found"])

    # Salva em CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["common_name", "scientific_name"])
        writer.writerows(translated)

if __name__ == "__main__":
    convert_names(r"C:\SeekMush\Dataset\Fotos + Nomes\common_names.txt", "translated_names.csv")

