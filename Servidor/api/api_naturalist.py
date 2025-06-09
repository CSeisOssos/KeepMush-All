import requests
from fastapi import APIRouter, HTTPException
import re
import json
from pathlib import Path
import pandas as pd
from .api_client import api_client
from services.ia_service import buscar_descricao_wikipedia
from db.database import SessionLocal  # Importe sua sessão do banco
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import urllib.parse
from config.settings import DB_URI

router = APIRouter()

# 1. CARREGAMENTO DOS DADOS
CSV_PATH = r"C:\SeekMush\Dataset\Fotos + Nomes\translated_names.csv"

# Carrega CSV
try:
    df = pd.read_csv(CSV_PATH)
    if df.shape[1] == 1:
        df = pd.read_csv(CSV_PATH, sep=';')
except Exception as e:
    raise RuntimeError(f"Erro ao carregar CSV: {e}")

df = df.dropna(subset=["scientific_name"])
df["scientific_name"] = df["scientific_name"].str.strip().str.lower()
df_sorted = df.sort_values("scientific_name").reset_index(drop=True)

# Dicionário para busca flexível
NOMES_CIENTIFICOS = {
    nome.lower().replace(" ", "_").replace("-", "_"): nome
    for nome in df_sorted["scientific_name"].unique()
}

# Carrega palavras-chave
def carregar_palavras_chave():
    try:
        with open(Path(__file__).parent / "palavras_chave.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar palavras-chave: {e}")
        return {}

PALAVRAS_CHAVE = carregar_palavras_chave()

def get_db_connection():
    """Converte a DB_URI para formato compatível com psycopg2"""
    db_uri = "postgresql+psycopg2://servidor:servidor123@localhost:5432/SeekMushBD"
    
    # Parse da URL de conexão
    parsed = urllib.parse.urlparse(db_uri)
    
    # Remove o '+psycopg2' do scheme
    dbname = parsed.path[1:]  # Remove a barra inicial
    conn_string = f"""
        host={parsed.hostname}
        dbname={dbname}
        user={parsed.username}
        password={parsed.password}
        port={parsed.port}
    """
    return conn_string

def buscar_id_especie(nome_cientifico: str) -> int:
    """Busca o ID real no PostgreSQL"""
    conn = None
    try:
        conn = psycopg2.connect(get_db_connection())
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id FROM public.mushrooms
                WHERE scientific_name ILIKE %s
                LIMIT 1
            """, (nome_cientifico,))
            resultado = cur.fetchone()
            return resultado['id'] if resultado else None
    except Exception as e:
        print(f"Erro ao buscar ID: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Função de destaque
def destacar_palavras_chave(texto: str) -> str:
    if not texto:
        return "Descrição não disponível."
    
    todas_palavras = {}
    for categoria in PALAVRAS_CHAVE.values():
        if isinstance(categoria, dict):
            for subcategoria in categoria.values():
                if isinstance(subcategoria, dict):
                    todas_palavras.update(subcategoria)
                else:
                    todas_palavras.update(categoria)
                    break
    
    for palavra, substituto in todas_palavras.items():
        texto = re.sub(rf"\b({re.escape(palavra)})\b", substituto, texto, flags=re.IGNORECASE)
    return texto

# 2. ENDPOINT COM ID DO BANCO
@router.get("/especie/{nome}")
async def buscar_especie(nome: str):
    session = SessionLocal()
    try:
        # Normalização do nome
        nome_csv = nome.strip().lower().replace(" ", "_").replace("-", "_")
        if nome_csv not in NOMES_CIENTIFICOS:
            raise ValueError(f"Espécie '{nome}' não encontrada")
        
        nome_api = NOMES_CIENTIFICOS[nome_csv].replace("_", " ")
        scientific_name = NOMES_CIENTIFICOS[nome_csv].replace("_", " ").title()
        
        # Busca ID no banco
        id_especie = buscar_id_especie(scientific_name)
        if id_especie is None:
            raise ValueError(f"Espécie '{scientific_name}' não encontrada no banco")

        
        # Consulta às APIs
        api_data = api_client.buscar_dados_especie(nome_api)
        common_name = df_sorted[df_sorted["scientific_name"] == NOMES_CIENTIFICOS[nome_csv]]["common_name"].iloc[0]
        
        # Busca descrição
        descricao = buscar_descricao_wikipedia(scientific_name)
        if not descricao and api_data.get("wikipedia_url"):
            try:
                pt_wiki = api_data["wikipedia_url"].replace("en.wikipedia", "pt.wikipedia")
                descricao = buscar_descricao_wikipedia(pt_wiki.split("/")[-1])
            except:
                pass
        
        return {
            "success": True,
            "data": {
                "id": id_especie,  # ID REAL do banco
                "scientific_name": scientific_name,
                "common_name": common_name,
                "taxonomy": api_data.get("taxonomy", {}),
                "description": destacar_palavras_chave(descricao or "Descrição não disponível"),
                "inaturalist_link": api_data.get("inaturalist_link", ""),
                "image_url": api_data.get("inaturalist", {}).get("default_photo", {}).get("medium_url", "")
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}. Nomes válidos: {list(NOMES_CIENTIFICOS.values())[:10]}..."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na pesquisa: {str(e)}"
        )
    finally:
        session.close()