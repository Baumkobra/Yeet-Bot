
import requests
from bs4 import BeautifulSoup
import lxml
class Heuriger:
    def __init__(self, name, adresse,telefonnummer,nochoffen, url) -> None:
        self.name = name
        self.adresse = adresse
        self.telefonnummer = telefonnummer
        self.tagenochoffen = nochoffen
<<<<<<< HEAD:new/heuriger.py
        self.url = url
def fetch()-> list[Heuriger]:
=======
def fetch():
>>>>>>> 70f81096ff47c653f720d83bac28f0fe4e2a2300:heuriger.py
    """
    returns a Heuriger Object
    """
    rtl = []
    x = requests.get('https://www.pdorf.at/home.php')
    
    soup = BeautifulSoup(x.content, 'html.parser')
    
    #"/html/body/font/div/table/tbody/tr/td[1]/font/blockquote/b/ul"
    s = soup.find("ul")
    for child in s.find_all("li"):
        child:BeautifulSoup  

        url = child.find("a")["href"] 

        data = child.text.split(",")
        name = data[0]
        adresse = data[1]
        telefonnummer = data[2]
        nochoffen = data[-1]
        
        if "-" in telefonnummer:
            telefonnummer = "--"

        self = Heuriger(name=name,adresse=adresse,telefonnummer=telefonnummer,nochoffen=nochoffen,url=url)
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