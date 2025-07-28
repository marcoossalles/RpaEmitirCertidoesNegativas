from models.connection import DatabaseConnection

class UpdateStatus:
    def __init__(self):
        self.db = DatabaseConnection()

    def update(self, record_id, new_status, error_message=None):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE controle_emissao_certidoes
                SET status = ?, error_message = ?
                WHERE id = ?
            ''', (new_status, error_message, record_id))
            conn.commit()
