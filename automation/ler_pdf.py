import fitz
import re
import logging

class LerCertidoes:
    def __init__(self):
            pass

    def leitura_certidao_estadual(self, caminho_pdf) -> bool:
        """
        Verifica se o trecho 'NAO CONSTA DEBITO' aparece logo após o trecho do despacho.
        Retorna True se sim, False caso contrário.
        """
        texto_total = ""
        with fitz.open(caminho_pdf) as pdf:
            for pagina in pdf:
                texto_total += pagina.get_text()
        
        trecho_chave = "DESPACHO (Certidao valida para a matriz e suas filiais):"
        if trecho_chave in texto_total:
            # Pega só o trecho depois do DESPACHO
            trecho_pos_despacho = texto_total.split(trecho_chave, 1)[1]
            # Verifica se 'NAO CONSTA DEBITO' aparece logo em seguida
            return "NAO CONSTA DEBITO" in trecho_pos_despacho.upper()
        return False
    
    def leitura_certidao_trabalhista(self, caminho_pdf) -> bool:
        """
        Verifica se o trecho 'NÃO CONSTA' aparece após a parte fixa da certidão.
        Retorna True se sim, False caso contrário.
        """
        texto_total = ""
        with fitz.open(caminho_pdf) as pdf:
            for pagina in pdf:
                texto_total += pagina.get_text()
        
        trecho_chave = "CNPJ sob o nº"
        if trecho_chave in texto_total:
            trecho_pos_chave = texto_total.split(trecho_chave, 1)[1]
            return "NÃO CONSTA" in trecho_pos_chave.upper()
        return False

