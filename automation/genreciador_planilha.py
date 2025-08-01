from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from datetime import datetime, timedelta
import calendar
import locale

# Define locale para português (ajusta os nomes dos meses)
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Linux/macOS
except:
    locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')  # Windows

class PlanilhaMensalDuplicador:
    def __init__(self, caminho_arquivo='C:\\empresas\\PLANILHA CONTROLE\\Controle de Certidões - 2025.xlsx'):
        self.caminho_arquivo = caminho_arquivo
        self.wb = load_workbook(caminho_arquivo)

    def duplicar_aba_mensal(self, 
                            colunas_para_limpar=("EMPRESAS", "CNPJ", "Simples Nacional", "Grupo", "Status", 
                                                "Inscrição", "Certidão", "FGTS", "TRABALHISTA", "Status Procesamento"),
                            linha_titulo=8, 
                            linha_dados=9):
        # Define o locale para português (Brasil)
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        hoje = datetime.today()

        # Mês atual e próximo com nome por extenso
        mes_atual_nome = hoje.strftime('%B').capitalize()  # Ex: "Julho"
        ano_atual = hoje.year
        aba_origem = f"{mes_atual_nome} {ano_atual}"

        proximo_mes = hoje.replace(day=28) + timedelta(days=4)
        proximo_mes = proximo_mes.replace(day=1)
        mes_proximo_nome = proximo_mes.strftime('%B').capitalize()
        ano_proximo = proximo_mes.year
        aba_destino = f"{mes_proximo_nome} {ano_proximo}"

        if aba_destino in self.wb.sheetnames:
            print(f"Aba '{aba_destino}' já existe. Nenhuma ação foi realizada.")
            return

        if aba_origem not in self.wb.sheetnames:
            raise ValueError(f"Aba de origem '{aba_origem}' não encontrada.")

        aba_original = self.wb[aba_origem]
        nova_aba = self.wb.copy_worksheet(aba_original)
        nova_aba.title = aba_destino

        # Padroniza colunas a limpar
        colunas_para_limpar = [col.strip().upper() for col in colunas_para_limpar]

        # Identifica índices das colunas a limpar
        titulos = [str(cell.value).strip().upper() for cell in aba_original[linha_titulo]]
        indices_para_limpar = [i + 1 for i, titulo in enumerate(titulos) if titulo in colunas_para_limpar]

        # Limpa os dados das colunas específicas
        for row in nova_aba.iter_rows(min_row=linha_dados, max_row=nova_aba.max_row):
            for cell in row:
                if cell.column in indices_para_limpar:
                    cell.value = None

        self.wb.save(self.caminho_arquivo)
        print(f"Aba '{aba_destino}' criada com sucesso com base na aba '{aba_origem}'.")

    def ler_aba_mes_atual(self, linha_titulo=8, linha_dados=9):
        hoje = datetime.today()
        mes_nome = hoje.strftime('%B').capitalize()
        ano = hoje.year
        nome_aba = f"{mes_nome} {ano}"

        if nome_aba not in self.wb.sheetnames:
            raise ValueError(f"Aba '{nome_aba}' não encontrada na planilha.")

        aba = self.wb[nome_aba]

        # Lê os nomes das colunas
        colunas = [cell.value for cell in aba[linha_titulo]]

        # Lê os dados
        dados = []
        for row in aba.iter_rows(min_row=linha_dados, max_row=aba.max_row, values_only=True):
            if any(row):  # ignora linhas vazias
                linha_dict = {colunas[i]: row[i] for i in range(len(colunas)) if i < len(row)}
                dados.append(linha_dict)

        return dados
    
    def escrever_status_linha(self, nome_aba, linha, dicionario_status, linha_titulo=8):
        if nome_aba not in self.wb.sheetnames:
            raise ValueError(f"Aba '{nome_aba}' não encontrada no arquivo.")
        aba = self.wb[nome_aba]

        # Mapeia os nomes das colunas para seus índices
        mapa_colunas = {}
        for cell in aba[linha_titulo]:
            if cell.value:
                nome_coluna = str(cell.value).strip()
                mapa_colunas[nome_coluna.lower()] = cell.column

        # Escreve os status diretamente conforme o dicionário passado
        for nome_coluna, valor in dicionario_status.items():
            col = mapa_colunas.get(nome_coluna.lower())
            if col is None:
                raise ValueError(f"Coluna '{nome_coluna}' não encontrada na aba '{nome_aba}'.")
            aba.cell(row=linha, column=col, value=valor)

        self.wb.save(self.caminho_arquivo)