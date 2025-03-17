"""
Path: src/services/config_repository.py
"""
from src.services.database_connection_manager import DatabaseConnectionManager

class ConfigRepository:
    " Repositorio para la tabla de configuración del sistema "
    def __init__(self, connection_manager: DatabaseConnectionManager,  logger = None):
        self.connection_manager = connection_manager
        self.logger = logger

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
                self.logger.debug("Tabla 'configuration' verificada/creada.")

    def get_system_instructions(self) -> str:
        " Obtiene las instrucciones del sistema "
        with self.connection_manager.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT system_instructions FROM configuration LIMIT 1;")
                result = cursor.fetchone()
                if result and result[0]:
                    self.logger.debug("Instrucciones obtenidas: %s", result[0])
                    return result[0]
                else:
                    self.logger.warning(
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
