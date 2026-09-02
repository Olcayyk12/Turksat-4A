import subprocess
import re

# Eklenecek YouTube Canlı Yayın Bilgileri
YOUTUBE_URL = "https://www.youtube.com/live/6QZ_qc75ihU"
CHANNEL_MARKER = "Yonhap News TV"  # playlist.m3u dosyasındaki kanal adı arama etiketi

try:
    # yt-dlp ile canlı yayının ham m3u8 adresini alıyoruz
    cmd = f"yt-dlp -g '{YOUTUBE_URL}'"
    m3u8_url = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

    # M3U dosyasını oku
    with open("playlist.m3u", "r", encoding="utf-8") as f:
        content = f.read()

    # M3U içindeki ilgili kanalın m3u8 linkini yenisiyle değiştir
    pattern = rf'(#EXTINF:-1.*{CHANNEL_MARKER}.*\n)(http[^\n]+)'
    new_content = re.sub(pattern, rf'\g<1>{m3u8_url}', content)

    # Güncellenmiş dosyayı kaydet
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Yonhap News TV yayın adresi başarıyla güncellendi.")
except Exception as e:
    print(f"Hata oluştu: {e}")
