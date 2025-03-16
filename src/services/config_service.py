"""
Path: src/services/config_service.py
"""

import pymysql
from src.configuration.central_config import CentralConfig
from src.utils.logging.simple_logger import get_logger, log_exception

logger = get_logger()

# Nuevo: Gestor de Conexiones a la Base de Datos
class DatabaseConnectionManager:
    " Gestor de conexiones a la base de datos MySQL "
    def __init__(self):
        self.config = CentralConfig

    def create_database_if_not_exists(self):
        " Crea la base de datos si no existe "
        connection = pymysql.connect(
            host=self.config.DB_HOST,
            user=self.config.DB_USER,
            password=self.config.DB_PASSWORD
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config.DB_NAME};")
                logger.debug("Base de datos '%s' verificada/creada.", self.config.DB_NAME)
            connection.commit()
        finally:
            connection.close()

    def get_connection(self):
        " Obtiene una conexión a la base de datos "
        return pymysql.connect(
            host=self.config.DB_HOST,
            user=self.config.DB_USER,
            password=self.config.DB_PASSWORD,
            database=self.config.DB_NAME
        )

# Nuevo: Repositorio de Configuración
class ConfigRepository:
    " Repositorio para la tabla de configuración del sistema "
    def __init__(self, connection_manager: DatabaseConnectionManager):
        self.connection_manager = connection_manager

    def initialize_configuration(self):
        " Inicializa la tabla de configuración si no existe "
        with self.connection_manager.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS configuration (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        system_instructions TEXT NOT NULL
                    );
                """)
                connection.commit()
                logger.debug("Tabla 'configuration' verificada/creada.")

    def get_system_instructions(self) -> str:
        " Obtiene las instrucciones del sistema "
        with self.connection_manager.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT system_instructions FROM configuration LIMIT 1;")
                result = cursor.fetchone()
                if result and result[0]:
                    logger.debug("Instrucciones obtenidas: %s", result[0])
                    return result[0]
                else:
                    logger.warning(
                        "No se encontraron instrucciones, "
                        "insertando instrucción por defecto."
                    )
                    default_instructions = "Responde de forma amistosa."
                    cursor.execute(
                        "INSERT INTO configuration (system_instructions) VALUES (%s);",
                        (default_instructions,)
                    )
                    connection.commit()
                    return default_instructions

# Refactorización de la función get_system_instructions
def get_system_instructions() -> str:
    " Obtiene las instrucciones del sistema "
    try:
        connection_manager = DatabaseConnectionManager()
        connection_manager.create_database_if_not_exists()
        repo = ConfigRepository(connection_manager)
        repo.initialize_configuration()
        return repo.get_system_instructions()
    except pymysql.MySQLError as e:
        log_exception(e)
    return "Responde de forma amistosa."
