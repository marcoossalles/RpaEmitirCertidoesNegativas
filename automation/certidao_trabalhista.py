import logging
import fitz
import re
import os
from automation.gerenciado_arquivo import CriadorPastasCertidoes
from automation.captch import CaptchaCapture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        try:
            url = os.getenv('BASE_URL_CERTIDAO_TRABALHISTA')
            self.driver.get(url)
            logging.info(f"Acessado o site: {url}")

            # Localiza e clica no botão para emitir a certidão
            botao_emitir = self.driver.find_element(By.XPATH, '//*[@id="corpo"]/div/div[2]/input[1]')
            botao_emitir.click()
            logging.info("Botão 'Emitir' clicado com sucesso.")

            # Preenche o campo de CNPJ
            input_cnpj = self.driver.find_element(By.XPATH, '//*[@id="gerarCertidaoForm:cpfCnpj"]')
            input_cnpj.clear()
            input_cnpj.send_keys(cnpj)
            logging.info(f"CNPJ informado no campo: {cnpj}")

            # Clica para gerar a certidão
            button_emitir_certidao = self.driver.find_element(By.XPATH, '//*[@id="gerarCertidaoForm:btnEmitirCertidao"]')
            button_emitir_certidao.click()
            logging.info("Requisição para emissão da certidão enviada.")

            # Verifica se um arquivo PDF foi baixado
            for nome_arquivo in os.listdir(self.download_dir):
                if nome_arquivo.endswith('.pdf'):
                    caminho_antigo = os.path.join(self.download_dir, nome_arquivo)
                    caminho_pdf = os.path.join(self.download_dir, f"{nome_empresa}.pdf")

                    # Renomeia o PDF com o nome da empresa
                    os.rename(caminho_antigo, caminho_pdf)
                    logging.info(f"Arquivo renomeado: {nome_arquivo} -> {nome_empresa}")

                    self.ler_certidao_trabalhista(caminho_pdf, cnpj, tipo)

            self.fechar()
            return True

        except Exception as e:
            logging.error(f"Erro ao emitir certidão para CNPJ {cnpj}: {e}")
            self.fechar()
            return False


    def ler_certidao_trabalhista(self, caminho_pdf, cnpj, tipo):
        """
        Lê o conteúdo de uma certidão trabalhista em PDF e verifica o tipo de certidão com base no título.
        Parâmetros:
            caminho_pdf (str): Caminho para o arquivo PDF da certidão.
        """
        negativa = None
        try:
            with fitz.open(caminho_pdf) as pdf:
                texto = ""
                for pagina in pdf:
                    texto += pagina.get_text()

            # Expressão para capturar a primeira linha da certidão com o título
            padrao = r'^(CERTIDÃO .*?TRABALHISTAS)$'
            resultado = re.search(padrao, texto, re.IGNORECASE | re.MULTILINE)

            if resultado:
                titulo = resultado.group(1).strip().upper()

                if "NEGATIVA" in titulo:
                    destino_final = CriadorPastasCertidoes().salvar_pdf(caminho_pdf, cnpj, tipo, negativa=True)
                    logging.info(f"PDF movido com sucesso para: {destino_final}")
                else:
                    destino_final = CriadorPastasCertidoes().salvar_pdf(caminho_pdf, cnpj, tipo, negativa=False)
                    logging.info(f"PDF movido com sucesso para: {destino_final}")
            else:
                print("Título da certidão não encontrado")

        except Exception as e:
            print(f"Erro ao ler o PDF: {e}")

    def fechar(self):
        """
        Encerra a sessão do navegador e libera os recursos.
        """
        self.driver.quit()
        logging.info("Sessão do navegador encerrada.")