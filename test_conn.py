import psycopg2

try:
    conn = psycopg2.connect(
        dbname="seekmushBD",
        user="rocha",
        password="rocha123",
        host="localhost",
        port="5432"
    )
    print("Conexão bem-sucedida!")
except Exception as e:
    print("Erro na conexão:", e)
