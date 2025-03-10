"""
Path: utils/logging/logger_factory.py
Factoría para la creación y gestión de loggers.
Permite tener un punto central para recuperar instancias de logger.
"""

import logging
from typing import Dict, Optional

class LoggerFactory:
    """Clase para gestionar la creación y obtención de loggers."""
    # Almacena el logger predeterminado para toda la aplicación
    _default_logger: Optional[logging.Logger] = None
    # Almacena loggers por nombre para evitar crear múltiples instancias
    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def set_default_logger(cls, logger: logging.Logger) -> None:
        """
        Establece el logger predeterminado para toda la aplicación.
        
        Args:
            logger: Logger a establecer como predeterminado
        """
        cls._default_logger = logger

    @classmethod
    def get_default_logger(cls) -> logging.Logger:
        """
        Obtiene el logger predeterminado.
        
        Returns:
            Logger predeterminado
        
        Raises:
            RuntimeError: Si el logger predeterminado no ha sido configurado
        """
        if cls._default_logger is None:
            # Si no hay logger configurado, usamos un logger básico para evitar errores
            print("ADVERTENCIA: Logger predeterminado no configurado, usando logger básico.")
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            logger = logging.getLogger("profebot_default")
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
            cls._default_logger = logger

        return cls._default_logger

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Obtiene un logger por nombre.
        Si ya existe un logger con ese nombre, lo devuelve.
        Si no, crea uno nuevo.
        
        Args:
            name: Nombre del logger a obtener
            
        Returns:
            Logger solicitado
        """
        if name == "default" or name == "profebot":
            return cls.get_default_logger()

        if name not in cls._loggers:
            # Crear un nuevo logger y heredar configuración del logger predeterminado
            logger = logging.getLogger(name)

            # Si el logger predeterminado está configurado, usar sus handlers
            if cls._default_logger is not None:
                # Limpiar handlers existentes
                for handler in logger.handlers[:]:
                    logger.removeHandler(handler)

                # Copiar handlers del logger predeterminado
                for handler in cls._default_logger.handlers:
                    logger.addHandler(handler)

                # Usar el mismo nivel de log
                logger.setLevel(cls._default_logger.level)

            cls._loggers[name] = logger

        return cls._loggers[name]
