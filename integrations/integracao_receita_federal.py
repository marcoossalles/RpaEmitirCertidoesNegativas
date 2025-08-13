import requests
import logging
import os

from integrations.baixar_pdf_certidao_api import BaixarCertidaoViaApi


class ApiCertidaoPgfn:
    def __init__(self):
        # Recupera o token de autenticação da API a partir das variáveis de ambiente
        self.token_api = os.getenv('TOKEN_API_INFOSIMPLES')
        # Monta a URL base da API a partir de variáveis de ambiente
        self.url = os.getenv("BASE_URL_INFOSIMPLES") + os.getenv("INFOSIMPLES_CERTIDAO_RECEITA_FEDERAL")

    def emitir_certidao_pgfn(self, cnpj, nome_empresa):
        timeout = 300  # Tempo limite para operações que precisam aguardar
        tipo = 'FEDERAL'  # Tipo fixo de certidão
        try:
            # Parâmetros a serem enviados na requisição POST
            args = {
                "cnpj": cnpj,
                "preferencia_emissao": 'nova',  # Solicita emissão de nova certidão
                "token": self.token_api,
                "timeout": timeout
            }

            # Log informando a URL de destino
            logging.info(f"Enviando requisição para {self.url}")
            # Envia a requisição POST para a API
            response = requests.post(self.url, json=args, timeout=timeout)
            # Lança exceção se o status HTTP indicar erro (>= 400)
            response.raise_for_status()
            # Converte o retorno da API em formato JSON
            response_json = response.json()

            # Se a API retornou sucesso no campo "code"
            if response_json.get("code") == 200:
                # Baixa o arquivo PDF usando a URL retornada
                logging.info(f"Dados da empresa {nome_empresa} encontrado.")
                status_baixa_certidao = BaixarCertidaoViaApi().baixa_certidao_api(response_json['site_receipts'][0], cnpj, nome_empresa, tipo)
                return status_baixa_certidao

            else:
                # Monta mensagem de erro com código, mensagem e lista de erros
                mensagem = (
                    f"Resultado sem sucesso."
                    f"Código: {response_json.get('code')} ({response_json.get('code_message')})"
                    + "; ".join(response_json.get("errors", []))
                )
                logging.error(mensagem)
                return False

        # Captura erros relacionados à requisição HTTP
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição: {e}")
            return False

        # Captura quaisquer outros erros inesperados
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            return False
