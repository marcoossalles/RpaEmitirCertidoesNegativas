import fitz  # Biblioteca PyMuPDF para manipulação de PDFs
import re    # Expressões regulares (não usado diretamente, mas importado)
from manager_logs.logger_manager import Logger

class LerCertidoes:
    def __init__(self):
        self.logging = Logger("EmissaoCertidao")

    def leitura_certidao_estadual(self, caminho_pdf) -> bool:
        """
        Lê a certidão estadual e verifica se o trecho 'NAO CONSTA DEBITO' 
        aparece logo após o trecho do despacho.
        Retorna True se encontrado, False caso contrário.
        """
        self.logging.info(f"Iniciando leitura da certidão estadual: {caminho_pdf}")
        texto_total = ""

        try:
            # Abre o PDF e concatena o texto de todas as páginas
            with fitz.open(caminho_pdf) as pdf:
                for pagina in pdf:
                    texto_total += pagina.get_text()

            self.logging.debug("Texto extraído do PDF com sucesso.")

            trecho_chave = "DESPACHO (Certidao valida para a matriz e suas filiais):"
            if trecho_chave in texto_total:
                self.logging.info("Trecho-chave do despacho encontrado no PDF.")
                # Pega apenas o texto após o trecho-chave
                trecho_pos_despacho = texto_total.split(trecho_chave, 1)[1]
                # Verifica se 'NAO CONSTA DEBITO' aparece logo após
                resultado = "NAO CONSTA DEBITO" in trecho_pos_despacho.upper()
                self.logging.info(f"Resultado da verificação: {resultado}")
                if resultado:
                    return "OK"
                else:
                    return "PENDENTE"

            self.logging.warning("Trecho-chave do despacho não encontrado no PDF.")
            return "Trecho-chave do despacho não encontrado no PDF."

        except Exception as e:
            self.logging.error(f"Erro ao processar certidão estadual: {e}")
            return e

    def leitura_certidao_trabalhista(self, caminho_pdf) -> bool:
        """
        Lê a certidão trabalhista e verifica se o trecho 'NÃO CONSTA' 
        aparece após o trecho fixo da certidão.
        Retorna True se encontrado, False caso contrário.
        """
        self.logging.info(f"Iniciando leitura da certidão trabalhista: {caminho_pdf}")
        texto_total = ""

        try:
            # Abre o PDF e concatena o texto de todas as páginas
            with fitz.open(caminho_pdf) as pdf:
                for pagina in pdf:
                    texto_total += pagina.get_text()

            self.logging.debug("Texto extraído do PDF com sucesso.")

            trecho_chave = "CNPJ sob o nº"
            if trecho_chave in texto_total:
                self.logging.info("Trecho-chave do CNPJ encontrado no PDF.")
                trecho_pos_chave = texto_total.split(trecho_chave, 1)[1]
                resultado = "NÃO CONSTA" in trecho_pos_chave.upper()
                self.logging.info(f"Resultado da verificação: {resultado}")
                resultado
                if resultado:
                    return "OK"
                else:
                    return "PENDENTE"

            self.logging.warning("Trecho-chave do CNPJ não encontrado no PDF.")
            return "Trecho-chave do despacho não encontrado no PDF."

        except Exception as e:
            self.logging.error(f"Erro ao processar certidão trabalhista: {e}")
            return e
