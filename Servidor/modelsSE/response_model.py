from pydantic import BaseModel

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool
    ranque: int
    foto: str 

    class Config:
        orm_mode = True
