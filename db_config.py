import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="mi_base_de_datos",
        user="root",
        password="!@#DeepThink^"
    )
