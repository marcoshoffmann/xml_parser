from resources.Xml import Xml
from tkinter import messagebox

if __name__ == '__main__':
    try:
        xml = Xml()
        xml.make_header()
        xml.add_csv()
        messagebox.showinfo(title="SUCESSO", message=f"OPERAÇÃO FINALIZADA COM SUCESSO!\nARQUIVO SALVO: {xml.new_name}")
    except Exception as error: messagebox.showerror(title="ERROR!!!", message=f'OPERAÇÃO NÃO FINALIZADA CORRETAMENTE, ERRO:\n{error}')
