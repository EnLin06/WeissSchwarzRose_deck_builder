import requests
import json
from bs4 import BeautifulSoup as bs

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html",
    "Referer": "https://www.google.com"
}
database = {}

def getdata(series, id):
    url = f"https://ws-rose.com/cardlist/?cardno={id}&expansion={series}&view=image"
    req = requests.get(url, headers=headers)

    card = {}
    html = bs(req.text, "html.parser")
    img = html.find(class_= 'thumbnail-Inner').find("img")['src']
    card['img'] = f"https://ws-rose.com{img}"
    card['name'] = html.find(class_ = "item-Heading").contents[0].strip()

    data = html.find_all(class_= 'dl-Item')
    for things in data:
        datatype = things.find("span")
        content = things.find("dd")
        if datatype.text.strip() == "カード番号":
            card["id"] = content.text.strip()
        if datatype.text.strip() == "レアリティ":
            card["rarity"] = content.text.strip()
        if datatype.text.strip() == "種類":
            card["type"] = content.text.strip()
        if datatype.text.strip() == "レベル":
            card["level"] = content.text.strip()
        if datatype.text.strip() == "コスト":
            card["cost"] = content.text.strip()
        if datatype.text.strip() == "パワー":
            card["power"] = content.text.strip()
        if datatype.text.strip() == "特徴":
            card["special"] = content.text.strip()
        if datatype.text.strip() == "ソウル":
            souls = content.find_all("img")
            card['souls'] = len(souls)
        if datatype.text.strip() == "色":
            card['color'] = content.find("img")['alt']
        if datatype.text.strip() == "テキスト":
            effect = content.get_text(separator="\n").strip()
            card['effect'] = effect

    return card


database = {}
product_name = input("請輸入商品代號(如R01、R02、R01-T...) : ")
series = input("請輸入系列號(如OS01、OS02...) : ")
isTD = input("是否是預組?(y/n) :")
card_num = int(input("請輸入該產品有幾張卡"))
name = input("請輸入檔名")

Td = True if isTD == 'y' else False
for i in range(1, card_num+1):
    if Td:
        code = f"T{str(i).zfill(2)}"
    else:
        code = str(i).zfill(3)
    if Td:
        database[f'T{code}'] = getdata(product_name, f"{series}/{product_name}{code}")
        print(f"T{code} 已完成")
    else:
        database[code] = getdata(product_name, f"{series}/{product_name}{code}")
        print(f"{code} 已完成")
    
with open(f'json/{name}.json', 'w', encoding='utf-8') as f:
    json.dump(database, f, ensure_ascii=False, indent=2)
