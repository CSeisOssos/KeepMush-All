# Servidor/test_db_utf8.py

import os
import sys
import traceback
from databaseSE import SessionLocal
from modelsSSE import Usuario

# Força encoding UTF-8 no sistema e no terminal (Windows-safe)
os.environ["PYTHONIOENCODING"] = "utf-8"
try:
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    # reconfigure não existe em versões antigas do Python
    pass

# Inicia sessão com o banco
session = SessionLocal()

# Cria novo usuário para teste
novo_usuario = Usuario(nome="Teste", email="teste@email.com", senha="123456")

try:
    session.add(novo_usuario)
    session.commit()
    print("✅ Usuário inserido com sucesso.")
except Exception as e:
    session.rollback()
    print("❌ Erro ao inserir usuário:")
    print(repr(e))  # Mostra erro completo, inclusive encoding
    traceback.print_exc()
finally:
    session.close()
