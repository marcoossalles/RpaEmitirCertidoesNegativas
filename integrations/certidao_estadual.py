import requests
import logging
import os


class ApiCertidaoEstadual:
    def __init__(self, token_api_info_simples: str):
        self.token_api_info_simples = token_api_info_simples
        self.base_url = os.getenv("BASE_URL_INFOSIMPLES") + os.getenv("CERTIDAO_ESTADUAL")

    def emitir_certidao_estadual(self, cnpj: str):
        timeout = 300
        try:
            args = {
                "cnpj": cnpj,
                "token": self.token_api_info_simples,
                "timeout": timeout
            }

            logging.info(f"Enviando requisição para {self.base_url} com CNPJ: {cnpj}")
            response = requests.post(self.base_url, json=args, timeout=timeout)  # usando `json=` em vez de form-data
            response.raise_for_status()

            response_json = response.json()

            if response_json.get("code") == 200:
                logging.info("Retorno com sucesso.")
                print("Dados: ", response_json.get("data"))
            elif 600 <= response_json.get("code", 0) <= 799:
                mensagem = (
                    "Resultado sem sucesso. Leia para saber mais:\n"
                    f"Código: {response_json.get('code')} ({response_json.get('code_message')})\n"
                    + "; ".join(response_json.get("errors", []))
                )
                logging.warning(mensagem)
                print(mensagem)

            print("Cabeçalho da consulta: ", response_json.get("header"))
            print("URLs de visualização (HTML/PDF): ", response_json.get("site_receipts"))

        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição: {e}")
        except ValueError as e:
            logging.error(f"Erro ao interpretar JSON: {e}")
