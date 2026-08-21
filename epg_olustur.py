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

url = "https://tvplus.com.tr/canli-tv/yayin-akisi/show-tv-hd--130"

try:
    response = requests.get(url, headers=headers, timeout=15)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        bugun = datetime.now().strftime("%Y%m%d")
        
        # TV+ sayfasındaki yayın kartlarını ve içeriklerini bulur
        for container in soup.find_all(['div', 'li']):
            # Saat bilgisini yakala (örn: 00:15 - 02:15)
            text_content = container.get_text(" ", strip=True)
            
            # Başlıkları div/h2/h3/h4 etiketlerinden çek
            title_elem = container.find(['h2', 'h3', 'h4', 'div', 'span'], class_=lambda c: c and ('title' in c.lower() or 'name' in c.lower()))
            time_elem = container.find(['span', 'div', 'p'], class_=lambda c: c and ('time' in c.lower() or 'date' in c.lower() or 'hour' in c.lower()))
            
            if title_elem and time_elem:
                baslik = title_elem.text.strip()
                saat_metni = time_elem.text.strip()
                
                # Saat formatını ayıkla (00:15 -> 001500)
                if ":" in saat_metni:
                    baslangic_saati = saat_metni.split("-")[0].strip().replace(":", "")
                    if len(baslangic_saati) == 4:
                        baslangic_saati += "00"
                        
                        programme = ET.SubElement(tv, 'programme', start=f"{bugun}{baslangic_saati} +0300", stop=f"{bugun}{baslangic_saati} +0300", channel="ShowTV.tr")
                        title = ET.SubElement(programme, 'title', lang="tr")
                        title.text = baslik

except Exception as e:
    print(f"TV+ Kazıma Hatası: {e}")

# Her ihtimale karşı dosya boş kalmasın diye fallback kontrolü
if len(tv.findall('programme')) == 0:
    # Sayfa yapısı render edilemezse doğrudan TV+ JSON API yapısından dener
    try:
        api_url = "https://tvplus.com.tr/api/epg/show-tv-hd--130"
        res = requests.get(api_url, headers=headers, timeout=10).json()
        bugun = datetime.now().strftime("%Y%m%d")
        for p in res.get('data', []):
            programme = ET.SubElement(tv, 'programme', start=f"{bugun}{p['start']}00 +0300", stop=f"{bugun}{p['end']}00 +0300", channel="ShowTV.tr")
            title = ET.SubElement(programme, 'title', lang="tr")
            title.text = p['name']
    except:
        pass

tree = ET.ElementTree(tv)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)

