import logging
import requests
import os


class ApiCertidaoFgts:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL_INFOSIMPLES')+os.getenv('INFOSIMPLES_CAIXA_REGULARIDADE')
        self.token = os.getenv('TOKEN_API_INFOSIMPLES')

    def emitir_certidao_fgts(self, cnpj):
        timeout=300
        try:
            if not self.base_url or not self.endpoint:
                raise ValueError("Base URL ou endpoint não configurados.")

            url = f"{self.base_url}{self.endpoint}"
            payload = {
                "cnpj": cnpj,
                "token": self.token,
                "timeout": timeout
            }

            response = requests.post(url, json=payload, timeout=timeout)
            response.raise_for_status()

            response_json = response.json()

            if response_json.get('code') == 200:
                logging.info("Retorno com sucesso.")
                return response_json.get('data')
            elif 600 <= response_json.get('code', 0) <= 799:
                mensagem = (
                    f"Resultado sem sucesso.\n"
                    f"Código: {response_json.get('code')} "
                    f"({response_json.get('code_message')})\n"
                    f"Erros: {'; '.join(response_json.get('errors', []))}"
                )
                logging.warning(mensagem)
            else:
                logging.warning("Resposta inesperada: %s", response_json)

            logging.debug("Cabeçalho da consulta: %s", response_json.get('header'))
            logging.debug("URLs (HTML/PDF): %s", response_json.get('site_receipts'))

        except requests.exceptions.RequestException as e:
            logging.error("Erro de requisição: %s", e)
        except ValueError as e:
            logging.error("Erro de configuração: %s", e)
        except Exception as e:
            logging.exception("Erro inesperado: %s", e)
