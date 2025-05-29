import os

CAMINHO_PRINCIPAL = r"C:\SeekMush\Dataset\Fotos + Nomes\Dataset Científico"

def verificar_subpastas(caminho_base):
    print(f"Verificando subpastas dentro de: {caminho_base}\n")

    for especie in os.listdir(caminho_base):
        caminho_especie = os.path.join(caminho_base, especie)

        if os.path.isdir(caminho_especie):
            subpastas = [p for p in os.listdir(caminho_especie)
                         if os.path.isdir(os.path.join(caminho_especie, p))]

            if subpastas:
                print(f"🟡 '{especie}' contém subpastas: {subpastas}")

    print("\nVerificação concluída.")

if __name__ == "__main__":
    verificar_subpastas(CAMINHO_PRINCIPAL)
