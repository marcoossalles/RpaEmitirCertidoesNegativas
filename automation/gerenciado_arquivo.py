import os
import shutil
from datetime import datetime

class CriadorPastasCertidoes:
    def __init__(self):
        """
        Inicializa a classe pegando o mês e o ano atual automaticamente.
        """
        agora = datetime.now()
        self.ano = str(agora.year)
        self.mes = f"{agora.month:02d}"  # Garante dois dígitos tipo "07"
        self.caminho_base = r"C:\empresas"
        self.subpastas = ["ESTADUAL", "FEDERAL", "FGTS", "MUNICIPAL"]

    def criar_estrutura_pastas(self):
        """
        Cria a estrutura de pastas:
        Certidões {ano} → {mes} {ano} → [ESTADUAL, FEDERAL, FGTS, MUNICIPAL]
        """
        pasta_ano = os.path.join(self.caminho_base, f"Certidões {self.ano}")
        pasta_mes = os.path.join(pasta_ano, f"{self.mes} {self.ano}")

        try:
            os.makedirs(pasta_mes, exist_ok=True)

            for subpasta in self.subpastas:
                caminho_subpasta = os.path.join(pasta_mes, subpasta)
                os.makedirs(caminho_subpasta, exist_ok=True)

            print(f"Pastas de {self.mes}/{self.ano} criadas com sucesso!")
        except Exception as e:
            print(f"Erro ao criar pastas: {e}")

    def salvar_pdf(self, caminho_pdf_origem, cnpj, tipo):
        """
        Move o PDF já nomeado corretamente para a pasta correta na estrutura:
        Certidões {ano}/{mes} {ano}/{tipo}/{CNPJ}/
        """

        # Limpa o CNPJ (só números)
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

        # Caminho da subpasta destino final
        pasta_destino = os.path.join(
            self.caminho_base,
            f"Certidões {self.ano}",
            f"{self.mes} {self.ano}",
            tipo.upper(),
            cnpj_limpo
        )

        # Garante que a subpasta exista
        os.makedirs(pasta_destino, exist_ok=True)

        # Nome do arquivo já vem pronto
        nome_arquivo = os.path.basename(caminho_pdf_origem)
        caminho_pdf_destino = os.path.join(pasta_destino, nome_arquivo)

        # Move o arquivo
        shutil.move(caminho_pdf_origem, caminho_pdf_destino)

        return caminho_pdf_destino