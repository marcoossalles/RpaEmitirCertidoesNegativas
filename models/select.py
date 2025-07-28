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