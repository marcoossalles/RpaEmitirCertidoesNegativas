import logging

# Classe responsável por deletar os dados da tabela
class DeleteTable:
    def __init__(self):
        pass  # Construtor vazio

    # Método para deletar todos os dados da tabela controle_emissao_certidoes
    def delete(self, contection):
        try:
            # Utiliza o contexto da conexão para garantir fechamento seguro
            with contection:
                logging.info("Deletando dados da tabela controle_emissao_certidoes.")
                cursor = contection.cursor()
                cursor.execute('DELETE FROM controle_emissao_certidoes')
                contection.commit()
                logging.info("Dados deletados com sucesso.")
            return True
        except Exception as e:
            # Registra qualquer erro ocorrido durante a exclusão
            logging.error(f"Erro ao deletar dados: {e}")
            return False
