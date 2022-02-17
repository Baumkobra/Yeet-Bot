from lib2to3.pytree import HUGE
import requests
from bs4 import BeautifulSoup
import lxml
class Heuriger:
    def __init__(self, name, adresse,telefonnummer,nochoffen) -> None:
        self.name = name
        self.adresse = adresse
        self.telefonnummer = telefonnummer
        self.tagenochoffen = nochoffen
def fetch()-> list[Heuriger]:
    """
    returns a Heuriger Object
    """
    rtl = []
    x = requests.get('https://www.pdorf.at/home.php')
    #"/html/body/font/div/table/tbody/tr/td[1]/font/blockquote/b/ul"
    soup = BeautifulSoup(x.content, 'html.parser')
    s = soup.find("ul")
    
            

    for child in s.find_all("li"):
        child:BeautifulSoup
        data = child.text.split(",")
        name = data[0]
        adresse = data[1]
        telefonnummer = data[2]
        nochoffen = data[-1]
        
        if "-" in telefonnummer:
            telefonnummer = "--"
        self = Heuriger(name,adresse,telefonnummer,nochoffen=nochoffen)
        rtl.append(self)
    return rtl


def pretty_fetch():
    """
    returns the same as fetch but pretty
    """
    data = fetch()
    txt = ""
    for heuriger in data:
        txt += f"{heuriger.name} | Adresse: {heuriger.adresse} |noch offen: {heuriger.tagenochoffen} |Tel: {heuriger.telefonnummer} |\n"

    return txt