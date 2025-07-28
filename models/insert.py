import logging

class InsertTable:
    def __init__(self):
        pass

    def insert(self, empresas, conection):
        logging.info("Inserindo dados na tabela controle_emissao_certidoes.")
        try:
            with conection:
                cursor = conection.cursor()
                dados = [(
                    e.get("empresa"),
                    e.get("cnpj"),
                    e.get("simples_nacional"),
                    e.get("grupo"),
                    e.get("status"),
                    e.get("cidade"),
                    e.get("receita_federal"),
                    e.get("sefaz_inscricao"),
                    e.get("sefaz_certidao"),
                    e.get("municipal_inscricao"),
                    e.get("municipal_certidao"),
                    e.get("fgts"),
                    e.get("trabalhista"),
                    "pendente",
                    e.get("data_ultima_atualizacao")
                ) for e in empresas]

                cursor.executemany('''
                    INSERT INTO controle_emissao_certidoes (
                        empresa, cnpj, simples_nacional, grupo, status, cidade,
                        receita_federal, sefaz_inscricao, sefaz_certidao,
                        municipal_inscricao, municipal_certidao, fgts, trabalhista,
                        status_processo, data_ultima_atualizacao
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', dados)

                conection.commit()
                logging.info("Dados inseridos com sucesso.")
                return True
            
        except Exception as e:
            logging.error(f"Erro ao inserir dados: {e}")
            return False