import logging
import json
from datetime import datetime
from config import settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from automation.genrenciador_processamento import GerenciadorProcessamento
from automation.gerenciado_arquivo import CriadorPastasCertidoes
from automation.genreciador_planilha import PlanilhaMensalDuplicador
from automation.certidao_trabalhista import CertidaoTrabalhista
from automation.certidao_fgts import CertidaoFgts
from automation.certidao_estadual import CertidaoEstadual
from automation.certidao_municipal import CertidaoMunicipal
from integrations.integracao_receita_federal import ApiCertidaoPgfn

#Criação da estrutura de gerenciamento de processamento
logging.info("Criando estrutura de pastas de gerenciamento de processamento.")
GerenciadorProcessamento()

#Criação da estrutura de pastas
logging.info("Criando estrutura de pastas para certidões.")
CriadorPastasCertidoes().criar_estrutura_pastas()

#Leitura do arquivo EMPRESA.json
logging.info("Realizando leitura obejto empresas.json")
with open('empresas.json', 'r', encoding='utf-8') as file:
    lista_EMPRESA = json.load(file)

#Instância do gerenciador da planilha
#duplicador = PlanilhaMensalDuplicador()

#Duplica a aba do próximo mês, se necessário
# logging.info("Verificando e duplicando aba mensal.")
# duplicador.duplicar_aba_mensal()

#Lê os dados da aba atual
# logging.info("Lendo dados da aba do mês atual.")
# lista_EMPRESA = duplicador.ler_aba_mes_atual(linha_titulo=7, linha_dados=8)

#linha_dados = 8  # linha inicial dos dados na planilha

#Itera sobre os dados das EMPRESA
for empresa in lista_EMPRESA:
    try:
        # status = empresa.get('Status')
        # status_proc = empresa.get('Status Processamento')

        if empresa['STATUS'] != ['Suspenso', 'Paralizado']:
            logging.info(f"Processando empresa {empresa.get('EMPRESA')} - CNPJ: {empresa.get('CNPJ')}")

            status_resultados = {}

            for campo in empresa:
                if campo == 'TRABALHISTA':
                    logging.info("Emitindo certidão TRABALHISTA.")
                    status_resultados[campo] = CertidaoTrabalhista().acessar_site(empresa['CNPJ'], empresa['EMPRESA'])

                elif campo == 'MUNICIPAL':
                    logging.info("Emitindo certidão MUNICIPAL.")
                    status_resultados[campo] = "OK"#CertidaoMunicipal().acessar_site(empresa['MUNICIPAL']['CAE'], empresa['MUNICIPAL']['EMPRESA'], empresa['CIDADE'])

                elif campo == 'FGTS':
                    logging.info("Emitindo certidão FGTS.")
                    status_resultados[campo] = CertidaoFgts().acessar_site(empresa['CNPJ'], empresa['EMPRESA'])

                elif campo == 'SEFAZ':
                    logging.info("Emitindo certidão ESTADUAL (SEFAZ).")
                    status_resultados[campo] = CertidaoEstadual().acessar_site(empresa['CNPJ'], empresa['EMPRESA'])

                elif campo == 'RECEITA FEDERAL':
                    logging.info("Emitindo certidão RECEITA FEDERAL.")
                    status_resultados[campo] = ApiCertidaoPgfn().emitir_certidao_pgfn(empresa['CNPJ'], empresa['EMPRESA'])
                    
                elif campo == 'STATUS PROCESSAMENTO':
                    logging.info("Marcando como processado.")
                    status_resultados[campo] = "OK"
        #atualiza fila

            # linha_planilha = linha_dados + idx
            # duplicador.escrever_status_linha(
            #     linha=linha_planilha,
            #     dicionario_status=status_resultados,
            #     linha_titulo=7
            # )
            #logging.info(f"Status escrito na planilha para linha {linha_planilha}.")
    except Exception as e:
        logging.error(f"Erro ao processar empresa {empresa.get('EMPRESA')} - CNPJ: {empresa.get('CNPJ')}: {e}")