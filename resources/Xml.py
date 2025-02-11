from sys import exit
from os import getenv, listdir
from datetime import datetime
from resources.FIlesManager import FilesManager

class Xml:
    def __init__(self):
        self.filesmanager = FilesManager()
        self.new_name = str(datetime.now()).replace(":", ".")
        self.new_name = f'{getenv("USERPROFILE")}\\Downloads\\{str(datetime.now()).replace(":", ".")}.csv'
        self.pattern_tag = 'xmlns="http://www.portalfiscal.inf.br/nfe"'
        self.tax_tags = ['<prod>', '<ICMS>', '<IPI>', '<PIS>', '<COFINS>']
        self.target_tags_info = {
                                '<ide>': ['<nNF>', '<dhEmi>'],
                                '<emit>': ['<CNPJ>', '<CPF>', '<xNome>', '<IE>'],
                                '<dest>': ['<CNPJ>', '<CPF>', '<xNome>', '<IE>'],
                                }
        self.target_tags = {
                            '<prod>':   ['<det nItem="', '<CFOP>', '<cProd>', '<xProd>', '<NCM>'],
                            '<ICMS>':   ['<orig>', ['<CST>', 'CSOSN'], '<modBC>', '<vBC>', '<pICMS>', '<vICMS>', '<vFCP>', '<modBCST>', '<pMVAST>', '<vBCST>', '<pICMSST>', '<vICMSST>', '<vBCFCPST>', '<pFCPST>', '<vFCPST>'],
                            '<IPI>':    ['<cEnq>', '<CST>', '<vBC>', '<pIPI>', '<vIPI>'],
                            '<PIS>':    ['<CST>', '<vBC>', '<pPIS>', '<vPIS>'],
                            '<COFINS>': ['<CST>', '<vBC>', '<pCOFINS>', '<vCOFINS>', '<vNF>', '<infCpl>', 'VAREJO', 'NCM', 'DESCRIÇÃO']
                            }
        
        self.ignore = ['<det nItem="', '<vNF>', '<infCpl>', 'VAREJO', 'NCM', 'DESCRIÇÃO']
        self.linhas_csv = []
        # self.csv_file = open(file=f'{getenv("USERPROFILE")}\\Downloads\\{self.new_name}.csv', mode='w', encoding='utf-8')
        self.csv_file = open(file=self.new_name, mode='w', encoding='utf-8')
        self.somar = [18+1, 20+1, 21+1, 24+1, 26+1, 27+1, 29+1, 32+1, 34+1, 36+1, 38+1, 40+1, 42+1, 43+1]

    def layout_verify(self, file: str) -> str:
        if file.lower().endswith('.xml'): xml = open(file=file, mode='r', encoding='utf-8').read()
        if self.pattern_tag in xml and "<total>" in xml: return xml

    def extract_infos(self, file: str):
        infos_list = []
        data = self.layout_verify(file)
        if self.layout_verify(file):
            data = [f'<{tag}' for tag in data.split('<') if not '</' in f'<{tag}']
            for tag in data:
                if '<chNFe>' in tag:
                    chave = tag
                    break

            infos_list.append(chave)
            position_infos = [position for position in range(len(data)) for tag in self.target_tags_info if tag in data[position]]
            start_items = data.index('<det nItem="1">')
            infos = {}

            for position in range(len(position_infos)):
                try:
                    infos[data[position_infos[position]]] = data[position_infos[position]+1:position_infos[position + 1]]
                except IndexError:
                    infos[data[position_infos[position]]] = data[position_infos[position]+1:start_items]

            for tag_info, values in self.target_tags_info.items():
                for value in values:
                    if tag_info in infos:
                        for info in infos[tag_info]:
                            if value in info:
                                infos_list.append(info)
                                break
                            elif value not in info and info == infos[tag_info][-1]:
                                infos_list.append(float(0))
                                break
                    else:
                        infos_list.append(0.0)
        return infos_list

    def extract_data(self, file: str) -> None:
        data = self.layout_verify(file)
        valor = True
        ncm = True
        cpl = True

        if self.layout_verify(file):
            linha_csv = []
            data = [f'<{tag}' for tag in data.split('<') if not '</' in f'<{tag}' and f'<{tag}' != '</imposto>']
            valor_nota = '0,00'
            inf_cpl = '-'
            for tag in data:
                if '<vNF>' in tag:
                    valor_nota = str(tag.split(">")[-1]).replace(".", ",")
                elif '<infCpl>' in tag:
                    inf_cpl = str(tag.split(">")[-1]).replace(".", ",")
            
            end_items = data.index('<total>')
            position_items = [position for position in range(len(data)) if '<det nItem="' in data[position]]
            items = {}

            for position in range(len(position_items)):
                try:
                    items[data[position_items[position]]] = data[position_items[position]+1:position_items[position + 1]]
                except IndexError:
                    items[data[position_items[position]]] = data[position_items[position]+1:end_items]

            for key, values in items.items():
                if '<impostoDevol>' in values:
                    end_values = values.index('<impostoDevol>')
                    items[key] = values[:end_values]

            for item, values in items.items():
                linha_csv = []
                linha_csv.extend(self.extract_infos(file=file))
                linha_csv.append(item)
                position_tax =[]
                for tax in self.tax_tags:
                    for tax_values in range(len(values)):
                        if tax == values[tax_values]:
                            position_tax.append(tax_values)
                dict_tax = {}

                for tax in self.target_tags:
                    dict_tax[tax] = []
                
                for position in range(len(position_tax)):
                    try:
                        dict_tax[values[position_tax[position]]] = values[position_tax[position] + 1:position_tax[position + 1]]
                    except IndexError:
                        dict_tax[values[position_tax[position]]] = values[position_tax[position] + 1:]

                for tax in self.target_tags:
                    if dict_tax[tax] == []:
                        for _ in self.target_tags[tax]:
                            dict_tax[tax].append('0,00')
                for tax, values in dict_tax.items():
                    for target_tag in self.target_tags[tax]:
                        if target_tag not in self.ignore:
                            for value in values:
                                    if isinstance(target_tag, list):
                                        if target_tag[0] in value or target_tag[1] in value:
                                            linha_csv.append(str(value).replace(".", ","))
                                            break
                                    elif target_tag in value:
                                        linha_csv.append(str(value).replace(".", ","))
                                        break
                                    elif target_tag not in value and value == values[-1]:
                                        linha_csv.append('0,00')
                                        break
                
                if valor is True:
                    linha_csv.append(valor_nota)
                    valor = False
                else:
                    linha_csv.append('0,00')
                if cpl is True:
                    linha_csv.append(inf_cpl)
                    cpl = False
                else:
                    linha_csv.append('-')
                if ncm is True:
                    linha_csv.extend(['0,00', '0,00', '-'])
                    ncm = False
                self.linhas_csv.append(linha_csv)
        
    def extract_all(self):
        for xml_file in self.filesmanager.list_xmls():
            self.extract_data(file=xml_file)
        return self.linhas_csv

    def make_header(self):
        linhas = self.extract_all()
        lista_nova = ["" for _ in linhas[0]]
        for soma in self.somar:
            globals()[f'soma_{soma}'] = float(0)
            for linha in linhas:
                try:
                    globals()[f'soma_{soma}'] += float(str(linha[soma].split(">")[-1]).replace(",", "."))
                except IndexError:
                    pass
                except ValueError:
                    pass
            lista_nova[soma] = str(globals()[f'soma_{soma}']).replace(".", ",")

        for item in lista_nova:
            self.csv_file.write(f'{item.replace(";", "")};')
        self.csv_file.write('\n')

        header = ['<chNFe>']
        for key, values in self.target_tags_info.items():
            header.extend(values)
        for key, values in self.target_tags.items():
            header.extend(values)
            
        for tag in header:
            self.csv_file.write(f'{tag};')
        self.csv_file.write(f'\n')
    
    def add_csv(self) -> None:
        linhas = self.linhas_csv
        for linha in linhas:
            if linha[2] != float(0):
                linha[2] = linha[2][:17]
            for item in linha:
                if '>' in str(item) and not '<det nItem=' in str(item):
                    self.csv_file.write(f'{item.split(">")[-1].replace(";", "")};')
                elif not isinstance(item, float) and not isinstance(item, int):
                    self.csv_file.write(f'{item.replace(";", "")};')
                else:
                    self.csv_file.write(f'{item};')
                
            self.csv_file.write('\n')
        self.csv_file.close()
        return self.new_name
