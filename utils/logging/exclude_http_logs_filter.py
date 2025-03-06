"""
Path: utils/logging/exclude_http_logs_filter.py
Filtro para excluir mensajes de log relacionados con HTTP.
Evita llenar los logs con peticiones HTTP que pueden ser muy numerosas.
"""

import logging

class ExcludeHTTPLogsFilter(logging.Filter):
    """
    Filtro que excluye mensajes de log relacionados con peticiones HTTP.
    Útil para reducir ruido en los logs cuando hay muchas peticiones web.
    """

    def filter(self, record):
        """
        Implementación del método filter.
        
        Args:
            record: El registro de log a evaluar
            
        Returns:
            bool: True si el registro debe ser incluido, False en caso contrario
        """
        # Excluir mensajes que contienen palabras clave de HTTP
        http_keywords = ['http', 'HTTP', 'GET', 'POST', 'PUT', 'DELETE']

        # Si el mensaje contiene alguna de las palabras clave, no lo incluimos
        if any(keyword in record.getMessage() for keyword in http_keywords):
            return False

        return True
