import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class CertidaoFgts:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless")  # Ative se quiser rodar sem abrir o navegador

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    def acessar_site(self, cnpj):
        try:
            url = os.getenv('BASE_URL_CERTIDAO_FGTS')
            self.driver.get(url)
            
            input_cnpj = self.driver.find_element(By.XPATH, '//*[@id="mainForm:txtInscricao1"]')
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)

            button_consultar = self.driver.find_element(By.XPATH, '//*[@id="mainForm:btnConsultar"]')
            button_consultar.click()

            button_obtenha_certificado = self.driver.find_element(By.XPATH, '//*[@id="mainForm:j_id51"]')
            button_obtenha_certificado.click()

            button_vizualizar = self.driver.find_element(By.XPATH, '//*[@id="mainForm:btnVisualizar"]')
            button_vizualizar.click()

            button_imprimir = self.driver.find_element(By.XPATH, '//*[@id="mainForm:btImprimir4"]')
            button_imprimir.click()

            button_save = self.driver.find_element(By.XPATH, '//*[@id="sidebar"]//print-preview-button-strip//cr-button[1]//*[@id="sidebar"]//print-preview-button-strip//cr-button[1]"]')
            button_save.click()

            logging.info(f"Certidão FGTS emitida com sucesso para o CNPJ: {cnpj}")

            self.fechar()
            return True 
        except Exception as e:
            logging.error(f"Erro ao emitir certidão trabalhista para o seguinte CNPJ:{cnpj}: {e}")
            self.fechar()
            return False
    def fechar(self):
        self.driver.quit()