import pandas as pd
from models.connection import DatabaseConnection

# Classe responsável por exportar os dados da tabela para um arquivo Excel
class ExportToExcel:
    def __init__(self):
        # Instancia o objeto de conexão com o banco de dados
        self.db = DatabaseConnection()

    # Método que exporta os dados da tabela para um arquivo Excel
    def export(self, output_path='certificate_results.xlsx'):
        # Estabelece conexão com o banco de dados
        with self.db.connect() as conn:
            # Executa a consulta SQL e armazena os dados em um DataFrame
            df = pd.read_sql_query("SELECT * FROM controle_emissao_certidoes", conn)
            # Exporta o DataFrame para um arquivo Excel
            df.to_excel(output_path, index=False)
