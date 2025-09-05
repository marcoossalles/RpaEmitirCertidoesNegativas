import os
import shutil
from datetime import datetime
from manager_logs.logger_manager import Logger


class CriadorPastasCertidoes:
    def __init__(self):
        self.logging = Logger("EmissaoCertidao")
        """
        Inicializa a classe pegando o mês e o ano atual automaticamente.
        Define os caminhos base (positivas e negativas) e as subpastas a serem criadas.
        """
        agora = datetime.now()
        self.ano = str(agora.year)
        self.mes = f"{agora.month:02d}"  # Ex: "08"
        self.caminhos_base = [
            os.getenv('PASTA_CERTIDOES_NEGATIVAS'),
            os.getenv('PASTA_CERTIDOES_POSITIVAS')
        ]
        self.subpastas = ["ESTADUAL", "FEDERAL", "FGTS", "MUNICIPAL", "TRABALHISTA"]

    def criar_estrutura_pastas(self):
        self.logging.info("Iniciando criação da estrutura de pastas para certidões.")
        """
        Cria a estrutura de pastas no formato:
        {caminho_base} → Certidões {ano} → {mes} {ano} → [ESTADUAL, FEDERAL, FGTS, MUNICIPAL, TRABALHISTA]
        em cada um dos caminhos base (positivas e negativas).
        """
        for caminho_base in self.caminhos_base:
            pasta_ano = os.path.join(caminho_base, f"Certidões {self.ano}")
            pasta_mes = os.path.join(pasta_ano, f"{self.mes} {self.ano}")

            try:
                os.makedirs(pasta_mes, exist_ok=True)

                for subpasta in self.subpastas:
                    caminho_subpasta = os.path.join(pasta_mes, subpasta)
                    os.makedirs(caminho_subpasta, exist_ok=True)

                self.logging.info(f"Pastas de {self.mes}/{self.ano} criadas com sucesso em '{pasta_mes}'.")
            except Exception as e:
                self.logging.error(f"Erro ao criar estrutura de pastas em '{caminho_base}': {e}")

    def salvar_pdf(self, caminho_pdf_origem, cnpj, tipo, negativa):
        """
        Move o PDF para a pasta correta na estrutura:
        Certidões {ano}/{mes} {ano}/{tipo}/{CNPJ}/
        Dentro de: 'Certidões Negativas' ou 'Certidões Positivas'

        Parâmetros:
        - caminho_pdf_origem: caminho do arquivo PDF a ser movido
        - cnpj: CNPJ da empresa
        - tipo: tipo da certidão (ex: "FGTS", "ESTADUAL", etc.)
        - negativa: bool (True para salvar em 'Certidões Negativas', False para 'Positivas')
        """
        try:
            agora = datetime.now()
            ano = str(agora.year)
            mes = f"{agora.month:02d}"
            
            if negativa == "OK":
                caminho_base = os.getenv('PASTA_CERTIDOES_NEGATIVAS')
            else:
                caminho_base = os.getenv('PASTA_CERTIDOES_POSITIVAS')
            
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

            pasta_destino = os.path.join(
                caminho_base,
                f"Certidões {ano}",
                f"{mes} {ano}",
                tipo.upper(),
                cnpj_limpo
            )

            os.makedirs(pasta_destino, exist_ok=True)

            nome_arquivo = os.path.basename(caminho_pdf_origem)
            caminho_pdf_destino = os.path.join(pasta_destino, nome_arquivo)

            shutil.move(caminho_pdf_origem, caminho_pdf_destino)

            self.logging.info(f"PDF movido para: {caminho_pdf_destino}")
            return caminho_pdf_destino

        except Exception as e:
            self.logging.error(f"Erro ao mover o PDF '{caminho_pdf_origem}': {e}")
            raise
