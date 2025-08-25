import requests
import logging
import os

from automation.gerenciado_arquivo import CriadorPastasCertidoes

class BaixarCertidaoViaApi:
    def __init__(self):
        # Define o diretório padrão para salvar downloads
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        # Garante que a pasta de downloads exista
        os.makedirs(self.download_dir, exist_ok=True)
    
    def baixa_certidao_api(self, url, cnpj, nome_empresa, tipo, extensao, negativa):
        try:
            logging.info(f"Baixando certidão da empresa {nome_empresa}")
            # Faz a requisição para baixar o arquivo PDF a partir da URL informada
            response = requests.get(url, timeout=60)
            
            # Verifica se a requisição foi bem-sucedida (status HTTP 200)
            if response.status_code == 200:
                logging.info(f"Certidão baixada com sucesso.")
                
                # Salva o conteúdo como arquivo PDF temporário no diretório de download configurado
                logging.info(f"Salvando certidão {self.download_dir}.")
                caminho_arquivo = os.path.join(self.download_dir, f"{cnpj}_certidao{extensao}")
                with open(caminho_arquivo, "wb") as f:
                    f.write(response.content)

                # Define o novo caminho com o nome da empresa
                caminho_pdf = os.path.join(self.download_dir, f"{nome_empresa}.{extensao}")

                # Renomeia o arquivo baixado
                os.rename(caminho_arquivo, caminho_pdf)
                logging.info(f"PDF renomeado: {cnpj}_certidao.{extensao} -> {nome_empresa}.{extensao}")

                # Move o PDF para a pasta final definida pelo CriadorPastasCertidoes
                CriadorPastasCertidoes().salvar_pdf(caminho_pdf, cnpj, tipo, negativa)

                return "OK"
            else:
                logging.error(f"Erro ao baixar arquivo PDF")
                return "PENDENTE"

        # Trata erros de timeout na requisição
        except requests.exceptions.Timeout:
            logging.error("Tempo limite excedido ao tentar baixar o arquivo.")
            return None
        
        # Trata outros erros relacionados à requisição HTTP
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao fazer requisição: {e}")
            return None
        
        # Trata qualquer outro erro inesperado
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            return None
