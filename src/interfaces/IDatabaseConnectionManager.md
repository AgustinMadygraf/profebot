# Interfaz IDatabaseConnectionManager

Esta interfaz define el contrato para la gestión de conexiones a la base de datos.

## Métodos Esperados

- **create_database_if_not_exists()**: Crea la base de datos si no existe.
- **get_connection()**: Retorna una conexión activa a la base de datos.
