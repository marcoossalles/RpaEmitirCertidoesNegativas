import requests
import os
import logging

from integrations.baixar_pdf_certidao_api import BaixarCertidaoViaApi

class ApiCertidaoTrabalhista:
    def __init__(self):
        # Monta a URL base da API a partir das variáveis de ambiente
        self.base_url = os.getenv('BASE_URL_INFOSIMPLES') + os.getenv('INFOSIMPLES_CERTIDAO_TRABALHISTA')
        # Token de autenticação obtido do ambiente
        self.token = os.getenv('TOKEN_API_INFOSIMPLES')

    def emitir_certidao_trabalhista(self, cnpj, nome_empresa):
        timeout = 60
        tipo = 'TRABALHISTA' 
        try:
            args = {
                "cnpj": cnpj,
                "login_cpf": '70181650169',
                "login_senha": 'Jump00jet@1',
                "token": self.token,
                "timeout": timeout
            }

            # Envia requisição POST para a API
            logging.info(f"Enviando requisição para {self.base_url}")
            response = requests.post(self.base_url, json=args, timeout=timeout)
            response.raise_for_status()

            # Converte resposta para JSON
            response_json = response.json()

            # Verifica se a API retornou sucesso
            if response_json.get('code') == 200:
                logging.info(f"Dados da empresa {nome_empresa} encontrado.")
                # Baixa o arquivo PDF retornado pela API
                status_baixa_certidao = BaixarCertidaoViaApi().baixa_certidao_api(response_json['site_receipts'][0], cnpj, nome_empresa, tipo)
                return status_baixa_certidao

            # Caso a API retorne erro
            else:
                mensagem = (
                    f"Resultado sem sucesso. "
                    f"Código: {response_json.get('code')} ({response_json.get('code_message')})"
                    + "; ".join(response_json.get("errors", []))
                )
                logging.error(mensagem)
                return []

        except requests.exceptions.RequestException as e:
            logging.error("Erro de requisição: %s", e)
            return []
        except ValueError as e:
            logging.error("Erro de configuração: %s", e)
            return []
        except Exception as e:
            logging.exception("Erro inesperado: %s", e)
            return []