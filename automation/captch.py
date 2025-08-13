from twocaptcha import TwoCaptcha
import logging
import base64
from openai import OpenAI

class Captch:
    def __init__(self):
        pass

    def quebrar_captch(self,captch_base64):
        """
    Envia um captcha em Base64 para a API da OpenAI e retorna o texto extraído.
    """
        # Decodifica o base64 para bytes
        image_data = base64.b64decode(captch_base64)

        client = OpenAI(api_key="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")

        prompt = f"""
        Decode o seguinte imagem de captcha de texto.
        Retorne apenas o texto que está escrito, sem espaços extras nem quebras de linha.
        Base64:
        {image_data}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            resposta = response.choices[0].message.content.strip()
            return resposta.strip()
        except Exception as e:
            logging.error(f"Erro na chamada da OpenAI: {e}")
            return f"❌ Erro na chamada da OpenAI: {e}"
    

    # def quebrar_captch(self, captch_base64):
    #     # Sua chave de API do 2Captcha
    #     API_KEY = '0c945c8d1447c7f214057200a3380181'

    #     # Inicializa o solver
    #     solver = TwoCaptcha(API_KEY)

    #     try:
    #         # Resolve um captcha de imagem
    #         result = solver.normal(captch_base64)
    #         print("Captcha resolvido:", result['code'])

    #     except Exception as e:
    #         print("Erro ao resolver captcha:", e)

    # def encontrar_base64_captch(self, captch):
    #     # Localiza o elemento da imagem do captcha
    #     captch = self.driver.find_element("xpath", "//img[@id='captchaImage']")

    #     # Pega o atributo src
    #     captch_src = captch.get_attribute("src")

    #     # Caso o src seja base64 direto
    #     if captch_src.startswith("data:image"):
    #         captcha_base64 = captch_src.split(",")[1]

    #     # Caso seja uma URL
    #     else:
    #         img_data = requests.get(captch_src).content
    #         captch_base64 = base64.b64encode(img_data).decode("utf-8")

    #     print(captch_base64)