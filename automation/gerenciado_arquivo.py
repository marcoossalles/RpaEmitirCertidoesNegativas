import os
import shutil
import logging
from datetime import datetime

# Configura o logging para exibir mensagens no terminal
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CriadorPastasCertidoes:
    def __init__(self):
        """
        Inicializa a classe pegando o mês e o ano atual automaticamente.
        Define o caminho base e as subpastas a serem criadas.
        """
        agora = datetime.now()
        self.ano = str(agora.year)
        self.mes = f"{agora.month:02d}"  # Garante dois dígitos, exemplo: "07"
        self.caminho_base = r"C:\empresas"
        self.subpastas = ["ESTADUAL", "FEDERAL", "FGTS", "MUNICIPAL"]

    def criar_estrutura_pastas(self):
        """
        Cria a estrutura de pastas no formato:
        Certidões {ano} → {mes} {ano} → [ESTADUAL, FEDERAL, FGTS, MUNICIPAL]
        """
        pasta_ano = os.path.join(self.caminho_base, f"Certidões {self.ano}")
        pasta_mes = os.path.join(pasta_ano, f"{self.mes} {self.ano}")

        try:
            # Cria a pasta do mês, se ainda não existir
            os.makedirs(pasta_mes, exist_ok=True)

            # Cria as subpastas dentro da pasta do mês
            for subpasta in self.subpastas:
                caminho_subpasta = os.path.join(pasta_mes, subpasta)
                os.makedirs(caminho_subpasta, exist_ok=True)

            logging.info(f"Pastas de {self.mes}/{self.ano} criadas com sucesso em '{pasta_mes}'.")
        except Exception as e:
            logging.error(f"Erro ao criar estrutura de pastas: {e}")

    def salvar_pdf(self, caminho_pdf_origem, cnpj, tipo):
        """
        Move o PDF já nomeado corretamente para a pasta correta na estrutura:
        Certidões {ano}/{mes} {ano}/{tipo}/{CNPJ}/
        
        Parâmetros:
        - caminho_pdf_origem: caminho do arquivo PDF a ser movido
        - cnpj: CNPJ da empresa (será limpo para conter apenas números)
        - tipo: tipo de certidão (ex: "FGTS", "ESTADUAL")
        """
        try:
            # Limpa o CNPJ (mantém apenas os números)
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

            # Caminho final de destino do arquivo PDF
            pasta_destino = os.path.join(
                self.caminho_base,
                f"Certidões {self.ano}",
                f"{self.mes} {self.ano}",
                tipo.upper(),
                cnpj_limpo
            )

            # Garante que o diretório de destino existe
            os.makedirs(pasta_destino, exist_ok=True)

            # Define o caminho completo do arquivo de destino
            nome_arquivo = os.path.basename(caminho_pdf_origem)
            caminho_pdf_destino = os.path.join(pasta_destino, nome_arquivo)

            # Move o arquivo para o destino
            shutil.move(caminho_pdf_origem, caminho_pdf_destino)

            logging.info(f"Arquivo '{nome_arquivo}' movido para '{caminho_pdf_destino}'.")
            return caminho_pdf_destino
        except Exception as e:
            logging.error(f"Erro ao mover PDF '{caminho_pdf_origem}' para pasta do tipo '{tipo}': {e}")
            raise
