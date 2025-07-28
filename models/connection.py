import sqlite3
from pathlib import Path
import logging

class DatabaseConnection:
    def __init__(self, path='data/database.sqlite'):
        self.path = Path(path)

    def connect(self):
        logging.info(f"Conectando ao banco de dados em {self.path}")
        try:
            conetion = sqlite3.connect(self.path)
            logging.info("Conexão estabelecida com sucesso.")
            return conetion
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            return None
