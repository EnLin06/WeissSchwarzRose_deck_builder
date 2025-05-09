from PIL import Image

def create_deck(deck, output_path):
    cols = 10
    rows = (len(deck) + cols - 1) // cols
    card_width, card_height = 300, 400

    # 建立空白背景
    deck_image = Image.new("RGB", (cols * card_width, rows * card_height), "white")

    # 排列卡片
    for idx, (series, card_id, card_type, _) in enumerate(deck):
        img_path = f"image/{series}/{card_id}.jpg"
        try:
            card_img = Image.open(img_path).resize((card_width, card_height))
            if card_type == "クライマックス":
                # 旋轉 90 度（順時針）
                card_img = card_img.rotate(-90, expand=True)
                # 填充白色背景，避免旋轉後的空白部分
                new_img = Image.new("RGB", (300, 400), "white")
                card_img = card_img.resize((300, 400))
                new_img.paste(card_img, (0, 0))
                card_img = new_img
            else:
                # 普通卡片直接調整大小
                card_img = card_img.resize((300, 400))
            col = idx % cols
            row = idx // cols
            deck_image.paste(card_img, (col * card_width, row * card_height))
        except FileNotFoundError:
            pass

    # 儲存圖片
    deck_image.save(output_path)
