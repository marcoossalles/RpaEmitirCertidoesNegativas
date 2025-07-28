import logging
class DeleteTable:
    def __init__(self):
        pass

    def delete(self, contection):
        try:
            with contection:
                logging.info("Deletando dados da tabela controle_emissao_certidoes.")
                cursor = contection.cursor()
                cursor.execute('DELETE FROM controle_emissao_certidoes')
                contection.commit()
                logging.info("Dados deletados com sucesso.")
            return True
        except Exception as e:
            logging.error(f"Erro ao deletar dados: {e}")
            return False
