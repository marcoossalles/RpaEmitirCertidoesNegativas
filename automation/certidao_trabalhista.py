import logging
import os
from automation.gerenciado_arquivo import GerenciadorDeArquivos
from automation.captch import CaptchaCapture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class CertidaoTrabalhista:
    def __init__(self):
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless")  # Ative se quiser rodar sem abrir o navegador

        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir
        })

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    def acessar_site(self, cnpj):
        try:
            url = os.getenv('BASE_URL_CERTIDAO_TRABALHISTA')
            tipo = 'TRABALHISTA'
            self.driver.get(url)

            botao_emitir = self.driver.find_element(By.XPATH, '//*[@id="corpo"]/div/div[2]/input[1]')
            botao_emitir.click()

            input_cnpj = self.driver.find_element(By.XPATH, '//*[@id="gerarCertidaoForm:cpfCnpj"]')
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)
            
            logging.info(f"pausa")

            button_emitir_certidao = self.driver.find_element(By.XPATH,'//*[@id="gerarCertidaoForm:btnEmitirCertidao"]')
            button_emitir_certidao.click()

            # Renomeia arquivos .asp para .pdf
            for nome_arquivo in os.listdir(self.download_dir):
                if nome_arquivo.endswith('.pdf'):
                    caminho_antigo = os.path.join(self.download_dir, nome_arquivo)
                    caminho_pdf = os.path.join(self.download_dir, f"{cnpj}.pdf")

                    os.rename(caminho_antigo, caminho_pdf)
                    logging.info(f"Renomeado: {nome_arquivo} -> {cnpj}.pdf")

                    # Chama o método para salvar na pasta final
                    destino_final = GerenciadorDeArquivos().salvar_pdf(caminho_pdf, cnpj, tipo)
                    logging.info(f"PDF movido para: {destino_final}")
            
            self.fechar()
            return True 
        except Exception as e:
            logging.error(f"Erro ao emitir certidão trabalhista para o seguinte CNPJ:{cnpj}: {e}")
            self.fechar()
            return False
    def fechar(self):
        self.driver.quit()
