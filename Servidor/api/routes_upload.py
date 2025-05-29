from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from databaseSE import SessionLocal
from modelsSSE import MushroomUser
from services.ia_service import prever_imagem
import os
import shutil
from uuid import uuid4

router = APIRouter()
UPLOAD_DIR = os.path.join("uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_imagem(
    file: UploadFile = File(...),
    usuario_id: int = Form(...)
):
    extensao = os.path.splitext(file.filename)[1].lower()
    if extensao not in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
        raise HTTPException(status_code=400, detail="Extensão de arquivo inválida.")

    nome_arquivo = f"{uuid4().hex}{extensao}"
    caminho_arquivo = os.path.join(UPLOAD_DIR, nome_arquivo)

    conteudo = await file.read()

    # Roda a IA
    try:
        scientific, common, accuracy = prever_imagem(conteudo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao classificar imagem: {e}")

    # Salva imagem no disco
    with open(caminho_arquivo, "wb") as buffer:
        buffer.write(conteudo)

    # Salva no banco
    session = SessionLocal()
    try:
        registro = MushroomUser(
            accuracy=accuracy,
            common_name=common,
            scientific_name=scientific,
            photo_path=caminho_arquivo,
            usuario_id=usuario_id
        )
        session.add(registro)
        session.commit()
        return {
            "message": "Imagem classificada e salva com sucesso",
            "scientific_name": scientific,
            "common_name": common,
            "accuracy": accuracy,
            "image_path": caminho_arquivo
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
