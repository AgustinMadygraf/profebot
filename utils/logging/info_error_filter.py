"""
Path: utils/logging/info_error_filter.py
Filtro para limitar los mensajes de log a INFO y ERROR.
Permite controlar la salida de logging según el nivel de los mensajes.
"""

import logging

class InfoErrorFilter(logging.Filter):
    """
    Filtro que solo permite mensajes de nivel INFO y ERROR.
    Útil para separar flujos de log según su importancia.
    """
    
    def filter(self, record):
        """
        Implementación del método filter.
        
        Args:
            record: El registro de log a evaluar
            
        Returns:
            bool: True si el registro debe ser incluido, False en caso contrario
        """
        # Permitir mensajes de nivel INFO y ERROR
        return record.levelno in (logging.INFO, logging.ERROR)
