import os
import shutil
from datetime import datetime
import pyautogui

class GerenciadorProcessamento:
    def __init__(self, base_path="."):
        # Pasta base fixa
        self.task_root = os.path.join(base_path, "Task")

        # Nome dinâmico para a subpasta Task com data
        nome_pasta = "Task_" + datetime.now().strftime("%Y%m%d")
        self.pasta_principal = os.path.join(self.task_root, nome_pasta)

        # Subpastas
        self.pasta_print_erro = os.path.join(self.pasta_principal, "Print Erro")
        self.pasta_log = os.path.join(self.pasta_principal, "Logs")
        self.pasta_copia_planilha = os.path.join(self.pasta_principal, "Copia Planilha")

        # Arquivo de log
        self.arquivo_log = os.path.join(self.pasta_log, "log.txt")

        # Caminho da planilha original
        self.planilha_origem = r"C:\empresas\PLANILHA CONTROLE\Controle de Certidões - 2025.xlsx"

        # Criar toda a estrutura
        self._criar_estrutura()

        # Copiar a planilha para a pasta Copia Planilha
        self._copiar_planilha()

    def _criar_estrutura(self):
        os.makedirs(self.pasta_print_erro, exist_ok=True)
        os.makedirs(self.pasta_log, exist_ok=True)
        os.makedirs(self.pasta_copia_planilha, exist_ok=True)

    def _copiar_planilha(self):
        if os.path.exists(self.planilha_origem):
            destino = os.path.join(self.pasta_copia_planilha, os.path.basename(self.planilha_origem))
            shutil.copy2(self.planilha_origem, destino)
        else:
            print(f"Arquivo de planilha não encontrado: {self.planilha_origem}")

    def print_momento_erro(self, nome_empresa, tipo):
        """Salva um print de tela no momento do erro"""
        filename = f"{tipo}_{nome_empresa}_{datetime.now().strftime('%Y%m%d')}.png"
        file_path = os.path.join(self.pasta_print_erro, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        return file_path
