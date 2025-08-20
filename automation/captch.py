import requests
import logging
import time
from twocaptcha import TwoCaptcha
import sys
import os

class CaptchaSolver:
    def __init__(self, api_key='0c945c8d1447c7f214057200a3380181'):
        self.api_key = api_key
        self.base_url = "https://api.2captcha.com"

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
            response = requests.post(create_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("errorId", 0) != 0:
                raise Exception(f"Erro ao criar task: {data.get('errorDescription')}")

            task_id = data.get("taskId")

            # Consultar resultado até estar pronto
            get_url = f"{self.base_url}/getTaskResult"
            while True:
                result = requests.post(get_url, json={"clientKey": self.api_key, "taskId": task_id}, timeout=30).json()
                
                if result.get("status") == "ready":
                    return result["solution"]["text"]
                
                time.sleep(5)  # espera 5s antes de tentar de novo

        except Exception as e:
            print(f"Erro: {e}")
            return None