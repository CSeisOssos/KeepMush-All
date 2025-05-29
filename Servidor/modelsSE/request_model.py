from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class MushroomUpload(BaseModel):
    accuracy: float
    common_name: str
    scientific_name: str
    usuario_id: int
