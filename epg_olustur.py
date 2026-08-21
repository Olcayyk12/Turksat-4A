import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

tv = ET.Element('tv')
channel1 = ET.SubElement(tv, 'channel', id='ShowTV.tr')
display_name1 = ET.SubElement(channel1, 'display-name')
display_name1.text = "Show TV"

headers = {'User-Agent': 'Mozilla/5.0'}

try:
    res = requests.get("https://www.showtv.com.tr/yayin-akisi", headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    bugun = datetime.now().strftime("%Y%m%d")
    
    programlar = soup.find_all('li', class_='stream-item')
    for prog in programlar:
        saat_elem = prog.find('span', class_='time')
        baslik_elem = prog.find('span', class_='title')
        
        if saat_elem and baslik_elem:
            saat = saat_elem.text.strip().replace(":", "") + "00"
            baslik = baslik_elem.text.strip()
            
            programme = ET.SubElement(tv, 'programme', start=f"{bugun}{saat} +0300", stop=f"{bugun}{saat} +0300", channel="ShowTV.tr")
            title = ET.SubElement(programme, 'title', lang="tr")
            title.text = baslik
except Exception as e:
    print("Hata:", e)

tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
