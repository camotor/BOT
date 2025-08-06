import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class ChatDatabase:
    def __init__(self, db_path: str = "chat_history.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla para sesiones de chat
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title TEXT
                )
            ''')
            
            # Tabla para mensajes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    message_type TEXT NOT NULL CHECK (message_type IN ('user', 'bot')),
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions (session_id)
                )
            ''')
            
            conn.commit()
    
    def create_session(self, session_id: str, title: str = None) -> bool:
        """Crea una nueva sesión de chat"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO chat_sessions (session_id, title)
                    VALUES (?, ?)
                ''', (session_id, title or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def add_message(self, session_id: str, message_type: str, content: str) -> bool:
        """Añade un mensaje a la sesión"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Actualizar última actividad de la sesión
                cursor.execute('''
                    UPDATE chat_sessions 
                    SET last_activity = CURRENT_TIMESTAMP 
                    WHERE session_id = ?
                ''', (session_id,))
                
                # Insertar mensaje
                cursor.execute('''
                    INSERT INTO messages (session_id, message_type, content)
                    VALUES (?, ?, ?)
                ''', (session_id, message_type, content))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding message: {e}")
            return False
    
    def get_session_messages(self, session_id: str) -> List[Dict]:
        """Obtiene todos los mensajes de una sesión"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT message_type, content, timestamp
                FROM messages
                WHERE session_id = ?
                ORDER BY timestamp ASC
            ''', (session_id,))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'type': row[0],
                    'content': row[1],
                    'timestamp': row[2]
                })
            
            return messages
    
    def get_all_sessions(self) -> List[Dict]:
        """Obtiene todas las sesiones de chat"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT session_id, title, created_at, last_activity,
                       (SELECT COUNT(*) FROM messages WHERE session_id = chat_sessions.session_id) as message_count
                FROM chat_sessions
                ORDER BY last_activity DESC
            ''')
            
            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    'session_id': row[0],
                    'title': row[1],
                    'created_at': row[2],
                    'last_activity': row[3],
                    'message_count': row[4]
                })
            
            return sessions
    
    def delete_session(self, session_id: str) -> bool:
        """Elimina una sesión y todos sus mensajes"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Eliminar mensajes
                cursor.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
                
                # Eliminar sesión
                cursor.execute('DELETE FROM chat_sessions WHERE session_id = ?', (session_id,))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
    
    def update_session_title(self, session_id: str, title: str) -> bool:
        """Actualiza el título de una sesión"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE chat_sessions 
                    SET title = ? 
                    WHERE session_id = ?
                ''', (title, session_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating session title: {e}")
            return False
