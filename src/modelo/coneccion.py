## coneccion a la base de datos
import psycopg2
## para recuperar datos de .env
from decouple import config

def db_connection():
    con=psycopg2.connect(
            host=config('PG_HOST'),
            user=config('PG_USER'),
            password=config('PG_PASSWORD'),
            database=config('PG_DB')
        )
    return con

