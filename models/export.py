import pandas as pd
from models.connection import DatabaseConnection

class ExportToExcel:
    def __init__(self):
        self.db = DatabaseConnection()

    def export(self, output_path='certificate_results.xlsx'):
        with self.db.connect() as conn:
            df = pd.read_sql_query("SELECT * FROM controle_emissao_certidoes", conn)
            df.to_excel(output_path, index=False)
