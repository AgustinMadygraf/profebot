"""
Path: docs/diagrama_e_r.py
"""
from graphviz import Digraph

def generar_diagrama_er():
    "Genera un diagrama E-R de la base de datos de Telegram."
    dot = Digraph(comment='Diagrama ER de la Base de Datos Telegram')

    # Nodo para la tabla users
    dot.node('users', '''users
--------------------------
id (PK)
is_bot
first_name
username
language_code''')

    # Nodo para la tabla chats
    dot.node('chats', '''chats
--------------------------
id (PK)
first_name
username
type''')

    # Nodo para la tabla updates
    dot.node('updates', '''updates
--------------------------
update_id (PK)
created_at''')

    # Nodo para la tabla messages
    dot.node('messages', '''messages
--------------------------
message_id (PK)
update_id (FK)
from_id (FK)
chat_id (FK)
date
text''')

    # Definir relaciones mediante aristas
    # messages -> updates (update_id)
    dot.edge('messages', 'updates', label='update_id')
    # messages -> users (from_id)
    dot.edge('messages', 'users', label='from_id')
    # messages -> chats (chat_id)
    dot.edge('messages', 'chats', label='chat_id')

    return dot

if __name__ == '__main__':
    diagrama = generar_diagrama_er()
    # Renderizar el diagrama en formato PNG y visualizarlo
    diagrama.render('diagrama_er', view=True, format='png')
