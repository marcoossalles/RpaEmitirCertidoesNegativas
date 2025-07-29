import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class CertidaoTrabalhista:
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
            url = os.getenv('BASE_URL_CERTIDAO_TRABALHISTA')
            self.driver.get(url)

            botao_emitir = self.driver.find_element(By.XPATH, '//*[@id="corpo"]/div/div[2]/input[1]')
            botao_emitir.click()

            input_cnpj = self.driver.find_element(By.XPATH, '//*[@id="gerarCertidaoForm:cpfCnpj"]')
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)
            
            button_emitir_certidao = self.driver.find_element(By.XPATH,'//*[@id="gerarCertidaoForm:btnEmitirCertidao"]')
            button_emitir_certidao.click()
            
            self.fechar()
            return True 
        except Exception as e:
            logging.error(f"Erro ao emitir certidão trabalhista para o seguinte CNPJ:{cnpj}: {e}")
            self.fechar()
            return False
    def fechar(self):
        self.driver.quit()
