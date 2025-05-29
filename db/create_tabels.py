from database import engine
import models

print("Criando tabelas no PostgreSQL...")
models.Base.metadata.create_all(bind=engine)
print("Concluído!")