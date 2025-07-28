from models.connection import DatabaseConnection

# Classe responsável por atualizar o status do processo na tabela
class UpdateStatus:
    def __init__(self):
        # Instancia o objeto de conexão com o banco de dados
        self.db = DatabaseConnection()

    # Método que atualiza o status_processo de uma empresa com base no CNPJ
    def update(self, cnpj, status_processo, connection_sqlite):
        # Estabelece nova conexão com o banco de dados
        with self.db.connect() as conn:
            cursor = conn.cursor()
            # Executa a atualização do campo status_processo onde o CNPJ for correspondente
            cursor.execute('''
                UPDATE controle_emissao_certidoes
                SET status_processo = ?
                WHERE cnpj = ?
            ''', (status_processo, cnpj))
            # Confirma as alterações no banco
            conn.commit()
