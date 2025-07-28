import logging

class SelectTable:
    def __init__(self):
        pass

    def select(self, conection):
        try:
            cursor = conection.cursor()
            logging.info("Selecionando dados da tabela controle_emissao_certidoes.")
            cursor.execute('SELECT * FROM controle_emissao_certidoes')
            return cursor.fetchall()
        except Exception as e:
            logging.error(f"Erro ao buscar dados: {e}")
            return []
        
    def select_pendente(self, conection):
        try:
            cursor = conection.cursor()
            cursor.execute("SELECT * FROM controle_emissao_certidoes WHERE status_processo = 'pendente';")
            colunas = [desc[0] for desc in cursor.description]
            resultados = cursor.fetchall()
            dados_com_colunas = [dict(zip(colunas, linha)) for linha in resultados]

            return dados_com_colunas
        except Exception as e:
            logging.error(f"Erro ao buscar dados: {e}")
            return None
        
    def count_pendentes(self, conection):
        try:
            cursor = conection.cursor()
            logging.info("Contando registros pendentes na tabela controle_emissao_certidoes.")
            cursor.execute("SELECT COUNT(*) FROM controle_emissao_certidoes;")
            row_count = cursor.fetchone()[0]
            return row_count
        except Exception as e:
            logging.error(f"Erro ao contar dados pendentes: {e}")
            return 0