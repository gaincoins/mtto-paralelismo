import psycopg2
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import os
import sys

# Cargar variables desde el archivo .env
load_dotenv()

# Leer configuraciones desde variables de entorno
ARCHIVO_SQL = os.getenv("SQL_FILE")
ARCHIVO_LOG = os.getenv("LOG_FILE")
MAX_CONEXIONES = int(os.getenv("MAX_CONN", 10))

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "port": os.getenv("DB_PORT", "5432"),
    "application_name": os.getenv("APPLICATION_NAME")
}

def ejecutar_vacuum(comando):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        
        with conn.cursor() as cursor:
            cursor.execute(comando)
        return True, comando
    except Exception as e:
        return False, f"{comando} - Error: {str(e)}"
    finally:
        if conn:
            conn.close()

def main():
    if not os.path.exists(ARCHIVO_SQL):
        print(f"Error: No se encontró el archivo {ARCHIVO_SQL}")
        sys.exit(1)

    with open(ARCHIVO_SQL, 'r') as f:
        comandos = [line.strip() for line in f if line.strip() and not line.startswith('--')]

    if not comandos:
        print("No se encontraron comandos VACUUM válidos en el archivo")
        sys.exit(1)

    with ThreadPoolExecutor(max_workers=MAX_CONEXIONES) as executor:
        resultados = list(executor.map(ejecutar_vacuum, comandos))

    exitos = sum(1 for resultado in resultados if resultado[0])
    resumen = (
        f"\nRESUMEN DE EJECUCIÓN:\n"
        f"Archivo SQL procesado: {ARCHIVO_SQL}\n"
        f"Comandos ejecutados: {len(comandos)}\n"
        f"Comandos exitosos: {exitos}\n"
        f"Comandos fallidos: {len(comandos) - exitos}\n"
    )

    with open(ARCHIVO_LOG, 'w') as log_file:
        log_file.write(resumen)
        log_file.write("\nDETALLE DE COMANDOS:\n")
        for resultado in resultados:
            log_file.write(f"{'ok' if resultado[0] else 'error'} {resultado[1]}\n")

    print(resumen)
    print(f"Log completo guardado en: {os.path.abspath(ARCHIVO_LOG)}")

if __name__ == "__main__":
    main()
