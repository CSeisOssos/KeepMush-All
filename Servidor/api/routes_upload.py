from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from databaseSE import SessionLocal
from modelsSSE import MushroomUser
from services.ia_service import prever_imagem
import os
import shutil
from uuid import uuid4
import json
from .api_client import api_client

router = APIRouter()
UPLOAD_DIR = os.path.join("uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def buscar_descricao_fallback(nome_cientifico: str):
    """Fallback para buscar descrição se não vier da IA"""
    try:
        # Tenta a API novamente se necessário
        api_data = api_client.buscar_dados_especie(nome_cientifico)
        return api_data.get("description", "Descrição não disponível.")
    except:
        return "Descrição não disponível."

@router.post("/upload")
async def upload_imagem(
    file: UploadFile = File(...),
    usuario_id: int = Form(...)
):
    session = SessionLocal()
    try:
        # Verificação da extensão do arquivo
        extensao = os.path.splitext(file.filename)[1].lower()
        if extensao not in [".jpg", ".jpeg", ".png", ".bmp", ".gif"]:
            raise HTTPException(status_code=400, detail="Extensão de arquivo inválida.")

        conteudo = await file.read()
        photo_path = os.path.join(UPLOAD_DIR, f"{uuid4().hex}{extensao}")
        
        
        # Processamento com IA
        resultado_ia = prever_imagem(conteudo, usuario_id, photo_path)
        
        # Debug: verifique se a descrição está vindo
        print(f"Descrição recebida da IA: {resultado_ia.get('description')}")

        # Salvar apenas os dados essenciais no banco
        session = SessionLocal()
        registro = MushroomUser(
            accuracy=resultado_ia["accuracy"],
            common_name=resultado_ia["common_name"],
            scientific_name=resultado_ia["scientific_name"],
            photo_path=photo_path,
            usuario_id=usuario_id,
            especie_id=resultado_ia.get("especie_id"),  # ID REAL do banco
        )
        
        session.add(registro)
        session.commit()
        
        # Escreve o arquivo após confirmar o BD
        with open(registro.photo_path, "wb") as buffer:
            buffer.write(conteudo)

        # Garantir que description existe no retorno
        descricao = resultado_ia.get("description")
        if not descricao:
            descricao = await buscar_descricao_fallback(resultado_ia["scientific_name"])
        

        # Monta a resposta com todos os dados (incluindo taxonomia e descrição)
        return {
            "success": True,
            "data": {
                "id": registro.id,
                "usuario_id": registro.usuario_id,
                "especie_id": resultado_ia["especie_id"],  # ID REAL do banco
                "scientific_name": registro.scientific_name,
                "common_name": registro.common_name,
                "accuracy": registro.accuracy,
                "image_url": f"/uploads/{os.path.basename(registro.photo_path)}",
                "taxonomy": resultado_ia.get("taxonomy", {}),  # Da IA/API externa
                "description": resultado_ia.get("description", ""),  # Da IA/API externa
                "inaturalist_link": resultado_ia.get("inaturalist_link", "")
            }
        }

    except Exception as e:
        if session:  # Verifica se session foi criada
            session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
    finally:
        if session:  # Verifica se session foi criada
            session.close()