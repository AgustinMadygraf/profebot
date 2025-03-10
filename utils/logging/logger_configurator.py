"""
Path: utils/logging/logger_configurator.py
Configurador de logging para la aplicación.
Proporciona una API unificada para configurar el logging.
"""

import json
import logging
import logging.config
import logging.handlers
import os
import sys
from typing import Optional, List, Any, Dict, Set

from utils.logging.logger_factory import LoggerFactory

# Bandera global para controlar el nivel de detalle del debug
# Se puede modificar en tiempo de ejecución según el entorno
DEBUG_VERBOSE = False

class LoggerConfigurator:
    """Configurador de logging para la aplicación."""

    # Almacenamiento para los handlers creados, evitando duplicación
    _handlers_cache: Dict[str, logging.Handler] = {}

    # Conjunto para seguir los nombres de loggers ya configurados
    _configured_loggers: Set[str] = set()

    def __init__(
        self,
        log_path: str = "logs",
        log_level: int = logging.INFO,
        logger_name: str = "profebot"
    ):
        """
        Inicializa el configurador de logging.
        
        Args:
            log_path: Ruta donde se almacenarán los logs
            log_level: Nivel de logging predeterminado
            logger_name: Nombre del logger principal
        """
        self.log_path = log_path
        self.log_level = log_level
        self.logger_name = logger_name
        self.filters = []
        self.formatter = self._create_standard_formatter()

        # Crear el directorio de logs si no existe
        self._ensure_directory_exists(log_path)

        # No podemos usar self.logger aquí porque aún no existe
        print(
            f"LoggerConfigurator inicializado: path={log_path}, "
            f"level={log_level}, name={logger_name}"
        )

    def _ensure_directory_exists(self, directory_path: str) -> None:
        """
        Asegura que un directorio exista, creándolo si es necesario.
        
        Args:
            directory_path: Ruta del directorio a verificar/crear
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            print(f"Directorio de logs asegurado: {directory_path}")
        except OSError as e:
            # No podemos usar logging aquí, así que solo imprimimos
            print(f"ADVERTENCIA: No se pudo crear el directorio para logs: {directory_path}")
            print(f"Razón: {str(e)}")

    def register_filter(self, filter_class: Any) -> None:
        """
        Registra un filtro para usarlo en la configuración.
        
        Args:
            filter_class: Clase del filtro a instanciar
        """
        # Solo añadir filtros nuevos, evitar duplicados
        for existing_filter in self.filters:
            if isinstance(existing_filter, filter_class):
                print(f"Filtro {filter_class.__name__} ya registrado, omitiendo")
                return

        self.filters.append(filter_class())
        # Como esto se llama antes de configurar el logger, usamos print para debug
        print(f"Filtro registrado: {filter_class.__name__}")

    def configure_from_json(self, json_path: str) -> logging.Logger:
        """
        Configura el logger utilizando un archivo JSON de configuración.
        
        Args:
            json_path: Ruta al archivo JSON de configuración
            
        Returns:
            Logger configurado
        """
        print(f"Configurando logger desde JSON: {json_path}")

        # Verificar existencia del archivo
        if not os.path.exists(json_path):
            return self._handle_json_config_error(
                f"Archivo de configuración JSON no encontrado: {json_path}",
                "Fallback a configuración manual"
            )

        try:
            print(f"Archivo JSON encontrado, intentando cargar: {json_path}")
            # Cargar configuración desde JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"JSON cargado correctamente, configuración: {config.keys()}")

            # Ajustar rutas de archivos si es necesario
            if 'handlers' in config:
                self._prepare_log_directories(config)

            if not DEBUG_VERBOSE:
                # Ajustar nivel del logger principal si existe
                if 'loggers' in config and self.logger_name in config['loggers']:
                    config['loggers'][self.logger_name]['level'] = 'INFO'

                # Ajustar nivel de handlers que no son específicos de errores
                if 'handlers' in config:
                    for handler_name, handler_config in config['handlers'].items():
                        if 'level' in handler_config and handler_config['level'] == 'DEBUG':
                            if not handler_name.startswith('error'):
                                handler_config['level'] = 'INFO'

                # Ajustar nivel del logger raíz si existe
                if ('root' in config and 'level' in config['root'] and
                        config['root']['level'] == 'DEBUG'):
                    config['root']['level'] = 'INFO'

                print("Niveles de logging ajustados a INFO (modo no verbose)")

            print("Aplicando configuración mediante dictConfig")
            # Aplicar configuración
            logging.config.dictConfig(config)
            print("Configuración aplicada correctamente")

            # Obtener logger configurado
            logger = logging.getLogger(self.logger_name)
            logger_level_name = logging.getLevelName(logger.level)
            print(
                f"Logger '{self.logger_name}' configurado con nivel: "
                f"{logger.level} ({logger_level_name})"
            )

            # Registrar en LoggerFactory para acceso global
            LoggerFactory.set_default_logger(logger)

            # Este mensaje solo se verá si DEBUG está activado después de la configuración
            logger.debug("Logger inicializado desde configuración JSON")

            return logger

        except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
            return self._handle_json_config_error(
                f"Error al cargar configuración desde JSON: {e}",
                "Fallback a configuración manual.",
                e
            )

    def _handle_json_config_error(self, error_message: str,
                                fallback_message: str = "Fallback a configuración manual.",
                                exception: Exception = None) -> logging.Logger:
        """
        Maneja errores durante la configuración desde JSON.
        
        Args:
            error_message: Mensaje principal de error
            fallback_message: Mensaje sobre la acción alternativa
            exception: La excepción que causó el error
            
        Returns:
            Logger configurado con el método fallback
        """
        print(f"{error_message}")
        print(f"{fallback_message}")

        # Crear logger con configuración manual como fallback
        fallback_logger = self.configure()

        # Registrar el error en el nuevo logger
        fallback_logger.error("%s. %s", error_message, fallback_message)
        if exception:
            fallback_logger.debug(
                "Detalles de la excepción: %s: %s", type(exception).__name__, str(exception)
            )

        return fallback_logger

    def _prepare_log_directories(self, config: Dict) -> None:
        """
        Prepara los directorios para los archivos de log definidos en la configuración.
        
        Args:
            config: Configuración de logging en formato diccionario
        """
        if 'handlers' not in config:
            print("No se encontraron handlers en la configuración")
            return

        print(f"Analizando {len(config['handlers'])} handlers para ajustar rutas")
        for handler_name, handler_config in config['handlers'].items():
            if 'filename' in handler_config:
                self._prepare_handler_directory(handler_name, handler_config['filename'])

    def _prepare_handler_directory(self, handler_name: str, filepath: str) -> None:
        """
        Prepara el directorio para un archivo de log específico.
        
        Args:
            handler_name: Nombre del handler para referencia
            filepath: Ruta del archivo de log
        """
        original_path = filepath
        # Extraer el directorio del archivo
        log_dir = os.path.dirname(filepath)
        if log_dir:
            print(f"Creando directorio para handler {handler_name}: {log_dir}")
            self._ensure_directory_exists(log_dir)
            print(f"Handler {handler_name}: directorio preparado para {original_path}")

    def configure(self, filters: Optional[List[Any]] = None) -> logging.Logger:
        """
        Configura y devuelve un logger con los filtros proporcionados.
        
        Args:
            filters: Lista opcional de filtros a aplicar
            
        Returns:
            Logger configurado
        """
        print(f"Configurando logger manualmente: {self.logger_name}")

        # Obtener o crear el logger
        logger = self._get_or_create_logger()

        # Si este logger ya está configurado, simplemente devolverlo
        if self.logger_name in self._configured_loggers:
            print(f"Logger '{self.logger_name}' ya configurado, reutilizando")
            return logger

        # Añadir handlers si no existen
        self._add_handlers_to_logger(logger, filters)

        # Registrar en LoggerFactory para acceso global
        LoggerFactory.set_default_logger(logger)

        # Marcar este logger como configurado
        self._configured_loggers.add(self.logger_name)

        # Mensaje inicial con información del sistema
        logger.debug("Logger configurado manualmente")
        logger.debug("Versión Python: %s", sys.version)
        logger.debug("Plataforma: %s", sys.platform)

        return logger

    def _get_or_create_logger(self) -> logging.Logger:
        """
        Obtiene un logger existente o crea uno nuevo configurándolo.
        
        Returns:
            Logger configurado con el nivel adecuado
        """
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.log_level)

        # Si el logger ya tiene handlers, verificamos si necesitamos propagar
        if logger.hasHandlers():
            # Solo desactivamos la propagación para el logger principal
            # para evitar duplicación de logs
            if not logger.name or logger.name == 'root':
                logger.propagate = False

        return logger

    def _add_handlers_to_logger(self, logger: logging.Logger, filters: Optional[List[Any]]) -> None:
        """
        Añade los handlers necesarios al logger si no existen ya.
        
        Args:
            logger: Logger al que añadir los handlers
            filters: Filtros adicionales a aplicar
        """
        # Si ya tiene handlers, no añadir más
        if logger.handlers:
            print(f"Logger ya tiene handlers ({len(logger.handlers)}), evitando duplicación")
            return

        # Crear los handlers necesarios o recuperar del caché
        console_handler = self._get_or_create_console_handler()
        file_handler = self._get_or_create_file_handler('app.log')
        error_handler = self._get_or_create_error_handler('error.log')

        # Aplicar filtros a los handlers
        self._apply_filters_to_handlers([console_handler, file_handler], filters)

        # Añadir los handlers al logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(error_handler)

        print(f"Handlers agregados al logger: {len(logger.handlers)} handlers")

    def _get_or_create_console_handler(self) -> logging.Handler:
        """
        Obtiene o crea un handler para consola.
        
        Returns:
            Handler configurado para consola
        """
        handler_key = 'console'
        if handler_key in self._handlers_cache:
            return self._handlers_cache[handler_key]

        console = logging.StreamHandler()
        console.setLevel(self.log_level)
        console.setFormatter(self.formatter)

        self._handlers_cache[handler_key] = console
        print(f"Handler de consola creado con nivel: {self.log_level}")

        return console

    def _get_or_create_file_handler(self, filename: str) -> logging.Handler:
        """
        Obtiene o crea un handler para archivo de log.
        
        Args:
            filename: Nombre del archivo de log
            
        Returns:
            Handler configurado para archivo
        """
        handler_key = f'file_{filename}'
        if handler_key in self._handlers_cache:
            return self._handlers_cache[handler_key]

        log_file_path = os.path.join(self.log_path, filename)
        print(f"Configurando handler para archivo: {log_file_path}")

        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self.formatter)

        self._handlers_cache[handler_key] = file_handler

        return file_handler

    def _get_or_create_error_handler(self, filename: str) -> logging.Handler:
        """
        Obtiene o crea un handler específico para errores.
        
        Args:
            filename: Nombre del archivo de log para errores
            
        Returns:
            Handler configurado para errores
        """
        handler_key = f'error_{filename}'
        if handler_key in self._handlers_cache:
            return self._handlers_cache[handler_key]

        error_file_path = os.path.join(self.log_path, filename)
        print(f"Configurando handler para errores: {error_file_path}")

        error_file = logging.handlers.RotatingFileHandler(
            error_file_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_file.setLevel(logging.ERROR)  # Solo para errores y críticos
        error_file.setFormatter(self.formatter)

        self._handlers_cache[handler_key] = error_file

        return error_file

    def _apply_filters_to_handlers(self, handlers: List[logging.Handler],
                                   additional_filters: Optional[List[Any]]) -> None:
        """
        Aplica los filtros registrados a los handlers especificados.
        
        Args:
            handlers: Lista de handlers a los que aplicar filtros
            additional_filters: Filtros adicionales a aplicar
        """
        # Combinar filtros registrados con los adicionales
        all_filters = list(self.filters)  # Crear una copia
        if additional_filters:
            print(f"Añadiendo {len(additional_filters)} filtros adicionales")
            all_filters.extend(additional_filters)

        # Si no hay filtros, no hacer nada
        if not all_filters:
            return

        print(f"Aplicando {len(all_filters)} filtros a {len(handlers)} handlers")
        for handler in handlers:
            for filter_obj in all_filters:
                # Evitar añadir el mismo filtro varias veces
                if self._should_add_filter(handler, filter_obj):
                    print(
                        f"Aplicando filtro: {filter_obj.__class__.__name__} "
                        f"a {handler.__class__.__name__}"
                    )
                    handler.addFilter(filter_obj)

    def _should_add_filter(self, handler: logging.Handler, filter_obj: Any) -> bool:
        """
        Determina si un filtro debe añadirse a un handler.
        
        Args:
            handler: Handler al que se quiere añadir el filtro
            filter_obj: Filtro a evaluar
            
        Returns:
            True si se debe añadir, False si ya existe un filtro del mismo tipo
        """
        for existing_filter in handler.filters:
            if isinstance(existing_filter, type(filter_obj)):
                return False
        return True

    def _create_standard_formatter(self) -> logging.Formatter:
        """
        Crea un formateador estándar para los logs.
        
        Returns:
            Formateador configurado
        """
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )

    def log_debug(self, logger: logging.Logger, message: str, *args, **kwargs) -> None:
        """
        Función centralizada para el logging de mensajes de debug.
        Permite controlar de forma centralizada el nivel de detalle de los logs.
        
        Args:
            logger: Logger a utilizar
            message: Mensaje a registrar
            *args: Argumentos posicionales para el mensaje
            **kwargs: Argumentos con nombre para la llamada al logger
        """
        # Si el modo verbose está activado, añadimos información extra
        if DEBUG_VERBOSE:
            # Obtener información del llamador
            import inspect
            caller_frame = inspect.currentframe().f_back
            filename = os.path.basename(caller_frame.f_code.co_filename)
            lineno = caller_frame.f_lineno
            caller_info = f"[{filename}:{lineno}]"

            # Añadir información del llamador al mensaje
            enhanced_message = f"{caller_info} {message}"
            logger.debug(enhanced_message, *args, **kwargs)
        else:
            # Comportamiento normal
            logger.debug(message, *args, **kwargs)


def get_logger(name: str = "profebot") -> logging.Logger:
    """
    Retorna un logger configurado.
    Wrapper simple para usar LoggerFactory.
    
    Args:
        name: Nombre del logger
        
    Returns:
        Logger configurado
    """
    logger = LoggerFactory.get_logger(name)
    logger.debug(f"Logger '{name}' obtenido de LoggerFactory")
    return logger


def set_debug_verbose(enabled: bool = True) -> None:
    """
    Activa o desactiva el modo verbose para mensajes de debug.
    
    Args:
        enabled: True para activar, False para desactivar
    """
    global DEBUG_VERBOSE
    DEBUG_VERBOSE = enabled

    # Obtener un logger para registrar el cambio
    logger = get_logger("logging_system")

    # Establecer el nivel apropiado en el logger raíz y todos los handlers
    root_logger = logging.getLogger()
    level = logging.DEBUG if enabled else logging.INFO

    # Cambiar nivel del logger raíz
    root_logger.setLevel(level)

    # Cambiar nivel de todos los handlers del logger raíz
    for handler in root_logger.handlers:
        # Solo cambiar el nivel en handlers que no son específicos para errores
        if handler.level < logging.ERROR:
            handler.setLevel(level)

    level_str = "ACTIVADO" if enabled else "DESACTIVADO"
    logger.info(f"Modo DEBUG_VERBOSE {level_str}, nivel de logging: {logging.getLevelName(level)}")


def get_debug_verbose() -> bool:
    """
    Obtiene el estado actual del modo verbose para debug.
    
    Returns:
        True si está activado, False si no
    """
    global DEBUG_VERBOSE
    return DEBUG_VERBOSE


def log_debug(message: str, *args, **kwargs) -> None:
    """
    Función global para logging centralizado de mensajes de debug.
    Utiliza el logger por defecto.
    
    Args:
        message: Mensaje a registrar
        *args: Argumentos posicionales para el mensaje
        **kwargs: Argumentos con nombre para la llamada al logger
    """
    logger = LoggerFactory.get_default_logger()
    configurator = LoggerConfigurator()
    configurator.log_debug(logger, message, *args, **kwargs)
