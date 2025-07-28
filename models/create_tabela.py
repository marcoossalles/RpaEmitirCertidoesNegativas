import logging
from models.connection import DatabaseConnection
from models.insert import InsertTable
from models.select import SelectTable

# Classe responsável por criar a tabela e gerenciar inserções/consultas
class CreateTable:
    def __init__(self):
        # Instancia os objetos necessários para conexão, inserção e seleção
        self.db = DatabaseConnection()
        self.insert_table = InsertTable()
        self.select_table = SelectTable()

    # Método que cria a tabela e insere dados, se necessário
    def create(self, empresas):
        # Estabelece conexão com o banco de dados
        conection = self.db.connect()
        if not conection:
            logging.error("Erro ao conectar ao banco de dados.")
            return []

        logging.info("Criando tabela controle.")
        try:
            cursor = conection.cursor()
            # Query para criação da tabela, caso não exista
            query = """
                    CREATE TABLE IF NOT EXISTS controle_emissao_certidoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        empresa TEXT NOT NULL,
                        cnpj TEXT NOT NULL UNIQUE,
                        simples_nacional TEXT,
                        grupo TEXT,
                        status TEXT,
                        cidade TEXT,
                        receita_federal TEXT,
                        sefaz_inscricao TEXT,
                        sefaz_certidao TEXT,
                        municipal_inscricao TEXT,
                        municipal_certidao TEXT,
                        fgts TEXT,
                        trabalhista TEXT,
                        status_processo TEXT,
                        data_ultima_atualizacao TEXT
                    );
                    """
            cursor.execute(query)
            conection.commit()
            logging.info("Tabela criada.")

            # Verifica se existem registros pendentes na tabela
            row_count = self.select_table.count_check(conection)
            if row_count == 0:
                # Insere os dados se não houver registros pendentes
                status_insert = self.insert_table.insert(empresas, conection)
                if not status_insert:
                    logging.error("Nenhum dado foi inserido na tabela.")
                    return []
            else:
                logging.info("Dados já existentes na tabela. Inserção ignorada.")
            
            # Retorna os dados pendentes da tabela
            return self.select_table.select_pending(conection)
        except Exception as e:
            # Captura e registra qualquer erro ocorrido durante o processo
            logging.error(f"Erro ao criar tabela ou inserir dados: {e}")
            return []
