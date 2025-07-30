import os
import shutil
from datetime import datetime

class GerenciadorDeArquivos:
    def __init__(self, pasta_base=os.getenv('PASTA_CERTIDOES')):
        self.pasta_base = pasta_base

    def salvar_pdf(self, caminho_pdf_origem, cnpj, tipo):
        """Move o PDF para a pasta correta com nome formatado por CNPJ e hora"""

        # Limpa o CNPJ (só números)
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

        # Data e hora atual
        agora = datetime.now()
        ano = agora.strftime("%Y")
        data_dia = agora.strftime("%d-%m-%Y")
        hora_str = agora.strftime("%H-%M-%S")

        # Estrutura de pastas
        pasta_destino = os.path.join(self.pasta_base, cnpj_limpo, ano, data_dia)
        os.makedirs(pasta_destino, exist_ok=True)

        # Nome do arquivo: <cnpj>_<hora>.pdf
        nome_arquivo = f"{cnpj_limpo}_{tipo}_{hora_str}.pdf"
        caminho_pdf_destino = os.path.join(pasta_destino, nome_arquivo)

        # Move o arquivo
        shutil.move(caminho_pdf_origem, caminho_pdf_destino)
        return caminho_pdf_destino
