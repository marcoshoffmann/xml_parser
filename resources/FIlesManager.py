from os import listdir
from resources.PathManager import PathManager

class FilesManager:
    def __init__(self):
        self.pathmanager = PathManager()

    def list_xmls(self) -> list:
        return [f'{self.pathmanager.path_xmls}\\{file}' for file in listdir(self.pathmanager.path_xmls) if file.lower().endswith('.xml')]
