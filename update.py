import subprocess

YOUTUBE_URL = "https://www.youtube.com/live/6QZ_qc75ihU"
CHANNEL_MARKER = "Yonhap News TV"

try:
    # yt-dlp ile canlı yayının m3u8 adresini çekiyoruz
    cmd = f"yt-dlp -g '{YOUTUBE_URL}'"
    m3u8_url = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

    # m3u dosyasını oku ve satır satır güncelle
    with open("playlist.m3u", "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    update_next = False

    for line in lines:
        if update_next:
            new_lines.append(m3u8_url + "\n")
            update_next = False
        else:
            new_lines.append(line)
            if CHANNEL_MARKER in line:
                update_next = True

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print("Yayın linki başarıyla güncellendi.")
except Exception as e:
    print(f"Hata
    : {e}")
