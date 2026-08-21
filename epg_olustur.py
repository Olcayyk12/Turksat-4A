import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

# XML Kökü
tv = ET.Element('tv')

# Kanal Tanımı
channel = ET.SubElement(tv, 'channel', id='ShowTV.tr')
display_name = ET.SubElement(channel, 'display-name')
display_name.text = "Show TV"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    url = "https://www.showtv.com.tr/yayin-akisi"
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        bugun = datetime.now().strftime("%Y%m%d")
        
        # Sayfadaki tüm liste elemanlarını tara
        programlar = soup.select('ul.stream-list li, li.stream-item, div.stream-item')
        
        for prog in programlar:
            saat_elem = prog.select_one('.time, span.time')
            baslik_elem = prog.select_one('.title, span.title, div.title')
            
            if saat_elem and baslik_elem:
                saat = saat_elem.text.strip().replace(":", "").zfill(4) + "00"
                baslik = baslik_elem.text.strip()
                
                programme = ET.SubElement(tv, 'programme', start=f"{bugun}{saat} +0300", stop=f"{bugun}{saat} +0300", channel="ShowTV.tr")
                title = ET.SubElement(programme, 'title', lang="tr")
                title.text = baslik
except Exception as e:
    print(f"Hata: {e}")

# XML Kaydet
tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
