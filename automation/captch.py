import base64
import cv2
import numpy as np
from PIL import Image
from selenium.webdriver.common.by import By
import pytesseract

# Caminho do tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class CaptchaCapture:
    def __init__(self, driver):
        self.driver = driver

    def quebrar_captcha(self, salvar_debug=True):
        # 1. Captura imagem base64
        img_element = self.driver.find_element(By.ID, "idImgBase64")
        img_base64 = img_element.get_attribute("src").split(",")[1]
        img_bytes = base64.b64decode(img_base64)

        # 2. Decodifica imagem
        np_img = np.frombuffer(img_bytes, np.uint8)
        imagem_colorida = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if imagem_colorida is None:
            raise ValueError("Erro ao decodificar imagem.")

        # 3. Converte para escala de cinza
        cinza = cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2GRAY)

        # 4. Redimensiona (aumenta para melhorar OCR)
        ampliada = cv2.resize(cinza, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

        # 5. Binariza com THRESH_BINARY
        binarizada = cv2.adaptiveThreshold(
            ampliada, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )

        # 6. Remove ruído
        kernel = np.ones((2, 2), np.uint8)
        limpa = cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel)

        # 7. Salva imagem para debug (opcional)
        if salvar_debug:
            cv2.imwrite("debug_captcha.png", limpa)

        # 8. OCR com Tesseract
        pil_img = Image.fromarray(limpa)
        config = r'--psm 6 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        texto = pytesseract.image_to_string(pil_img, config=config)

        return texto.strip()
