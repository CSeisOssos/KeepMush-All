# db/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from database import Base

# Classe para armazenar os usuários do sistema e suas respectivas informações

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    foto = Column(String, nullable=True)
    
    # Ranque: 1 - iniciante, 2 - explorador, etc.
    ranque = Column(Integer, default=1)

def __init__(self, nome, email, senha, foto):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = True
        self.ranque = 1
        self.foto = foto
        
# Classe para armazenar as imagens de cogumelos enviadas pelos usuários e suas respectivas informações    

class MushroomUser(Base):
    __tablename__ = "imagens_dos_usuarios"

    accuracy = Column(Float, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    common_name = Column(String)
    scientific_name = Column(String)
    photo_path = Column(String)

    def __init__(self, photo_path, scientific_name, common_name, accuracy, usuario_id):
        self.photo_path = photo_path
        self.scientific_name = scientific_name
        self.accuracy = accuracy
        self.common_name = common_name
        self.usuario_id = usuario_id


