"""
Path: src/services/config_service.py
"""

import pymysql
from src.configuration.central_config import CentralConfig
from src.utils.logging.simple_logger import get_logger, log_exception

logger = get_logger()

def get_system_instructions() -> str:
    """
    Conecta a MySQL, verifica/crea la base de datos y la tabla 'configuration',
    y retorna el valor de system_instructions. En caso de error,
    retorna una instrucción por defecto.
    """
    try:
        # Conectar sin especificar la base de datos para poder crearla si no existe
        connection = pymysql.connect(
            host=CentralConfig.DB_HOST,
            user=CentralConfig.DB_USER,
            password=CentralConfig.DB_PASSWORD
        )
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {CentralConfig.DB_NAME};")
            logger.debug("Base de datos '%s' verificada/creada.", CentralConfig.DB_NAME)
        connection.close()

        # Conectar a la base de datos especificada
        connection = pymysql.connect(
            host=CentralConfig.DB_HOST,
            user=CentralConfig.DB_USER,
            password=CentralConfig.DB_PASSWORD,
            database=CentralConfig.DB_NAME
        )
        logger.debug(
            "Valores de conexión: DB_HOST=%s, DB_USER=%s, DB_NAME=%s",
            CentralConfig.DB_HOST, CentralConfig.DB_USER, CentralConfig.DB_NAME
        )
        with connection.cursor() as cursor:
            # Crear la tabla 'configuration' sin valor por defecto en system_instructions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS configuration (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    system_instructions TEXT NOT NULL
                );
            """)
            connection.commit()
            logger.debug("Tabla 'configuration' verificada/creada.")

            # Intentar obtener las instrucciones del sistema
            cursor.execute("SELECT system_instructions FROM configuration LIMIT 1;")
            result = cursor.fetchone()
            if result and result[0]:
                logger.debug("Instrucciones obtenidas: %s", result[0])
                return result[0]
            else:
                logger.warning(
                    "No se encontraron instrucciones en la base de datos, "
                    "insertando instrucción por defecto."
                )
                default_instructions = "Responde de forma amistosa."
                cursor.execute(
                    "INSERT INTO configuration (system_instructions) VALUES (%s);",
                    (default_instructions,)
                )
                connection.commit()
                return default_instructions
    except pymysql.MySQLError as e:
        log_exception(e)
    return "Responde de forma amistosa."
