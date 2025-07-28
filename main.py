import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from models.create_tabela import CreateTable
from models.update import UpdateStatus
from models.delete import DeleteTable
import json

with open('empresas.json', 'r') as file:
    try:
      logging.info("Lendo o arquivo JSON de empresas.")
      empresas = json.load(file)
      logging.info("Arquivo JSON lido com sucesso.")
    except json.JSONDecodeError as e:
        logging.error(f"Erro ao ler o arquivo JSON: {e}")
        empresas = []

if not empresas:
    logging.info("Nenhuma empresa encontrada no arquivo JSON.")

lista_teste = connection_sqlite = CreateTable().create(empresas)

if not lista_teste:
    print("Nenhum dado foi inserido ou ocorreu um erro.")

for empresa in lista_teste:
    print(f"Empresa: {empresa['empresa']}, CNPJ: {empresa['cnpj']}, Status: {empresa['status']}")