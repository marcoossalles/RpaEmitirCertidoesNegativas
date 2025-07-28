import logging

# Classe responsável por realizar operações de seleção na tabela
class SelectTable:
    def __init__(self):
        pass  # Construtor vazio

    # Método que retorna todos os registros da tabela
    def select(self, conection):
        try:
            cursor = conection.cursor()
            logging.info("Selecionando dados da tabela controle_emissao_certidoes.")
            cursor.execute('SELECT * FROM controle_emissao_certidoes')
            return cursor.fetchall()
        except Exception as e:
            # Registra erro ao tentar buscar os dados
            logging.error(f"Erro ao buscar dados: {e}")
            return []
        
    # Método que retorna os registros com status_processo igual a 'pendente'
    def select_pending(self, conection):
        try:
            cursor = conection.cursor()
            cursor.execute("SELECT * FROM controle_emissao_certidoes WHERE status_processo = 'pendente';")
            
            # Obtém os nomes das colunas da tabela
            colunas = [desc[0] for desc in cursor.description]
            # Busca todas as linhas retornadas
            resultados = cursor.fetchall()
            # Combina os nomes das colunas com os valores das linhas
            dados_com_colunas = [dict(zip(colunas, linha)) for linha in resultados]

            return dados_com_colunas
        except Exception as e:
            # Registra erro ao tentar buscar os dados
            logging.error(f"Erro ao buscar dados: {e}")
            return None
        
    # Método que conta a quantidade de registros na tabela
    def count_check(self, conection):
        try:
            cursor = conection.cursor()
            logging.info("Contando registros pendentes na tabela controle_emissao_certidoes.")
            cursor.execute("SELECT COUNT(*) FROM controle_emissao_certidoes;")
            # Obtém a contagem de registros
            row_count = cursor.fetchone()[0]
            return row_count
        except Exception as e:
            # Registra erro ao tentar contar os registros
            logging.error(f"Erro ao contar dados pendentes: {e}")
            return 0
