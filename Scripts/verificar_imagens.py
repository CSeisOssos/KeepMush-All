import os
from PIL import Image, UnidentifiedImageError

# Caminho base
BASE_DIR = r"C:\SeekMush\Dataset\Fotos + Nomes\Dataset Científico"

# Extensões válidas (todas em minúsculas)
EXTENSOES_VALIDAS = {'.jpeg', '.jpg', '.png', '.gif', '.bmp'}

# Relatórios
extensao_invalida = []
imagens_corrompidas = []

# Percorre todos os arquivos nas subpastas
for root, dirs, files in os.walk(BASE_DIR):
    for nome_arquivo in files:
        caminho_completo = os.path.join(root, nome_arquivo)
        extensao = os.path.splitext(nome_arquivo)[1].lower()

        # Verifica extensão
        if extensao not in EXTENSOES_VALIDAS:
            extensao_invalida.append(caminho_completo)
            continue

        # Verifica integridade da imagem
        try:
            with Image.open(caminho_completo) as img:
                img.verify()  # Testa se a imagem é legível
        except (UnidentifiedImageError, OSError, IOError):
            imagens_corrompidas.append(caminho_completo)

# Exibe o relatório
print("\n🔍 RELATÓRIO DE VERIFICAÇÃO DE IMAGENS\n")

print("📛 Arquivos com extensão inválida:")
if extensao_invalida:
    for path in extensao_invalida:
        print(" -", path)
else:
    print(" ✅ Nenhum encontrado.")

print("\n🛑 Imagens corrompidas ou ilegíveis:")
if imagens_corrompidas:
    for path in imagens_corrompidas:
        print(" -", path)
else:
    print(" ✅ Nenhuma imagem corrompida detectada.")
