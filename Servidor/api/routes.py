from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from db.database import SessionLocal
from modelsSSE import Usuario
from pydantic import BaseModel
from modelsSE.request_model import UsuarioCreate
from modelsSE.response_model import UsuarioOut
import os
from uuid import uuid4

router = APIRouter()

avatar_padrao = r"C:\SeekMush\Servidor\uploads\avatars\default-avatar.jpg"

@router.post("/usuarios", response_model=UsuarioOut)
def criar_usuario(usuario: UsuarioCreate):
    session = SessionLocal()
    try:
        # Verifica se email já existe
        if session.query(Usuario).filter_by(email=usuario.email).first():
            raise HTTPException(status_code=400, detail="Email já cadastrado.")

        novo = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha, foto=avatar_padrao)
        session.add(novo)
        session.commit()
        session.refresh(novo)
        return novo
    finally:
        session.close()

@router.get("/usuarios", response_model=list[UsuarioOut])
def listar_usuarios():
    session = SessionLocal()
    try:
        return session.query(Usuario).all()
    finally:
        session.close()


class UsuarioLogin(BaseModel):
    email: str
    senha: str

@router.post("/login")
def login(dados: UsuarioLogin):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter_by(email=dados.email).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        if usuario.senha != dados.senha:
            raise HTTPException(status_code=401, detail="Senha incorreta.")
        return {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "ranque": usuario.ranque
        }
    finally:
        session.close()

@router.get("/usuarios/{usuario_id}")
def obter_usuario(usuario_id: int):
    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")
        return {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "foto": usuario.foto,
            "ranque": usuario.ranque,
            "ativo": usuario.ativo
        }
    finally:
        session.close()

UPLOAD_DIR = os.path.join("uploads", "avatars")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/usuarios/{usuario_id}/foto")
async def atualizar_foto(usuario_id: int, file: UploadFile = File(...)):
    extensao = os.path.splitext(file.filename)[1].lower()
    if extensao not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Formato inválido.")

    nome_arquivo = f"{uuid4().hex}{extensao}"
    caminho = os.path.join(UPLOAD_DIR, nome_arquivo)

    with open(caminho, "wb") as f:
        f.write(await file.read())

    caminho_relativo = f"/uploads/avatars/{nome_arquivo}"

    session = SessionLocal()
    try:
        usuario = session.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado.")

        usuario.foto = caminho_relativo
        session.commit()
        return {"foto": caminho_relativo}
    finally:
        session.close()