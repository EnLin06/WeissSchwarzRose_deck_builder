import os
import requests
import json

def download_image(img_url, series, card_id):
    save_path = f"image/{series}/{card_id}.jpg"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        response = requests.get(img_url, timeout=5)
        response.raise_for_status()
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"下載完成：{save_path}")
    except requests.RequestException as e:
        print(f"下載失敗：{img_url} - {e}")

target = str(input("請輸入系列代碼(json檔案檔名) : "))
with open(f"json/{target}.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    for  id, index in data.items():
        download_image(index['img'], target, id)