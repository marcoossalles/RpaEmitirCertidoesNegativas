import logging
import os
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

from automation.gerenciado_arquivo import CriadorPastasCertidoes
from integrations.integracao_certidao_fgts import ApiCertidaoFgts
from automation.captch import CaptchaSolver
from automation.genrenciador_processamento import GerenciadorProcessamento

class CertidaoFgts:
    def __init__(self):
        """
        Inicializa o driver do Chrome com opções específicas,
        incluindo diretório de download e permissões de segurança.
        """
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        
        chrome_options = Options()
        if os.getenv("CONFIG_HEADLESS") == 'True':
                # chrome moderno
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--disable-gpu")

        chrome_options.add_argument("--start-maximized")

        chrome_options.add_argument(f"user-agent={user_agent}")
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

        logging.info("Driver Chrome iniciado com sucesso para emissão FGTS.")

    def acessar_site(self, cnpj, nome_empresa):
        """
        Acessa o site da Caixa, preenche o CNPJ e realiza o fluxo
        de emissão da certidão FGTS em PDF.
        """
        status_emissao_certidao = None
        tipo = 'FGTS'
        wait = WebDriverWait(self.driver, 20)
        try:
            url = os.getenv('BASE_URL_CERTIDAO_FGTS')
            self.driver.get(url)
            time.sleep(5)
            logging.info("Site FGTS acessado com sucesso.")

            wait = WebDriverWait(self.driver, 20)

            logging.info(f"Emitindo certidão FGTS para o CNPJ: {cnpj}")

            # Preenche o CNPJ
            input_cnpj = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainForm:txtInscricao1"]')))
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)

            # Captura o atributo src
            src = self.driver.find_element("xpath", '//*[@id="captchaImg_N2"]').get_attribute("src")
            
            # Remove o prefixo "data:image/png;base64,"
            base64_data = src.split(",")[1]
            
            #Resolver captcha
            captcha_string = CaptchaSolver().solve_captcha(base64_data)
            
            #Campo input captcha
            input_captcha = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainForm:txtCaptcha"]')))
            input_captcha.clear()
            input_captcha.send_keys(captcha_string)
            time.sleep(2)

            # Inicia o processo de emissão
            self.driver.find_element(By.XPATH, '//*[@id="mainForm:btnConsultar"]').click()
            time.sleep(2)
            
            try:
                mensagem = wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="mainForm"]/div[1]/div[1]/div/span'))
                )
                if mensagem.is_displayed():
                    logging.warning("Mensagem de erro encontrada, interrompendo emissão.")
                    return "PENDENTE"
            except TimeoutException:
                # A mensagem não apareceu → segue o processo
                pass

            self.driver.find_element(By.XPATH, '//*[@id="mainForm:j_id51"]').click()
            time.sleep(2)

            self.driver.find_element(By.XPATH, '//*[@id="mainForm:btnVisualizar"]').click()
            time.sleep(3)

            # Troca para a aba da certidão
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(2)
            logging.info("Aba da certidão carregada.")

            # Captura da tela em imagem
            caminho_png = os.path.join(self.download_dir, f"{cnpj}_certidao_fgts.png")
            self.driver.save_screenshot(caminho_png)
            logging.info(f"Screenshot salva em: {caminho_png}")

            # Converte imagem para PDF
            imagem = Image.open(caminho_png)
            caminho_pdf = os.path.join(self.download_dir, f"{cnpj}_certidao_fgts.pdf")
            imagem.convert("RGB").save(caminho_pdf)
            logging.info(f"Imagem convertida para PDF: {caminho_pdf}")

            os.remove(caminho_png)  # Remove a imagem original
            logging.info("Imagem PNG removida após conversão.")

            # Renomeia e move o arquivo PDF final
            for nome_arquivo in os.listdir(self.download_dir):
                if nome_arquivo.endswith('.pdf'):
                    status_emissao_certidao = "OK"
                    caminho_antigo = os.path.join(self.download_dir, nome_arquivo)
                    caminho_pdf = os.path.join(self.download_dir, f"{nome_empresa}.pdf")
                    os.rename(caminho_antigo, caminho_pdf)
                    logging.info(f"PDF renomeado: {nome_arquivo} -> {cnpj}.pdf")

                    destino_final = CriadorPastasCertidoes().salvar_pdf(caminho_pdf, cnpj, tipo, status_emissao_certidao)
                    logging.info(f"PDF movido para: {destino_final}")

            self.fechar()
            logging.info(f"Processo concluído para o CNPJ: {cnpj}")
            return "OK"

        except Exception as e:
            logging.error(f"Erro ao emitir certidão estadual via Web para o CNPJ {cnpj}: {e}")
            GerenciadorProcessamento().print_momento_erro(nome_empresa, tipo, self.driver)            
            self.fechar()
            logging.info(f"Vamos utilizar API para emitir a certidão")
            status_emissao_certidao = ApiCertidaoFgts().emitir_certidao_fgts(cnpj, nome_empresa)
            return status_emissao_certidao

    def fechar(self):
        """
        Fecha o navegador.
        """
        self.driver.quit()
        logging.info("Driver encerrado.")
