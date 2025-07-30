from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

class PlanilhaMensalDuplicador:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo
        self.wb = load_workbook(caminho_arquivo)

    def duplicar_aba_mensal(self, aba_origem, aba_destino, colunas_para_manter=("EMPRESAS", "CNPJ"), linha_titulo=7, linha_dados=8):
        if aba_origem not in self.wb.sheetnames:
            raise ValueError(f"Aba '{aba_origem}' não encontrada no arquivo.")
        
        aba_original = self.wb[aba_origem]
        nova_aba = self.wb.copy_worksheet(aba_original)
        nova_aba.title = aba_destino

        # Descobre os índices das colunas que devem ser mantidas
        colunas_mantidas = []
        for col in nova_aba.iter_cols(min_row=linha_titulo, max_row=linha_titulo):
            valor = str(col[0].value).strip().upper()
            if valor in [c.upper() for c in colunas_para_manter]:
                colunas_mantidas.append(col[0].column)

        # Limpa os dados das colunas que não devem ser mantidas
        for row in nova_aba.iter_rows(min_row=linha_dados):
            for cell in row:
                if cell.column not in colunas_mantidas:
                    cell.value = None

        self.wb.save(self.caminho_arquivo)
        print(f"Aba '{aba_destino}' criada com sucesso baseada na aba '{aba_origem}'.")
