from logs import log_config
from config import settings
import logging

from automation.gerenciado_arquivo import CriadorPastasCertidoes
from automation.genreciador_planilha import PlanilhaMensalDuplicador
from automation.certidao_trabalhista import CertidaoTrabalhista
from automation.certidao_fgts import CertidaoFgts
from automation.certidao_estadual import CertidaoEstadual
from automation.certidao_municipal import CertidaoMunicipal
from integrations.integracao_receita_federal import ApiCertidaoPgfn
from integrations.integracao_certidao_fgts import ApiCertidaoFgts
from integrations.integracao_certidao_estadual import ApiCertidaoEstadual
from integrations.integracao_certidao_municipal import ApiCertidaoMunicipalGoiania
from integrations.integracao_certidao_trabalhista import ApiCertidaoTrabalhista


#Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#Criação da estrutura de pastas
logging.info("Criando estrutura de pastas para certidões.")
CriadorPastasCertidoes().criar_estrutura_pastas()

#Instância do gerenciador da planilha
duplicador = PlanilhaMensalDuplicador()

#Duplica a aba do próximo mês, se necessário
logging.info("Verificando e duplicando aba mensal.")
duplicador.duplicar_aba_mensal()

#Lê os dados da aba atual
logging.info("Lendo dados da aba do mês atual.")
lista_empresas = duplicador.ler_aba_mes_atual(linha_titulo=7, linha_dados=8)

linha_dados = 8  # linha inicial dos dados na planilha

#Itera sobre os dados das empresas
for idx, item in enumerate(lista_empresas):
    try:
        status = item.get('Status')
        status_proc = item.get('Status Processamento')

        if status != ['Suspenso', 'Paralizado'] and status_proc is None:
            logging.info(f"Processando empresa {item.get('Empresas')} - CNPJ: {item.get('CNPJ')}")

            status_resultados = {}

            for campo in item:
                if item[campo] is None:
                    if campo == 'TRABALHISTA':
                        logging.info("Emitindo certidão TRABALHISTA.")
                        status_resultados[campo] = ApiCertidaoTrabalhista().emitir_certidao_trabalhista(item['CNPJ'], item['Empresas'])#CertidaoTrabalhista().acessar_site(item['CNPJ'], item['Empresas'])

                    elif campo == 'Certidão Mun.':
                        logging.info("Emitindo certidão MUNICIPAL.")
                        status_resultados[campo] = ApiCertidaoMunicipalGoiania().emitir_certidao_municipal(item['CNPJ'], item['Empresas'])#CertidaoMunicipal().acessar_site(item['Inscrição Mun.'], item['Empresas'])

                    elif campo == 'FGTS':
                        logging.info("Emitindo certidão FGTS.")
                        status_resultados[campo] = ApiCertidaoFgts().emitir_certidao_fgts(item['CNPJ'], item['Empresas'])#CertidaoFgts().acessar_site(item['CNPJ'], item['Empresas'])

                    elif campo == 'Certidão Sefaz':
                        logging.info("Emitindo certidão ESTADUAL (SEFAZ).")
                        status_resultados[campo] = ApiCertidaoEstadual().emitir_certidao_estadual(item['CNPJ'], item['Empresas'])#CertidaoEstadual().acessar_site(item['CNPJ'], item['Empresas'])

                    elif campo == 'Fazendaria/Previdenciária':
                        logging.info("Emitindo certidão RECEITA FEDERAL.")
                        status_resultados[campo] = True#ApiCertidaoPgfn().emitir_certidao_pgfn(item['CNPJ'], item['Empresas'])
                        
                    elif campo == 'Status Processamento':
                        logging.info("Marcando como processado.")
                        status_resultados[campo] = True

            linha_planilha = linha_dados + idx
            duplicador.escrever_status_linha(
                nome_aba="Agosto 2025",
                linha=linha_planilha,
                dicionario_status=status_resultados,
                linha_titulo=7
            )
            logging.info(f"Status escrito na planilha para linha {linha_planilha}.")
    except Exception as e:
        logging.error(f"Erro ao processar empresa {item.get('Empresas')} - CNPJ: {item.get('CNPJ')}: {e}")