import requests

class BaixarCertidaoViaApi:
    def __init__(self):
        pass 
    
    def baixa_certidao_api(self, url):
        # Faz a requisição para baixar o arquivo
        response = requests.get(url, timeout=300)

        # Verifica se deu certo
        if response.status_code == 200:
            # Salva o conteúdo como arquivo HTML
            with open("certidao.html", "wb") as f:
                f.write(response.content)
            print("Arquivo baixado com sucesso como 'certidao.html'")
        else:
            print(f"Erro ao baixar o arquivo: {response.status_code}")