import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Caminho base das imagens
BASE_IMAGE_PATH = r"C:\SeekMush\Dataset\Fotos + Nomes\Dataset Científico"

# Conectar ao banco PostgreSQL (ajuste os dados de acesso conforme seu setup)
engine = create_engine("postgresql+psycopg2://rocha:rocha123@localhost:5432/SeekMushBD")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Definir o modelo da tabela
class Mushroom(Base):
    __tablename__ = 'mushrooms'

    id = Column(Integer, primary_key=True)
    common_name = Column(String)
    scientific_name = Column(String)
    photo_path = Column(String)

# Criar as tabelas (caso não existam)
Base.metadata.create_all(engine)

# Carregar o CSV com os dados
df = pd.read_csv('C:/SeekMush/Dataset/Fotos + Nomes/translated_names.csv')

# Adicionar o caminho da pasta de imagens com base no nome científico
def montar_caminho(scientific_name):
    pasta = scientific_name.replace(" ", "_")  # Garantir o underline
    caminho_completo = os.path.join(BASE_IMAGE_PATH, pasta)
    return caminho_completo if os.path.isdir(caminho_completo) else None

# Preencher e inserir no banco
try:
    for _, row in df.iterrows():
        caminho = montar_caminho(row['scientific_name'])
        if caminho is None:
            print(f"Pasta não encontrada para {row['scientific_name']}. Pulando...")
            continue
        cogumelo = Mushroom(
            common_name=row['common_name'],
            scientific_name=row['scientific_name'],
            photo_path=caminho
        )
        session.add(cogumelo)

    session.commit()
    print("Dados inseridos com caminhos de imagem.")

except Exception as e:
    import traceback
    print("ERRO DETECTADO:")
    traceback.print_exc()

session.commit()
print("Dados inseridos com caminhos de imagem.")
