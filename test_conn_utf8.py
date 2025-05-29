import os
import psycopg2
import sys

# Força o encoding UTF-8 no sistema e no Python
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

try:
    conn = psycopg2.connect(
        dbname="SeekMushBD",
        user="rocha",
        password="rocha123",
        host="localhost",
        port="5432"
    )
    print("Conexão bem-sucedida!")
except Exception as e:
    print("Erro na conexão:")
    print(repr(e))
