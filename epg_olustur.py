import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

tv = ET.Element('tv')

# Kanal Tanımı
channel = ET.SubElement(tv, 'channel', id='ShowTV.tr')
display_name = ET.SubElement(channel, 'display-name')
display_name.text = "Show TV"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    url = "https://www.showtv.com.tr/yayin-akisi"
    response = requests.get(url, headers=headers, timeout=15)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        bugun = datetime.now().strftime("%Y%m%d")
        
        # Show TV'nin güncel site yapısındaki yayın öğelerini tara
        items = soup.select('div.stream-item, li.stream-item, ul.broadcast-list li')
        
        for item in items:
            saat_elem = item.select_one('.time, span.time, div.time')
            baslik_elem = item.select_one('.title, span.title, div.title, h3')
            
            if saat_elem and baslik_elem:
                saat = saat_elem.text.strip().replace(":", "")
                if len(saat) == 4:
                    saat = saat + "00"
                
                baslik = baslik_elem.text.strip()
                
                programme = ET.SubElement(tv, 'programme', start=f"{bugun}{saat} +0300", stop=f"{bugun}{saat} +0300", channel="ShowTV.tr")
                title = ET.SubElement(programme, 'title', lang="tr")
                title.text = baslik
except Exception as e:
    print(f"Web kazıma hatası: {e}")

# XML Kaydet
tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
)
