import os
import shutil
from datetime import datetime
import logging

class GerenciadorProcessamento:
    def __init__(self, base_path="."):
        logging.info("Iiciacando criação da estrutura de gerenciamento de processamento.")
        # Pasta base fixa
        self.task_root = os.path.join(base_path, "Task")

        # Nome dinâmico para a subpasta Task com data
        nome_pasta = "Task_" + datetime.now().strftime("%Y%m%d")
        self.pasta_principal = os.path.join(self.task_root, nome_pasta)

        # Subpastas
        self.pasta_print_erro = os.path.join(self.pasta_principal, "Print Erro")
        self.pasta_log = os.path.join(self.pasta_principal, "logs")

        # Arquivo de log
        self.arquivo_log = os.path.join(self.pasta_log, "log.txt")

        # Criar toda a estrutura
        self._criar_estrutura()

    def _criar_estrutura(self):
        os.makedirs(self.pasta_print_erro, exist_ok=True)
        os.makedirs(self.pasta_log, exist_ok=True)  # criar a pasta, não o arquivo

        # Criar o arquivo de log se não existir
        if not os.path.exists(self.arquivo_log):
            with open(self.arquivo_log, 'w', encoding='utf-8') as f:
                f.write(f"Log iniciado em {datetime.now()}\n")

    def print_momento_erro(self, nome_empresa, tipo, driver):
        """Salva um print de tela no momento do erro"""
        filename = f"{tipo}_{nome_empresa}_{datetime.now().strftime('%Y%m%d')}.png"
        file_path = os.path.join(self.pasta_print_erro, filename)
        driver.save_screenshot(file_path)

