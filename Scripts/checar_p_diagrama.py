import os

def listar_estrutura(pasta_raiz, prefixo=''):
    """Lista recursivamente a estrutura de pastas e arquivos de forma hierárquica."""
    conteudo = sorted(os.listdir(pasta_raiz))
    total = len(conteudo)

    for i, nome in enumerate(conteudo):
        caminho_completo = os.path.join(pasta_raiz, nome)
        is_ultimo = i == total - 1

        if os.path.isdir(caminho_completo):
            print(f"{prefixo}└── " if is_ultimo else f"{prefixo}├── ", end='')
            print(f"[{nome}]")
            novo_prefixo = prefixo + ("    " if is_ultimo else "│   ")
            listar_estrutura(caminho_completo, novo_prefixo)
        else:
            print(f"{prefixo}└── " if is_ultimo else f"{prefixo}├── ", end='')
            print(nome)

# Caminho da pasta principal que deseja mapear
PASTA_PRINCIPAL = r"C:\SeekMush"

print(f"📁 Estrutura de diretórios em: {PASTA_PRINCIPAL}\n")
listar_estrutura(PASTA_PRINCIPAL)
