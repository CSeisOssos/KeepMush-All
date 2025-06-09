import tensorflow as tf
import numpy as np
from PIL import Image
import io
import pandas as pd
import requests
from fastapi import HTTPException
import sys
from pathlib import Path
from fastapi import APIRouter, Form, UploadFile, File
from contextlib import asynccontextmanager
import re
import json
import psycopg2
import urllib.parse
from psycopg2.extras import RealDictCursor
from config.settings import DB_URI

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.api_client import api_client

router = APIRouter()

@asynccontextmanager
async def lifespan(app):
    # Inicialização
    yield
    # Limpeza
    if hasattr(api_client, '__del__'):
        api_client.__del__()


CSV_PATH = r"C:\SeekMush\Dataset\Fotos + Nomes\translated_names.csv"
WIKIPEDIA_API_URL = "https://pt.wikipedia.org/w/api.php"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Configuração inicial (mantida igual)
try:
    df = pd.read_csv(CSV_PATH)
    if df.shape[1] == 1:
        df = pd.read_csv(CSV_PATH, sep=';')
except Exception as e:
    raise RuntimeError(f"Erro ao carregar CSV: {e}")

# Processamento do DataFrame (mantido igual)
df = df.dropna(subset=["scientific_name"])
df["scientific_name"] = df["scientific_name"].str.strip()
df["common_name"] = df["common_name"].str.strip()
df_sorted = df.sort_values("scientific_name").reset_index(drop=True)

print(f">>> CSV carregado: {len(df_sorted)} classes científicas")

CLASSES = df_sorted["scientific_name"].tolist()
COMMON_NAMES = dict(zip(df_sorted["scientific_name"], df_sorted["common_name"]))

# Carrega palavras-chave
def carregar_palavras_chave():
    try:
        with open(Path(__file__).parent / "../api/palavras_chave.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar palavras-chave: {e}")
        return {}

PALAVRAS_CHAVE = carregar_palavras_chave()

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

def get_db_connection():
    """Converte a DB_URI para formato compatível com psycopg2"""
    db_uri = DB_URI if 'DB_URI' in globals() else "postgresql+psycopg2://servidor:servidor123@localhost:5432/SeekMushBD"
    parsed = urllib.parse.urlparse(db_uri)
    dbname = parsed.path[1:]
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

# Carregamento do modelo (mantido igual)
MODEL_PATH = r"C:\SeekMush\models\V2.1TF.keras"
model = tf.keras.models.load_model(MODEL_PATH)

def buscar_descricao_wikipedia(nome_cientifico: str) -> str:
    """Busca a descrição da espécie na Wikipedia (função mantida igual)"""
    try:
        params = {
            "action": "query",
            "format": "json",
            "titles": nome_cientifico,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": True
        }
        
        response = requests.get(
            WIKIPEDIA_API_URL,
            params=params,
            timeout=5,
            headers={"User-Agent": "SeekMushBot/1.0"}
        )
        response.raise_for_status()
        
        dados = response.json()
        pagina = next(iter(dados["query"]["pages"].values()))
        return pagina.get("extract", "").strip()
        
    except Exception:
        return ""

def salvar_imagem_usuario(usuario_id: int, scientific_name: str, common_name: str, accuracy: float, photo_path: str, especie_id: int) -> int:
    """Salva os dados da imagem enviada pelo usuário e retorna o id da imagem"""
    conn = None
    try:
        conn = psycopg2.connect(get_db_connection())
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO imagens_dos_usuarios (usuario_id, scientific_name, common_name, accuracy, photo_path, especie_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (usuario_id, scientific_name, common_name, accuracy, photo_path, especie_id))
            id_imagem = cur.fetchone()[0]
            conn.commit()
            return id_imagem
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}")
        return None
    finally:
        if conn:
            conn.close()

def prever_imagem(imagem_bytes: bytes, usuario_id: int, photo_path: str) -> dict:
    """Função principal que integra IA + API externa"""
    try:
        # 1. Processamento da imagem 
        image = Image.open(io.BytesIO(imagem_bytes)).convert("RGB").resize((256, 256))
        array = np.expand_dims(np.array(image) / 255.0, axis=0)
        pred = model.predict(array, verbose=0)[0]

        # 2. Obter classificação básica
        idx = int(np.argmax(pred))
        if idx >= len(CLASSES):
            raise ValueError("Índice de classe inválido")

        scientific = CLASSES[idx]
        common = COMMON_NAMES.get(scientific, "Unknown")
        accuracy = float(pred[idx])

        # 3. Consulta à API externa (usando o cliente existente)
        api_data = api_client.buscar_dados_especie(scientific)
        
        # 4. Buscar descrição (mantendo a lógica original)
        descricao = buscar_descricao_wikipedia(scientific)
        descricao_destacada = destacar_palavras_chave(descricao or api_data.get("description", "Descrição não disponível."))

        # 5. Buscar ID da espécie
        especie_id = buscar_id_especie(scientific)

        # 6. Salvar imagem no banco e obter id da imagem
        id_imagem = salvar_imagem_usuario(usuario_id, scientific, common, accuracy, photo_path, especie_id)

        # 7. Montagem da resposta final
        return {
            "id": id_imagem,  # ID da imagem enviada
            "especie_id": especie_id,  # ID REAL da espécie no banco
            "usuario_id": usuario_id,
            "scientific_name": scientific,
            "common_name": common,
            "accuracy": accuracy,
            "taxonomy": api_data.get("taxonomy", {}),
            "inaturalist_link": api_data.get("inaturalist_link", ""),
            "description": descricao_destacada,
            "photo_path": photo_path  # Caminho da foto enviada
        }

    except requests.exceptions.RequestException as e:
        print(f"Erro na API: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail="Serviço externo indisponível"
        )
        
    except Exception as e:
        print(f"Erro no processamento: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )
    
@router.post("/prever/")
async def prever(
    usuario_id: int = Form(...),
    photo_path: str = Form(...),
    imagem: UploadFile = File(...),
    especie_id: int = Form(...)
):
    try:
        imagem_bytes = await imagem.read()
        resultado = prever_imagem(imagem_bytes, usuario_id, photo_path, especie_id)
        return resultado
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")