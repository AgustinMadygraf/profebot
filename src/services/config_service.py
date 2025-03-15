"""
Path: src/services/config_service.py
"""

import os
import pymysql

def get_system_instructions() -> str:
    """
    Conecta a MySQL y retorna el valor de system_instructions.
    En caso de error, retorna una instrucción por defecto.
    """
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "configdb")
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT system_instructions FROM configuration LIMIT 1;")
            result = cursor.fetchone()
            if result and result[0]:
                return result[0]
    except pymysql.MySQLError as e:
        print(f"Error conectando a MySQL: {e}")
    return "Responde de forma amistosa."
