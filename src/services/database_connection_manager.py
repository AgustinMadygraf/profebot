"""
Path: src/services/database_connection_Manager.py
"""

import pymysql
from src.configuration.central_config import CentralConfig

class DatabaseConnectionManager():
    " Gestor de conexiones a la base de datos MySQL "
    def __init__(self,logger = None):
        self.config = CentralConfig
        self.logger = logger

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
                self.logger.debug("Base de datos '%s' verificada/creada.", self.config.DB_NAME)
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
