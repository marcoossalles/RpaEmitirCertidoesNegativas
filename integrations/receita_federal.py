import requests
import logging


class ApiCertidaoPgfn:
    def __init__(self, token_api):
        self.token_api = token_api
        self.url = "https://api.infosimples.com/api/v2/consultas/receita-federal/pgfn"

    def emitir_certidao_pgfn(self, cnpj=None, cpf=None, preferencia_emissao=None, birthdate=None):
        try:
            args = {
                "cnpj": cnpj,
                "cpf": cpf,
                "preferencia_emissao": preferencia_emissao,
                "birthdate": birthdate,
                "token": self.token_api,
                "timeout": 300
            }

            logging.info(f"Enviando requisição para {self.url}")
            response = requests.post(self.url, json=args, timeout=30)
            response.raise_for_status()
            response_json = response.json()

            if response_json.get("code") == 200:
                logging.info("Retorno com sucesso.")
                return {
                    "status": "sucesso",
                    "dados": response_json.get("data"),
                    "header": response_json.get("header"),
                    "arquivos": response_json.get("site_receipts")
                }

            elif 600 <= response_json.get("code", 0) <= 799:
                mensagem = (
                    f"Resultado sem sucesso.\n"
                    f"Código: {response_json.get('code')} ({response_json.get('code_message')})\n"
                    + "; ".join(response_json.get("errors", []))
                )
                logging.warning(mensagem)
                return {"status": "erro", "mensagem": mensagem}

            else:
                logging.warning(f"Retorno inesperado: {response_json}")
                return {"status": "indefinido", "resposta": response_json}

        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição: {e}")
            return {"status": "erro_rede", "mensagem": str(e)}

        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            return {"status": "erro_interno", "mensagem": str(e)}
