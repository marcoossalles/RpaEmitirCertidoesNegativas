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
        # Define e cria a pasta de downloads se não existir
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        # Configurações do Chrome
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

        # Inicializa o driver do Chrome
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    def acessar_site(self, cnpj, nome_empresa):
        tipo = 'ESTADUAL'
        try:
            logging.info(f"Iniciando emissão da certidão estadual para o CNPJ: {cnpj}")
            url = os.getenv('BASE_URL_CERTIDAO_ESTADUAL')
            self.driver.get(url)
            time.sleep(3)

            # Seleciona a opção de documento como CNPJ
            self.driver.find_element(By.XPATH, '//*[@id="Certidao.TipoDocumentoCNPJ"]').click()
            logging.info("Selecionado tipo de documento: CNPJ")

            time.sleep(2)

            # Preenche o campo com o CNPJ
            input_cnpj = self.driver.find_element(By.XPATH, '//*[@id="Certidao.NumeroDocumentoCNPJ"]')
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)
            logging.info(f"CNPJ preenchido: {cnpj}")

            time.sleep(2)

            # Clica no botão de emissão
            self.driver.find_element(By.XPATH, '/html/body/form/div/div[2]/input[1]').click()
            logging.info("Botão de emissão da certidão clicado")

            # Aguarda o download ser concluído
            time.sleep(5)

            # Renomeia e move o arquivo baixado
            for nome_arquivo in os.listdir(self.download_dir):
                if nome_arquivo.endswith('.asp'):
                    caminho_antigo = os.path.join(self.download_dir, nome_arquivo)
                    caminho_pdf = os.path.join(self.download_dir, f"{nome_empresa}.pdf")

                    os.rename(caminho_antigo, caminho_pdf)
                    logging.info(f"Arquivo renomeado: {nome_arquivo} -> {nome_empresa}")

                    # Salva o PDF na pasta final organizada
                    destino_final = CriadorPastasCertidoes().salvar_pdf(caminho_pdf, cnpj, tipo)
                    logging.info(f"Certidão estadual salva em: {destino_final}")

            self.fechar()
            return True

        except Exception as e:
            logging.error(f"Erro ao emitir certidão estadual para o CNPJ {cnpj}: {e}")
            self.fechar()
            return False

    def fechar(self):
        # Encerra o navegador
        logging.info("Encerrando o navegador")
        self.driver.quit()
