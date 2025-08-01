import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Configura o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CertidaoMunicipal:
    def __init__(self):
        """
        Inicializa o driver do Chrome com as configurações desejadas.
        """
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless")  # Ative se quiser rodar sem abrir o navegador

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        logging.info("Driver do Chrome iniciado com sucesso para certidão municipal.")

    def acessar_site(self, cnpj):
        """
        Acessa o site da certidão municipal, emite a certidão e faz o download.
        """
        try:
            url = os.getenv('BASE_URL_CERTIDAO_MUNICIPAL')
            self.driver.get(url)
            logging.info(f"Acessando o site da certidão municipal: {url}")

            # Clica no botão para selecionar o tipo de documento como CNPJ
            botao_cnpj = self.driver.find_element(By.XPATH, '//*[@id="Certidao.TipoDocumentoCNPJ"]')
            botao_cnpj.click()
            logging.info("Selecionado o tipo de documento: CNPJ")

            # Insere o CNPJ no campo de entrada
            input_cnpj = self.driver.find_element(By.XPATH, '//*[@id="Certidao.NumeroDocumentoCNPJ"]')
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)
            logging.info(f"CNPJ inserido: {cnpj}")

            # Clica no botão para emitir a certidão
            button_emitir_certidao = self.driver.find_element(By.XPATH,'/html/body/form/div/div[2]/input[1]')
            button_emitir_certidao.click()
            logging.info("Botão de emissão da certidão clicado.")

            # Clica no botão para salvar/download da certidão
            button_salve = self.driver.find_element(By.XPATH,'//*[@id="icon"]')
            button_salve.click()
            logging.info("Botão de salvar certidão clicado.")

            self.fechar()
            return True 
        except Exception as e:
            logging.error(f"Erro ao emitir certidão municipal para o CNPJ {cnpj}: {e}")
            self.fechar()
            return False

    def fechar(self):
        """
        Encerra a sessão do navegador.
        """
        self.driver.quit()
        logging.info("Driver do Chrome encerrado.")
