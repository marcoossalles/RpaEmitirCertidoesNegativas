import requests
import logging
import os

from integrations.baixar_pdf_certidao_api import BaixarCertidaoViaApi

class ApiCertidaoEstadual:
    def __init__(self):
        # Token de autenticação obtido de variável de ambiente
        self.token = os.getenv('TOKEN_API_INFOSIMPLES')
        # URL da API montada a partir das variáveis de ambiente
        self.base_url = os.getenv("BASE_URL_INFOSIMPLES") + os.getenv("INFOSIMPLES_CERTIDAO_ESTADUAL")

    def emitir_certidao_estadual(self, cnpj, nome_empresa):
        extensao = '.pdf'
        timeout = 60  # Tempo limite de espera em segundos
        tipo = 'ESTADUAL'  # Tipo de certidão
        try:
            # Monta o corpo da requisição
            args = {
                "cnpj": cnpj,
                "token": self.token,
                "timeout": timeout
            }

            # Envia a requisição POST para a API
            logging.info(f"Enviando requisição para: {self.base_url}")
            response = requests.post(self.base_url, json=args, timeout=timeout)
            response.raise_for_status()  # Lança exceção em caso de erro HTTP

            # Converte a resposta para JSON
            response_json = response.json()

            # Se a API retornou sucesso
            if response_json.get("code") == 200:
                if response.get("code_message") != "CERTIDAO DE DEBITO INSCRITO EM DIVIDA ATIVA - NEGATIVA":
                    negativa = "PENDENTE"
                else:
                    negativa = "OK"
                logging.info(f"Dados da empresa {nome_empresa} encontrado.")
                # Baixa o arquivo PDF usando a URL retornada
                status_baixa_certidao = BaixarCertidaoViaApi().baixa_certidao_api(response_json['data'][0]['site_receipt'],cnpj,nome_empresa,tipo, extensao, negativa)
                return status_baixa_certidao

            # Caso a API retorne erro ou código diferente de 200
            else:
                mensagem = (
                    "Resultado sem sucesso. Leia para saber mais: "
                    f"Código: {response_json.get('code')} ({response_json.get('code_message')})"
                    + "; ".join(response_json.get("errors", []))
                )
                logging.warning(mensagem)
                return False

        # Tratamento de erros específicos de timeout
        except requests.exceptions.Timeout:
            logging.error("Tempo limite excedido na requisição para emissão da certidão.")
            return False
        # Tratamento de erros relacionados a requisições HTTP
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro na requisição: {e}")
            return False
        # Tratamento de erro ao interpretar o JSON
        except ValueError as e:
            logging.error(f"Erro ao interpretar JSON: {e}")
            return False
        # Tratamento de qualquer outro erro inesperado
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            return False
