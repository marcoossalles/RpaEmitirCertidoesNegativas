import requests
import logging
import os

from integrations.baixar_pdf_certidao_api import BaixarCertidaoViaApi

class ApiCertidaoMunicipalGoiania:
    def __init__(self):
        # Token de autenticação da API obtido via variável de ambiente
        self.token_api = os.getenv('TOKEN_API_INFOSIMPLES')
        # Monta a URL base da API a partir de variáveis de ambiente
        self.url = os.getenv("BASE_URL_INFOSIMPLES") + os.getenv("INFOSIMPLES_CERTIDAO_MUNICIPAL")

    def emitir_certidao_municipal(self, cnpj, nome_empresa):
        extensao = '.html'
        timeout = 60  # Tempo máximo de espera da requisição
        tipo = 'MUNICIPAL'
        try:
            # Monta os parâmetros que serão enviados para a API
            args = {
                "cnpj": cnpj,
                "token": self.token_api,
                "timeout": timeout
            }

            # Envia a requisição POST para a API
            logging.info(f"Enviando requisição para {self.url}")
            response = requests.post(self.url, json=args, timeout=300)
            response.raise_for_status()  # Lança erro se o status HTTP for >= 400

            # Converte a resposta em JSON
            response_json = response.json()

            # Caso de sucesso
            if response_json.get("code") == 200:
                # Baixa o arquivo PDF usando a URL retornada
                logging.info(f"Dados da empresa {nome_empresa} encontrado.")
                status_baixa_certidao = BaixarCertidaoViaApi().baixa_certidao_api(response_json['data'][0]['site_receipt'], cnpj, nome_empresa, tipo, extensao)
                return status_baixa_certidao

            # Caso de retorno inesperado da API
            else:
                # Monta mensagem de erro com código, mensagem e lista de erros
                mensagem = (
                    f"Resultado sem sucesso."
                    f"Código: {response_json.get('code')} ({response_json.get('code_message')})"
                    + "; ".join(response_json.get("errors", []))
                )
                logging.warning(mensagem)
                return None

        # Erros relacionados à conexão ou requisição HTTP
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição: {e}")
            return None

        # Qualquer outro erro não previsto
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            return None
