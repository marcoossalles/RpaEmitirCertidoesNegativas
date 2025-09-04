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
        self.pasta_log = os.path.join(self.pasta_principal, "logs")
        self.pasta_copia_planilha = os.path.join(self.pasta_principal, "Copia Planilha")

        # Arquivo de log
        self.arquivo_log = os.path.join(self.pasta_log, "log.txt")

        # Caminho da planilha original
        self.planilha_origem = os.getenv("PASTA_PLANILHA_CNPJS")

        # Criar toda a estrutura
        self._criar_estrutura()

        # Copiar a planilha para a pasta Copia Planilha
        self._copiar_planilha()

    def _criar_estrutura(self):
        os.makedirs(self.pasta_print_erro, exist_ok=True)
        os.makedirs(self.pasta_log, exist_ok=True)  # criar a pasta, não o arquivo
        os.makedirs(self.pasta_copia_planilha, exist_ok=True)

        # Criar o arquivo de log se não existir
        if not os.path.exists(self.arquivo_log):
            with open(self.arquivo_log, 'w', encoding='utf-8') as f:
                f.write(f"Log iniciado em {datetime.now()}\n")

    def _copiar_planilha(self):
        if self.planilha_origem and os.path.exists(self.planilha_origem):
            destino = os.path.join(self.pasta_copia_planilha, os.path.basename(self.planilha_origem))
            shutil.copy2(self.planilha_origem, destino)

    def print_momento_erro(self, nome_empresa, tipo, driver):
        """Salva um print de tela no momento do erro"""
        filename = f"{tipo}_{nome_empresa}_{datetime.now().strftime('%Y%m%d')}.png"
        file_path = os.path.join(self.pasta_print_erro, filename)
        screenshot = driver.save_screenshot(file_path)
        screenshot.save(file_path)
        return file_path
