import requests
import time
from twocaptcha import TwoCaptcha
import sys
import os
from manager_logs.logger_manager import Logger

class CaptchaSolver:
    def __init__(self, api_key=os.getenv('TOKEN_API_2CAPTCHA')):
        self.logging = Logger("EmissaoCertidao")
        self.api_key = api_key
        self.base_url = os.getenv('BASE_URL_2CAPTCHA')
        self.timeout = 60
        self.start_time = time.time()

    def solve_captcha(self, image_base64):
        """
        Cria uma task de ImageToText no 2Captcha e retorna somente o texto do captcha resolvido.
        """
        # Criar task
        create_url = f"{self.base_url}/createTask"
        payload = {
            "clientKey": self.api_key,
            "task": {
                "type": "ImageToTextTask",
                "body": image_base64,
                "phrase": False,
                "case": True,
                "numeric": 0,
                "math": False,
                "minLength": 1,
                "maxLength": 5,
                "comment": "enter the text you see on the image"
            },
            "languagePool": "en"
        }

        try:
            self.logging.info("Criando task para quebrar captcha")
            response = requests.post(create_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("errorId", 0) != 0:
                self.logging.error(f"Erro ao criar task: {data.get('errorDescription')}")
                raise Exception(f"Erro ao criar task: {data.get('errorDescription')}")

            task_id = data.get("taskId")

            # Consultar resultado até estar pronto
            self.logging.info("Aguardando quebra do Captcha")
            get_url = f"{self.base_url}/getTaskResult"
            
            while True:
                result = requests.post(
                    get_url,
                    json={"clientKey": self.api_key, "taskId": task_id},
                    timeout=30
                ).json()

                if result.get("status") == "ready":
                    return result["solution"]["text"]
                    #return "teste"

                # verifica se já passou do tempo limite
                if time.time() - self.start_time > self.timeout:
                    return "Erro: não ficou pronto dentro de 1 minuto"

                time.sleep(2)

        except Exception as e:
            self.logging.error(f"Erro: {e}")
            return None