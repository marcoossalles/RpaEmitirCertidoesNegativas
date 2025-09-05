import json
import os
from config import settings

from models.genrenciador_processamento import GerenciadorProcessamento
from manager_logs.logger_manager import Logger
from models.gerenciado_arquivo import CriadorPastasCertidoes
from models.genreciador_planilha import CriarAbaPlanilha
from automation.certidao_trabalhista import CertidaoTrabalhista
from automation.certidao_fgts import CertidaoFgts
from automation.certidao_estadual import CertidaoEstadual
from automation.certidao_municipal import CertidaoMunicipal
from integrations.integracao_receita_federal import ApiCertidaoPgfn
from services.db_services import DbServices


class Main:
    def __init__(self):
        #Criação da estrutura de gerenciamento de processamento
        GerenciadorProcessamento()

        logging = Logger("EmissaoCertidao", log_file ='.\\Task\\Task_20250905\\logs\\log.txt')

        #Criação da estrutura de pastas
        CriadorPastasCertidoes().criar_estrutura_pastas()

        #Leitura do arquivo EMPRESA.json
        logging.info("Realizando leitura obejto empresas.json")
        with open(r'data\empresas.json', 'r', encoding='utf-8') as file:
            lista_empresa = json.load(file)

        #Instância do serviço de banco de dados
        db_services = DbServices()

        #Criação da tabela, se não existir
        db_services.criar_tabela()

        #Inserção das EMPRESA no banco, ignorando duplicatas
        db_services.inserir_empresas(lista_empresa)

        #busca das EMPRESA que precisam ser processadas
        lista_empresa_db = db_services.buscar_pendentes()

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
        for empresa in lista_empresa_db:
            try:
                # status = empresa.get('Status')
                # status_proc = empresa.get('Status Processamento')

                if empresa['status'] != ['Suspenso', 'Paralizado']:
                    logging.info(f"Processando empresa {empresa.get('empresa')} - CNPJ: {empresa.get('cnpj')}")

                    status_resultados = {}

                    for campo in empresa:
                        if campo == 'trabalhista':
                            logging.info("Emitindo certidão TRABALHISTA.")
                            status_resultados[campo] = CertidaoTrabalhista().acessar_site(empresa['cnpj'], empresa['empresa'])

                        elif campo == 'municipal_certidao' and empresa['cidade'] == 'Goiânia - GO':
                            logging.info("Emitindo certidão MUNICIPAL.")
                            status_resultados[campo] = CertidaoMunicipal().acessar_site(empresa['municipal_cae'], empresa['empresa'], empresa['cidade'])

                        elif campo == 'fgts':
                            logging.info("Emitindo certidão FGTS.")
                            status_resultados[campo] = CertidaoFgts().acessar_site(empresa['cnpj'], empresa['empresa'])

                        elif campo == 'estadual':
                            logging.info("Emitindo certidão ESTADUAL (SEFAZ).")
                            status_resultados[campo] = CertidaoEstadual().acessar_site(empresa['cnpj'], empresa['empresa'])

                        elif campo == 'receita_federal':
                            logging.info("Emitindo certidão RECEITA FEDERAL.")
                            status_resultados[campo] = ApiCertidaoPgfn().emitir_certidao_pgfn(empresa['cnpj'], empresa['empresa'])
                            
                        elif campo == 'status_processamento':
                            logging.info("Marcando como processado.")
                            campos_verificacao = ['receita_federal', 'estadual', 'municipal_certidao', 'fgts', 'trabalhista']
                            
                            if any(status_resultados[c] == None for c in campos_verificacao):
                                status_resultados[campo] = "PROCESSO PENDENTE"
                            else:
                                status_resultados[campo] = "OK"

                    #atualiza tabela com os status
                    db_services.atualizar_empresa(empresa['cnpj'], status_resultados)
            except Exception as e:
                logging.error(f"Erro ao processar empresa {empresa.get('EMPRESA')} - CNPJ: {empresa.get('CNPJ')}: {e}")

        #Criação da aba mensal, se necessário
        CriarAbaPlanilha().criar_aba_mensal()

        db_services.gerar_relatorio(os.getenv('PASTA_PLANILHA_CNPJS'))

if __name__ == "__main__":
    main = Main()