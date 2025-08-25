import logging
import requests
import os

from integrations.baixar_pdf_certidao_api import BaixarCertidaoViaApi

class ApiCertidaoFgts:
    def __init__(self):
        # Monta a URL base da API a partir das variáveis de ambiente
        self.base_url = os.getenv('BASE_URL_INFOSIMPLES') + os.getenv('INFOSIMPLES_CAIXA_REGULARIDADE')
        # Token de autenticação obtido do ambiente
        self.token = os.getenv('TOKEN_API_INFOSIMPLES')

    def emitir_certidao_fgts(self, cnpj, nome_empresa):
        extensao = '.html'
        timeout = 60  # Tempo máximo de espera para requisição
        tipo = 'FGTS'  # Tipo da certidão emitida

        try:
            # Monta o corpo da requisição
            payload = {
                "cnpj": cnpj,
                "token": self.token,
                "timeout": timeout
            }

            # Envia requisição POST para a API
            logging.info(f"Enviando requisição para {self.base_url}")
            response = requests.post(self.base_url, json=payload, timeout=timeout)
            response.raise_for_status()

            # Converte resposta para JSON
            response_json = response.json()
            
            # Se a API retornou 611 e pq existe pendencias
            if response_json.get("code") == 611:
                return "PENDENTE"

            # Verifica se a API retornou sucesso
            if response_json.get('code') == 200:
                negativa = "OK"
                logging.info(f"Dados da empresa {nome_empresa} encontrado.")
                # Baixa o arquivo PDF retornado pela API
                status_baixa_certidao = BaixarCertidaoViaApi().baixa_certidao_api(response_json['data'][0]['site_receipt'], cnpj, nome_empresa, tipo, extensao, negativa)
                return status_baixa_certidao
            # Caso a API retorne erro
            else:
                mensagem = (
                    f"Resultado sem sucesso. "
                    f"Código: {response_json.get('code')} ({response_json.get('code_message')})"
                    + "; ".join(response_json.get("errors", []))
                )
                logging.error(mensagem)
                return None

        except requests.exceptions.RequestException as e:
            logging.error("Erro de requisição: %s", e)
            return None
        except ValueError as e:
            logging.error("Erro de configuração: %s", e)
            return None
        except Exception as e:
            logging.exception("Erro inesperado: %s", e)
            return None