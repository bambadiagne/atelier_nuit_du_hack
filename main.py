import os
import sqlite3
from typing import Optional
from pathlib import Path
import logging
from dotenv import load_dotenv
load_dotenv() 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_config():
    return {
            'username': os.environ.get('DB_USERNAME'),
            'password': os.environ.get('DB_PASSWORD'),
            'database_path': os.environ.get('DB_PATH'),
            'timeout': 5
        }

def connect_to_database() -> Optional[sqlite3.Connection]:
    config = get_db_config()
    try:
        db_path = Path(config['database_path'])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        connection = sqlite3.connect(
            database=str(db_path),
            timeout=config['timeout']
        )

        cursor = connection.cursor()
        cursor.execute("SELECT SQLITE_VERSION()")
        version = cursor.fetchone()
        logger.info(f"Successfully connected to SQLite. Version: {version[0]}")
        logger.info(f"Using database at: {config['database_path']}")
        
        return connection
        
    except sqlite3.Error as error:
        logger.error(f"Error while connecting to SQLite: {error}")
        return None
    except Exception as error:
        logger.error(f"Unexpected error: {error}")
        return None

def close_connection(connection: sqlite3.Connection) -> None:
    if connection:
        connection.close()
        logger.info("Database connection closed")

if __name__ == "__main__":
    
    connection = connect_to_database()
    if connection:
        close_connection(connection)