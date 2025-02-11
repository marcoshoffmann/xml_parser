import webview

from resources.Xml import Xml

import sys

class MyAPI:
    def __init__(self):
        self.xml = Xml()

    def process_files(self):
        try:
            self.xml.make_header()
            operacao = self.xml.add_csv()
            # operacao = self.xml.extract_all()
            # Simulação de resposta após processamento
            return f"Arquivos processados com sucesso!\nSalvo como: {operacao}"
        except Exception as error:
            return f'Ocorreu o erro: {error}'
    
    def sair(self):
        sys.exit()

def main():
    api = MyAPI()
    try:
        webview.create_window(
            "Comunicação HTML e Python",
            "index.html",  # Certifique-se de que o caminho esteja correto
            js_api=api,
            # icon=".\\static\\boaro_logotipo-em-marca-dagua_sem-fundo_9_4x-8.ico"
        )
        webview.start(server_args={}, icon='.\\static\\boaro_logotipo-em-marca-dagua_sem-fundo_9_4x-8.ico')
    except Exception as error:
        print(f'Error: {error}')

if __name__ == '__main__':
    main()
