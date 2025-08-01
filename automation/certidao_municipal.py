import logging
import os
import time
from automation.gerenciado_arquivo import CriadorPastasCertidoes
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class CertidaoMunicipal:
    def __init__(self):
        """
        Inicializa o driver do Chrome com opções específicas,
        incluindo diretório de download e permissões de segurança.
        """
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(self.download_dir, exist_ok=True)

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir
        })

        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

        logging.info("Driver Chrome iniciado com sucesso para emissão FGTS.")

    def acessar_site(self, cnpj, nome_empresa):
        """
        Acessa o site, preenche o CNPJ e realiza o fluxo
        de emissão da certidão PDF.
        """
        tipo = 'MUNICIPAL'
        try:
            url = os.getenv('BASE_URL_MUNICIPAL')
            self.driver.get(url)
            logging.info("Site prefeitrua de X.")

            wait = WebDriverWait(self.driver, 20)

            # Preenche o CNPJ
            input_cnpj = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/font/form/table[1]/tbody/tr[1]/td[2]/input')))
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)
            logging.info(f"Emitindo certidão FGTS para o CNPJ: {cnpj}")

            # Inicia o processo de emissão
            self.driver.find_element(By.XPATH, '/html/body/font/form/table[1]/tbody/tr[3]/td/input').click()
            time.sleep(2)

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
                    caminho_antigo = os.path.join(self.download_dir, nome_arquivo)
                    caminho_pdf = os.path.join(self.download_dir, f"{nome_empresa}.pdf")
                    os.rename(caminho_antigo, caminho_pdf)
                    logging.info(f"PDF renomeado: {nome_arquivo} -> {cnpj}.pdf")

                    destino_final = CriadorPastasCertidoes().salvar_pdf(caminho_pdf, cnpj, tipo)
                    logging.info(f"PDF movido para: {destino_final}")

            self.fechar()
            logging.info(f"Processo concluído para o CNPJ: {cnpj}")
            return True

        except Exception as e:
            logging.error(f"Erro ao emitir certidão FGTS para o CNPJ {cnpj}: {e}")
            self.fechar()
            return False

    def fechar(self):
        """
        Fecha o navegador.
        """
        self.driver.quit()
        logging.info("Driver encerrado.")