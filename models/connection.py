import sqlite3
from pathlib import Path
import logging

# Classe responsável por gerenciar a conexão com o banco de dados
class DatabaseConnection:
    def __init__(self, path='data/database.sqlite'):
        # Define o caminho do banco de dados
        self.path = Path(path)

    # Método para estabelecer a conexão com o banco de dados
    def connect(self):
        logging.info(f"Conectando ao banco de dados em {self.path}")
        try:
            # Tenta conectar ao banco de dados
            conetion = sqlite3.connect(self.path)
            logging.info("Conexão estabelecida com sucesso.")
            return conetion
        except sqlite3.Error as e:
            # Em caso de erro, registra o log e retorna None
            logging.error(f"Erro ao conectar ao banco de dados: {e}")
            return None
