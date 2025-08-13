import logging
from dotenv import load_dotenv
import os
import logging

try:
    # Caminho para o arquivo .env dentro da pasta 'env'
    env_path = os.path.join("env", ".env")
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"Arquivo .env não encontrado em {env_path}")
    
    load_dotenv(dotenv_path=env_path)
    logging.info(f".env carregado com sucesso de {env_path}")

except Exception as e:
    logging.error(f"Erro ao carregar o .env: {e}")
    # Opcional: re-raise se quiser que o erro pare a execução
    # raise
