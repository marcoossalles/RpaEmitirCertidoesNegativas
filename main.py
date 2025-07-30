from config import settings
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from models.create_tabela import CreateTable
from models.update import UpdateStatus
from models.delete import DeleteTable
from models.export import ExportToExcel
from automation.certidao_trabalhista import CertidaoTrabalhista
from automation.certidao_fgts import CertidaoFgts
from automation.certidao_estadual import CertidaoEstadual
from automation.certidao_municipal import CertidaoMunicipal
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
    cnpj = empresa['cnpj']
    
    status_emissao = CertidaoTrabalhista().acessar_site(cnpj)
    status_emissao_fgts = CertidaoFgts().acessar_site(cnpj)
    status_emissao_estadual = CertidaoEstadual().acessar_site(cnpj)

    if not all([status_emissao, status_emissao_fgts, status_emissao_estadual]):
        # Pelo menos um deles é False → faz o UPDATE
        UpdateStatus().update((cnpj, status_emissao, status_emissao_fgts, status_emissao_estadual))
# Exporta os dados para um arquivo Excel
ExportToExcel().export_to_excel(lista_empresas, 'certidoes_negativas.xlsx')
# Exclui a tabela do banco de dados após o processamento
DeleteTable().delete(connection_sqlite)
