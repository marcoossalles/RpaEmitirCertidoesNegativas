from config import settings
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from automation.gerenciado_arquivo import CriadorPastasCertidoes
from automation.certidao_trabalhista import CertidaoTrabalhista
from automation.certidao_fgts import CertidaoFgts
from automation.certidao_estadual import CertidaoEstadual
from automation.certidao_municipal import CertidaoMunicipal
from automation.genreciador_planilha import PlanilhaMensalDuplicador
import json

CriadorPastasCertidoes().criar_estrutura_pastas()
# Cria uma instância única
duplicador = PlanilhaMensalDuplicador()

# Primeiro, duplica a aba do próximo mês se não existir
duplicador.duplicar_aba_mensal()

# Lê os dados da aba atual
lista_empresas = duplicador.ler_aba_mes_atual(linha_titulo=7, linha_dados=8)

linha_dados = 8  # linha inicial dos dados (conforme seu parâmetro)

for item in lista_empresas:
    if (item['Status'] == 'Suspenso' or 'Paralizado' and item['Status Processamento'] is None):
        for idx, item in enumerate(lista_empresas):
            trabalhista = None,
            fgts = None,
            certidao_mun = None,
            certidao_sefaz = None,
            fazendaria_previdenvia = None,
            status_processamentos = None
            status_resultados = {}
            for x in item:
                if item[x] is None:
                    if x == 'TRABALHISTA' and item[x] is None:
                        status_resultados[x] = CertidaoTrabalhista().acessar_site(item['CNPJ'], item['Empresas'])
                    elif x == 'FGTS' and item[x] is None:
                        status_resultados[x] = CertidaoFgts().acessar_site(item['CNPJ'], item['Empresas'])
                    elif x == 'Certidão Sefaz' and item[x] is None:
                        status_resultados[x] = CertidaoEstadual().acessar_site(item['CNPJ'], item['Empresas'])
                    elif x == 'Status Processamento' and item[x] is None:
                        status_resultados[x] = True
            linha_planilha = linha_dados + idx
            duplicador.escrever_status_linha(
                nome_aba="Agosto 2025",
                linha=linha_planilha,
                dicionario_status=status_resultados,
                linha_titulo=7
            )