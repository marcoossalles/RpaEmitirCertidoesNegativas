import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from automation.gerenciado_arquivo import CriadorPastasCertidoes
from automation.ler_pdf import LerCertidoes
from integrations.integracao_certidao_trabalhista import ApiCertidaoTrabalhista
from automation.captch import CaptchaSolver

class CertidaoTrabalhista:
    def __init__(self):
        """
        Inicializa o navegador Chrome com configurações específicas,
        incluindo o diretório onde os arquivos PDF serão baixados.
        """
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)
        logging.info(f"Diretório de downloads configurado em: {self.download_dir}")

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument("--headless")  # Descomente se quiser executar em segundo plano

        # Define o diretório padrão de downloads no navegador
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir
        })

        # Inicializa o driver com as opções definidas
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        logging.info("Driver do Chrome iniciado com sucesso.")

    def acessar_site(self, cnpj, nome_empresa):
        """
        Acessa o site da certidão trabalhista, emite o documento e move o PDF baixado
        para a estrutura de pastas correta com nome personalizado.
        """
        tipo = 'TRABALHISTA'
        status_emissao_certidao = []
        try:
            url = os.getenv('BASE_URL_CERTIDAO_TRABALHISTA')
            self.driver.get(url)
            logging.info(f"Acessado o site: {url}")
            time.sleep(5)

            # Localiza e clica no botão para emitir a certidão
            botao_emitir = self.driver.find_element(By.XPATH, '//*[@id="corpo"]/div/div[2]/input[1]')
            botao_emitir.click()
            logging.info("Botão 'Emitir' clicado com sucesso.")
            time.sleep(5)

            # Preenche o campo de CNPJ
            input_cnpj = self.driver.find_element(By.XPATH, '//*[@id="gerarCertidaoForm:cpfCnpj"]')
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)
            logging.info(f"CNPJ informado no campo: {cnpj}")
            
            # Captura o atributo src
            src = self.driver.find_element("xpath", '//*[@id="idImgBase64"]').get_attribute("src")
            
            # Remove o prefixo "data:image/png;base64,"
            base64_data = src.split(",")[1]
            
            #Resolver captcha
            captcha_string = CaptchaSolver().solve_captcha(base64_data)
            
            #Campo input captcha
            input_captcha = self.driver.find_element(By.XPATH, '//*[@id="idCampoResposta"]')
            input_captcha.clear()
            input_captcha.send_keys(captcha_string)

            # Clica para gerar a certidão
            button_emitir_certidao = self.driver.find_element(By.XPATH, '//*[@id="gerarCertidaoForm:btnEmitirCertidao"]')
            button_emitir_certidao.click()
            time.sleep(3)
            logging.info("Requisição para emissão da certidão enviada.")

            # Verifica se um arquivo PDF foi baixado
            for nome_arquivo in os.listdir(self.download_dir):
                if nome_arquivo.endswith('.pdf'):
                    caminho_antigo = os.path.join(self.download_dir, nome_arquivo)
                    caminho_pdf = os.path.join(self.download_dir, f"{nome_empresa}.pdf")

                    # Renomeia o PDF com o nome da empresa
                    os.rename(caminho_antigo, caminho_pdf)
                    logging.info(f"Arquivo renomeado: {nome_arquivo} -> {nome_empresa}")
                    
                    status_emissao_certidao = LerCertidoes().leitura_certidao_trabalhista(caminho_pdf)
                    
                    destino_final = CriadorPastasCertidoes().salvar_pdf(caminho_pdf, cnpj, tipo, status_emissao_certidao)
                    logging.info(f"Certidão estadual salva em: {destino_final}")

            self.fechar()
            return status_emissao_certidao

        except Exception as e:
            logging.error(f"Erro ao emitir certidão estadual via Web para o CNPJ {cnpj}: {e}")
            logging.info(f"Vamos utilizar API para emitir a certidão")
            status_emissao_certidao = ApiCertidaoTrabalhista.emitir_certidao_trabalhista(cnpj, nome_empresa)
            self.fechar()
            return status_emissao_certidao
        
    def fechar(self):
        """
        Fecha o navegador.
        """
        self.driver.quit()
        logging.info("Driver encerrado.")
