# import requests
# import os
# import logging
# import base64
# import aes256  # precisa ter a biblioteca AES que você está usando

# class ApiCertidaoTrabalhista:
#     def __init__(self, token_api, chave_cripto):
#         self.token_api = token_api
#         self.chave_cripto = chave_cripto
#         self.url = self.base_url = os.getenv("BASE_URL_INFOSIMPLES") + os.getenv("INFOSIMPLES_CERTIDAO_TRABALHISTA")

#     def emitir_certidao_trabalhista(self, cnpj=None, cpf=None, login_cpf=None, login_senha=None, certificado_path=None, senha_certificado=None):
#         try:
#             Leitura e criptografia do certificado
#             with open(certificado_path, "rb") as f:
#                 certificado_base64 = base64.b64encode(f.read()).decode()

#             certificado_cript = aes256.encrypt(certificado_base64, self.chave_cripto).replace("+", "-").replace("/", "_").rstrip("=")
#             senha_cript = aes256.encrypt(senha_certificado, self.chave_cripto).replace("+", "-").replace("/", "_").rstrip("=")

#             args = {
#                 "cnpj": cnpj,
#                 "cpf": cpf,
#                 "login_cpf": login_cpf,
#                 "login_senha": login_senha,
#                 "pkcs12_cert": certificado_cript,
#                 "pkcs12_pass": senha_cript,
#                 "token": self.token_api,
#                 "timeout": 300
#             }

#             logging.info(f"Enviando requisição para {self.url}")
#             response = requests.post(self.url, json=args, timeout=30)
#             response.raise_for_status()
#             response_json = response.json()

#             if response_json.get("code") == 200:
#                 logging.info("Retorno com sucesso.")
#                 return response_json.get("data")
#             elif 600 <= response_json.get("code", 0) <= 799:
#                 mensagem = (
#                     f"Resultado sem sucesso.\nCódigo: {response_json.get('code')} ({response_json.get('code_message')})\n"
#                     + "; ".join(response_json.get("errors", []))
#                 )
#                 logging.warning(mensagem)
#                 return mensagem

#             return response_json

#         except requests.exceptions.RequestException as e:
#             logging.error(f"Erro na requisição: {e}")
#         except Exception as e:
#             logging.error(f"Erro inesperado: {e}")
