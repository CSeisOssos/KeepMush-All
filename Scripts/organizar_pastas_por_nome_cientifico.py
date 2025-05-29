import os
import shutil
import csv

# Caminhos
PASTA_ORIGEM = r"C:\SeekMush\Dataset\Fotos + Nomes\data"
PASTA_DESTINO = r"C:\SeekMush\Dataset\Fotos+ Nomes\Dataset Científico"
CSV_CAMINHO = r"C:\SeekMush\Dataset\Fotos + Nomes\translated_names.csv"

def organizar_pastas():
    if not os.path.exists(PASTA_DESTINO):
        os.makedirs(PASTA_DESTINO)

    with open(CSV_CAMINHO, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            common_name = row["common_name"]
            scientific_name = row["scientific_name"]

            if not scientific_name or scientific_name.strip().lower() == "none":
                continue  # pula se o nome científico não foi encontrado

            pasta_origem = os.path.join(PASTA_ORIGEM, common_name)
            pasta_destino = os.path.join(PASTA_DESTINO, scientific_name.replace(" ", "_"))

            if os.path.exists(pasta_origem):
                print(f"Movendo '{pasta_origem}' para '{pasta_destino}'...")
                shutil.move(pasta_origem, pasta_destino)
            else:
                print(f"Pasta '{common_name}' não encontrada em {PASTA_ORIGEM}. Ignorando...")

    print("\nFinalizado! As pastas com nomes científicos foram movidas para:", PASTA_DESTINO)

if __name__ == "__main__":
    organizar_pastas()
