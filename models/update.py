from models.connection import DatabaseConnection

class UpdateStatus:
    def __init__(self):
        self.db = DatabaseConnection()

    def update(self, cnpj, status_processo, connection_sqlite):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE controle_emissao_certidoes
                SET status_processo = ?
                WHERE cnpj = ?
            ''', (status_processo, cnpj))
            conn.commit()