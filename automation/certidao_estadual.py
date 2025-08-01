import os
import time
import logging
from automation.gerenciado_arquivo import CriadorPastasCertidoes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CertidaoEstadual:
    def __init__(self):
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")

        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing.disable_download_protection": True
        })

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    def acessar_site(self, cnpj, nome_empresa):
        tipo = 'ESTADUAL'
        try:
            url = "https://www.sefaz.go.gov.br/certidao/emissao/"
            self.driver.get(url)
            time.sleep(3)
            
            # Seleciona o tipo de documento como CNPJ
            self.driver.find_element(By.XPATH, '//*[@id="Certidao.TipoDocumentoCNPJ"]').click()

            time.sleep(2)
            # Preenche o campo de CNPJ
            input_cnpj = self.driver.find_element(By.XPATH, '//*[@id="Certidao.NumeroDocumentoCNPJ"]')
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)

            time.sleep(2)
            # Clica no botão "Emitir Certidão"
            self.driver.find_element(By.XPATH, '/html/body/form/div/div[2]/input[1]').click()

            # Aguarda o download completar
            time.sleep(5)

            # Renomeia arquivos .asp para .pdf
            for nome_arquivo in os.listdir(self.download_dir):
                if nome_arquivo.endswith('.asp'):
                    caminho_antigo = os.path.join(self.download_dir, nome_arquivo)
                    caminho_pdf = os.path.join(self.download_dir, nome_empresa)

                    os.rename(caminho_antigo, caminho_pdf)
                    logging.info(f"Renomeado: {nome_arquivo} -> {cnpj}.pdf")

                    # Chama o método para salvar na pasta final
                    destino_final = CriadorPastasCertidoes().salvar_pdf(caminho_pdf, cnpj, tipo)
                    logging.info(f"PDF movido para: {destino_final}")

            self.fechar()
            return True

        except Exception as e:
            logging.error(f"Erro ao emitir certidão estadual para o CNPJ {cnpj}: {e}")
            self.fechar()
            return False

    def fechar(self):
        self.driver.quit()
