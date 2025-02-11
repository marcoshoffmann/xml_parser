from os import getenv
from dotenv import load_dotenv
load_dotenv()

class PathManager:
    def __init__(self):
        self.path_xmls = getenv("PATH_XMLS")
