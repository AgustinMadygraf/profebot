"""
Path: src/interfaces/ILogger.py
"""

import abc

class ILogger(abc.ABC):
    """
    Interfaz para un servicio de logging.
    Define el contrato que deben cumplir las implementaciones, 
    facilitando la inyección de dependencias y la futura extensión."
    """
    @abc.abstractmethod
    def debug(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje de depuración."
        pass

    @abc.abstractmethod
    def info(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje informativo."
        pass

    @abc.abstractmethod
    def warning(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje de advertencia."
        pass

    @abc.abstractmethod
    def error(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje de error."
        pass

    @abc.abstractmethod
    def exception(self, msg: str, *args, **kwargs) -> None:
        "Registra un mensaje de excepción, incluyendo información de la traza."
        pass
