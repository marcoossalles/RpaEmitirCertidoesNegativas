import logging
import inspect
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler, SMTPHandler, SysLogHandler
class Logger:
    """
    Classe Logger para criar e gerenciar logs de aplicação de forma centralizada.
    Implementa o padrão Singleton para evitar múltiplas instâncias do logger.
    Inclui configurações avançadas como logs rotativos por tempo, envio por e-mail e integração com syslog.
    """
    _instances = {}  # Dicionário para armazenar instâncias do logger por nome
    
    def __new__(cls, name: str, log_file: str=None , level: int = logging.DEBUG,
                rotate_by_time: bool = False, email_errors: bool = False, syslog: bool = False,maestro = None ):
        """
        Método para garantir que apenas uma instância do logger seja criada por nome.
        """
        if name not in cls._instances:
            instance = super(Logger, cls).__new__(cls)
            instance._initialize_logger(name, log_file, level, rotate_by_time, email_errors, syslog, maestro)
            cls._instances[name] = instance
        return cls._instances[name]

    def _initialize_logger(self, name: str, log_file: str, level: int, rotate_by_time: bool, email_errors: bool, syslog: bool,maestro):
        """
        Inicializa o logger com configurações de nível, formatação e handlers avançados.
        """
        self.logger = logging.getLogger(name)  # Cria ou obtém um logger com o nome fornecido
        self.logger.setLevel(level)  # Define o nível de log como DEBUG para capturar todos os logs
        self.logger.propagate = False  # Impede que mensagens sejam propagadas para loggers ancestrais
        self.maestro = maestro

        # Define o formato da mensagem de log, incluindo o nome da função
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
        
        # Escolhe entre log rotativo por tamanho ou tempo
        if rotate_by_time:
            file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7)
        else:
            file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        
        file_handler.setFormatter(formatter)
        
        # Cria um manipulador de saída para o console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        # Adiciona suporte para envio de logs por e-mail em caso de erro
        if email_errors:
            smtp_handler = SMTPHandler(mailhost=("smtp.example.com", 587),
                                       fromaddr="noreply@example.com",
                                       toaddrs=["admin@example.com"],
                                       subject="Erro crítico no sistema",
                                       credentials=("user", "password"),
                                       secure=())
            smtp_handler.setLevel(logging.ERROR)
            smtp_handler.setFormatter(formatter)
            self.logger.addHandler(smtp_handler)
        
        # Adiciona suporte para integração com SysLog
        if syslog:
            syslog_handler = SysLogHandler(address=("localhost", 514))
            syslog_handler.setFormatter(formatter)
            self.logger.addHandler(syslog_handler)
        
        # Adiciona handlers sem a verificação que pode impedir a gravação dos logs
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
    
    def _log(self, level, message):
        """Método interno para registrar logs incluindo o nome da classe e da função automaticamente."""
        stack = inspect.stack()[2]
        module = inspect.getmodule(stack[0])
        class_name = module.__name__.split('.')[-1] if module else "Unknown"
        func_name = stack.function  # Obtém o nome da função chamadora
        self.logger.log(level, f"[{class_name}.{func_name}] {message}")
    
    def debug(self, message: str):
        """Registra uma mensagem de depuração (DEBUG)"""
        self._log(logging.DEBUG, message)
    
    def info(self, message: str):
        """Registra uma mensagem informativa (INFO)"""
        self._log(logging.INFO, message)
    
    def warning(self, message: str):
        """Registra uma mensagem de aviso (WARNING)"""
        self._log(logging.WARNING, message)
    
    def error(self, message: str):
        """Registra uma mensagem de erro (ERROR)"""
        self._log(logging.ERROR, message)
    
    def critical(self, message: str):
        """Registra uma mensagem crítica (CRITICAL)"""
        self._log(logging.CRITICAL, message)

