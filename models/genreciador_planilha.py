import pandas as pd
from datetime import datetime
import os
from manager_logs.logger_manager import Logger

class CriarAbaPlanilha:
    def __init__(self):
        self.logging = Logger("EmissaoCertidao")
        self.caminho_arquivo = os.getenv('PASTA_PLANILHA_CNPJS')
        self.writer = pd.ExcelWriter(
            self.caminho_arquivo, 
            engine='openpyxl', 
            mode='a', 
            if_sheet_exists='overlay'
        )
        self.workbook = self.writer.book

    def criar_aba_mensal(self):
        self.logging.info("Criando aba mensal na planilha, se necessário.")
        # pega mês e ano atuais em PT-BR
        meses = {
            1: "Janeiro", 2: "Fevereiro", 3: "Março",
            4: "Abril", 5: "Maio", 6: "Junho",
            7: "Julho", 8: "Agosto", 9: "Setembro",
            10: "Outubro", 11: "Novembro", 12: "Dezembro"
        }
        agora = datetime.now()
        nome_aba = f"{meses[agora.month]} {agora.year}"

        if nome_aba in self.workbook.sheetnames:
            self.logging.info(f"Aba '{nome_aba}' já existe. Nenhuma ação tomada.")
            return

        df = pd.DataFrame()  # DataFrame vazio só pra criar a aba
        df.to_excel(self.writer, sheet_name=nome_aba, index=False)
        self.writer.close()
        self.logging.info(f"Aba '{nome_aba}' criada com sucesso.")
