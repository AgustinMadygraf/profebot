"""
Path: utils/logging/error_manager.py
Gestor centralizado de errores para la aplicación.
Proporciona funciones y clases para el manejo unificado de excepciones.
"""

import logging
import sys
import traceback
from typing import Optional, Callable, Dict, Any, Type, TypeVar

# Tipo genérico para excepciones
ExceptionType = TypeVar('ExceptionType', bound=Exception)

# Tipo de callback para handlers de errores
ErrorHandlerCallback = Callable[[Exception, Dict[str, Any]], None]

class ErrorManager:
    """
    Gestor centralizado para el manejo de errores y excepciones.
    Permite registrar handlers personalizados para diferentes tipos de excepciones
    y proporciona una interfaz unificada para el manejo de errores.
    """

    def __init__(self, logger: logging.Logger):
        """
        Inicializa el gestor de errores.
        
        Args:
            logger: Logger configurado para registrar eventos
        """
        self.logger = logger
        self.logger.debug("Inicializando ErrorManager")

        # Diccionario de handlers específicos por tipo de excepción
        self._handlers: Dict[Type[Exception], ErrorHandlerCallback] = {}

        # Handler por defecto
        self._default_handler: Optional[ErrorHandlerCallback] = None

        # Configurar el handler por defecto
        self.set_default_handler(self._log_exception)

        self.logger.debug("ErrorManager inicializado")

    def set_default_handler(self, handler: ErrorHandlerCallback) -> None:
        """
        Establece el handler por defecto para excepciones no manejadas específicamente.
        
        Args:
            handler: Función de callback para manejar excepciones
        """
        self._default_handler = handler
        self.logger.debug(f"Handler por defecto establecido: {handler.__name__}")

    def register_handler(self, exception_type: Type[ExceptionType],
                        handler: ErrorHandlerCallback) -> None:
        """
        Registra un handler específico para un tipo de excepción.
        
        Args:
            exception_type: Clase de excepción a manejar
            handler: Función de callback para manejar la excepción
        """
        self._handlers[exception_type] = handler
        self.logger.debug(
            f"Handler registrado para {exception_type.__name__}: {handler.__name__}"
        )

    def handle_exception(self, exception: Exception, context: Dict[str, Any] = None) -> None:
        """
        Maneja una excepción utilizando el handler apropiado.
        
        Args:
            exception: Excepción a manejar
            context: Información de contexto adicional (opcional)
        """
        if context is None:
            context = {}

        # Añadimos información sobre la pila de llamadas
        exc_info = sys.exc_info()
        if exc_info[2] is not None:
            context['traceback'] = traceback.format_tb(exc_info[2])

        # Buscar un handler específico para esta excepción
        handler_found = False
        for exc_type, handler in self._handlers.items():
            if isinstance(exception, exc_type):
                self.logger.debug(
                    f"Usando handler específico para {exc_type.__name__}: {handler.__name__}"
                )
                handler(exception, context)
                handler_found = True
                break

        # Si no hay handler específico, usar el por defecto
        if not handler_found and self._default_handler is not None:
            self.logger.debug(
                f"Usando handler por defecto para {type(exception).__name__}"
            )
            self._default_handler(exception, context)

    def _log_exception(self, exception: Exception, context: Dict[str, Any]) -> None:
        """
        Handler por defecto que registra la excepción en el log.
        
        Args:
            exception: Excepción a registrar
            context: Información de contexto adicional
        """
        # Preparar mensaje de error con contexto
        error_msg = f"Error no manejado: {exception}"

        # Si hay contexto, incluirlo en el log
        if context:
            error_msg += f" | Contexto: {context}"

        # Registrar con nivel ERROR y la excepción completa
        self.logger.error(error_msg, exc_info=True)

    def critical_error(self, exception: Exception, context: Dict[str, Any] = None) -> None:
        """
        Maneja un error crítico que requiere notificación inmediata.

        Args:
            exception: Excepción que provocó el error crítico
            context: Información de contexto adicional (opcional)
        """
        if context is None:
            context = {}

        context['critical'] = True
        self.logger.critical(f"ERROR CRÍTICO: {exception}", exc_info=True)

        # Aquí se podrían implementar notificaciones adicionales
        # como enviar emails, mensajes a un servicio de monitoreo, etc.

        # Manejar la excepción normalmente después de la notificación
        self.handle_exception(exception, context)


# Instancia global del manager (se inicializará más tarde)
_error_manager: Optional[ErrorManager] = None

def init_error_manager(logger: logging.Logger) -> ErrorManager:
    """
    Inicializa el gestor de errores con el logger proporcionado.
    
    Args:
        logger: Logger configurado para registrar eventos
        
    Returns:
        Instancia de ErrorManager configurada
    """
    global _error_manager
    _error_manager = ErrorManager(logger)
    logger.debug("ErrorManager global inicializado")
    return _error_manager

def get_error_manager() -> ErrorManager:
    """
    Obtiene la instancia global del gestor de errores.
    
    Returns:
        Instancia de ErrorManager configurada
        
    Raises:
        RuntimeError: Si el gestor de errores no ha sido inicializado
    """
    if _error_manager is None:
        # Intentar obtener un logger para inicializar el error manager
        try:
            from utils.logging.dependency_injection import get_logger
            logger = get_logger("error_manager")
            init_error_manager(logger)
        except ImportError:
            # Si no podemos obtener el logger, crear uno básico
            logger = logging.getLogger("error_manager_fallback")
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.warning("Usando logger de fallback para ErrorManager")
            init_error_manager(logger)

    return _error_manager

def handle_exception(exception: Exception, context: Dict[str, Any] = None) -> None:
    """
    Función helper para manejar excepciones a través del gestor global.
    
    Args:
        exception: Excepción a manejar
        context: Información de contexto adicional (opcional)
    """
    get_error_manager().handle_exception(exception, context)

def critical_error(exception: Exception, context: Dict[str, Any] = None) -> None:
    """
    Función helper para manejar errores críticos a través del gestor global.
    
    Args:
        exception: Excepción que provocó el error crítico
        context: Información de contexto adicional (opcional)
    """
    get_error_manager().critical_error(exception, context)
