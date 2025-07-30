import cv2
import pytesseract
import numpy as np
from PIL import Image

class CaptchaCapture:
    def __init__(self):
        pass

    def quebrar_captcha(self, imagem_path):
        # 1. Carrega imagem
        imagem_colorida = cv2.imread(imagem_path)
        if imagem_colorida is None:
            raise FileNotFoundError(f"Imagem não encontrada: {imagem_path}")

        # 2. Converte para escala de cinza
        cinza = cv2.cvtColor(imagem_colorida, cv2.COLOR_BGR2GRAY)

        # 3. Aplica binarização adaptativa
        binarizada = cv2.adaptiveThreshold(
            cinza, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )

        # 4. Remove ruídos
        kernel = np.ones((2, 2), np.uint8)
        limpa = cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel)

        # 5. Executa OCR
        config_tesseract = r'--psm 7 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        texto = pytesseract.image_to_string(limpa, config=config_tesseract)

        return texto.strip()

# Exemplo de uso:
if __name__ == "__main__":
    captcha = CaptchaCapture()
    print(captcha.quebrar_captcha("captcha1.png"))  # Ex: r3jinn
    print(captcha.quebrar_captcha("captcha2.png"))  # Ex: 715dm
