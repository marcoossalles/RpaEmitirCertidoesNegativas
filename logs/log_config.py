import logging
import os

# Define a pasta de logs
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # cria a pasta se não existir

# Define o arquivo de log
log_file = os.path.join(log_dir, "logs.txt")

# Configuração do logger
logger = logging.getLogger()  # pega o logger raiz
logger.setLevel(logging.INFO)

# Formato do log
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Handler para salvar no arquivo
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler para imprimir no console (opcional)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Exemplo de log
logger.info("Logger configurado com pasta e arquivo separado!")
