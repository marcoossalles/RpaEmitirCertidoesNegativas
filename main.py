import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from models.create_tabela import CreateTable
from models.update import UpdateStatus
from models.delete import DeleteTable
from models.export import ExportToExcel
from automation.certidao_trablhista import CertidaoTrabalhista

import json

# Lê o arquivo JSON contendo as empresas
with open('empresas.json', 'r') as file:
    try:
        logging.info("Lendo o arquivo JSON de empresas.")
        empresas = json.load(file)
        logging.info("Arquivo JSON lido com sucesso.")
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao ler o arquivo JSON: {e}")
        empresas = []

# Verifica se a lista de empresas está vazia
if not empresas:
    logging.info("Nenhuma empresa encontrada no arquivo JSON.")
    exit()

# Cria a tabela e insere os dados das empresas
lista_empresas = connection_sqlite = CreateTable().create(empresas)

# Verifica se os dados foram inseridos corretamente
if not lista_empresas:
    print("Nenhum dado foi inserido ou ocorreu um erro.")

# Itera sobre a lista de empresas e atualiza o status
for empresa in lista_empresas:
    CertidaoTrabalhista().acessar_site()


    status_update = UpdateStatus().update(empresa['cnpj'], 'processando', connection_sqlite)

# Exporta os dados para um arquivo Excel
ExportToExcel().export_to_excel(lista_empresas, 'certidoes_negativas.xlsx')

# Exclui a tabela do banco de dados após o processamento
DeleteTable().delete(connection_sqlite)
