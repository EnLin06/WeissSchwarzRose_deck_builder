import sys
import json
import os
import deck_creater
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import Qt

def sort_key(card):
    series, card_id, card_type, level = card

    # 名場面：單獨排序，僅按卡號順序排
    if card_type == "クライマックス":
        if "T" in card_id:
            return (3, int(card_id.replace("T", "")))  # 名場面卡片排序優先級最低
        return (3, int(card_id))

    # 角色卡 (キャラ) 排第一優先
    elif card_type == "キャラ":
        return (1, level, int(card_id.replace("T", "")))

    # 事件卡 (イベント) 排第二優先
    elif card_type == "イベント":
        return (2, level, int(card_id.replace("T", "")))

    # 未知類型，放最後
    return (99, 999, int(card_id.replace("T", "")))


class CardViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WSR Card Viewer")
        self.setGeometry(100, 100, 800, 600)

        # 讀取資料
        self.data = {}

        #空牌組
        self.deck = []

        # 主布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QHBoxLayout(self.main_widget)

        # 左側布局
        self.filter_widget = QWidget()
        self.filter_layout = QVBoxLayout(self.filter_widget)
        self.filter_widget.setFixedWidth(250)  # 固定寬度

        # 類型篩選
        self.type_combo = QComboBox()
        self.type_combo.addItem("全部類型")
        self.type_combo.addItems(["角色", "事件", "名場面"])
        self.type_combo.currentIndexChanged.connect(lambda : self.filter(False))
        self.filter_layout.addWidget(QLabel("類型："))
        self.filter_layout.addWidget(self.type_combo)

        # 顏色篩選
        self.color_combo = QComboBox()
        self.color_combo.addItem("全部顏色")
        self.color_combo.addItems(["黃", "綠", "紅", "藍"])
        self.color_combo.currentIndexChanged.connect(lambda : self.filter(False))
        self.filter_layout.addWidget(QLabel("顏色："))
        self.filter_layout.addWidget(self.color_combo)

        # 等級篩選
        self.level_combo = QComboBox()
        self.level_combo.addItem("全部等級")
        self.level_combo.addItems([str(i) for i in range(4)])
        self.level_combo.currentIndexChanged.connect(lambda : self.filter(False))
        self.filter_layout.addWidget(QLabel("等級："))
        self.filter_layout.addWidget(self.level_combo)

        # 費用篩選
        self.cost_combo = QComboBox()
        self.cost_combo.addItem("全部費用")
        self.cost_combo.addItems([str(i) for i in range(4)])
        self.cost_combo.currentIndexChanged.connect(lambda : self.filter(False))
        self.filter_layout.addWidget(QLabel("費用："))
        self.filter_layout.addWidget(self.cost_combo)

        # 魂值篩選
        self.soul_combo = QComboBox()
        self.soul_combo.addItem("全部魂值")
        self.soul_combo.addItems([str(i) for i in range(4)])
        self.soul_combo.currentIndexChanged.connect(lambda : self.filter(False))
        self.filter_layout.addWidget(QLabel("魂值："))
        self.filter_layout.addWidget(self.soul_combo)

        # 名稱篩選
        self.name_kw = QLineEdit()
        self.name_kw.setPlaceholderText("輸入名稱關鍵字 (按下enter來篩選)")
        self.name_kw.returnPressed.connect(lambda : self.filter(False))
        self.filter_layout.addWidget(QLabel("名稱："))
        self.filter_layout.addWidget(self.name_kw)

        # 編號篩選
        self.effect_kw = QLineEdit()
        self.effect_kw.setPlaceholderText("輸入效果關鍵字 (按下enter來查詢)")
        self.effect_kw.returnPressed.connect(lambda : self.filter(False))
        self.filter_layout.addWidget(QLabel("效果："))
        self.filter_layout.addWidget(self.effect_kw)

         # 下拉選單
        self.combo_box = QComboBox()
        self.combo_box.addItems(["請選擇系列"])
        self.combo_box.currentIndexChanged.connect(lambda : self.filter(True))
        for file_name in os.listdir("json"):
            if file_name.endswith(".json"):
                with open(f"json/{file_name}", "r", encoding="utf-8") as file:
                    file_name = os.path.splitext(file_name)[0]
                    self.data[file_name] = json.load(file)
                # 去除副檔名並添加到下拉選單  
                self.combo_box.addItem(file_name)

        # 清空條件按鈕
        self.clear_button = QPushButton("清空牌組")
        self.clear_button.clicked.connect(self.clear_deck)
        self.filter_layout.addWidget(self.clear_button)

        # 清空條件按鈕
        self.filter_button = QPushButton("清空條件")
        self.filter_button.clicked.connect(lambda : self.filter(True))
        self.filter_layout.addWidget(self.filter_button)

        # 將篩選區域加入主佈局的左側
        self.layout.addWidget(self.filter_widget)        

        # 滾動區域
        self.shower_widget = QWidget()
        self.shower_layout = QVBoxLayout(self.shower_widget)

        self.shower_layout.addWidget(self.combo_box)
        

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.shower_layout.addWidget(self.scroll_area)

        # 內容區域 (放置在滾動區域之下)
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)


        # 牌組張數顯示區域
        self.deck_label = QLabel("目前牌組張數：0")
        self.shower_layout.addWidget(self.deck_label)

        # 預覽牌組按鈕
        self.preview_button = QPushButton("預覽牌組")
        self.preview_button.clicked.connect(self.preview_deck)
        self.shower_layout.addWidget(self.preview_button)

        self.layout.addWidget(self.shower_widget)

    def filter(self, isclear):
        if isclear:
            self.type_combo.setCurrentIndex(0)
            self.level_combo.setCurrentIndex(0)
            self.color_combo.setCurrentIndex(0)
            self.cost_combo.setCurrentIndex(0)
            self.soul_combo.setCurrentIndex(0)
            self.name_kw.clear()
            self.effect_kw.clear()

        selected_type = self.type_combo.currentText()
        selected_level = self.level_combo.currentText()
        selected_color = self.color_combo.currentText()
        selected_cost = self.cost_combo.currentText()
        selected_soul = self.soul_combo.currentText()
        name_keyword = self.name_kw.text().strip()
        effect_keyword = self.effect_kw.text().strip()
        
        selected_series = self.combo_box.currentText()
        self.select_data = self.data.get(selected_series, {})
        self.show_list = {}

        for key, datas in self.select_data.items():
            if selected_type != "全部類型":
                #"キャラ", "イベント", "クライマックス"
                if selected_type == "角色" and datas['type'] != "キャラ":
                    continue
                if selected_type == "事件" and datas['type'] != "イベント":
                    continue
                if selected_type == "名場面" and datas['type'] != "クライマックス":
                    continue

            if selected_level != "全部等級":
                if datas['level'] != selected_level:
                    continue

            if selected_color != "全部顏色":
                if selected_color == "藍" and datas['color'] != "青":
                    continue
                if selected_color == "紅" and datas['color'] != "赤":
                    continue
                if selected_color == "黃" and datas['color'] != "黄":
                    continue
                if selected_color == "綠" and datas['color'] != "緑":
                    continue

            if selected_cost != "全部費用":
                if datas['cost'] != selected_cost:
                    continue
                    
            if selected_soul != "全部魂值":
                if datas['souls'] != int(selected_soul):
                    continue
                

            if name_keyword:
                if name_keyword not in datas['name']:
                    continue   

            if effect_keyword:
                if effect_keyword not in datas['effect']:
                    continue

            self.show_list[key] = datas

        self.load_cards()
    def preview_deck(self):
        if not self.deck:
            return
        
        def remove_preview():
            preview_path = "preview.jpg"
            if os.path.exists(preview_path):
                try:
                    os.remove(preview_path)
                except Exception:
                    pass

        # 生成預覽圖片
        preview_path = "preview.jpg"
        deck_creater.create_deck(self.deck, preview_path)

        # 創建預覽視窗
        dialog = QDialog(self)
        dialog.setWindowTitle("預覽牌組")
        dialog.setFixedSize(630, 600)

        # 佈局
        layout = QVBoxLayout(dialog)

        # 牌組名稱輸入欄
        name_input = QLineEdit()
        name_input.setPlaceholderText("請輸入牌組名稱")
        name_input.setFixedHeight(30)

        # 圖片顯示區域
        img_label = QLabel()
        img_label.setFixedSize(600, 400)
        pixmap = QPixmap(preview_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(600, 400, Qt.KeepAspectRatio)
            img_label.setPixmap(pixmap)
        else:
            img_label.setText("圖片生成失敗")

        def handel_export(preview_path):
            self.clear_deck()
            deck_name = name_input.text().strip()
            if not deck_name:
                self.export_deck_image(preview_path, None)
                return
            self.export_deck_image(preview_path, deck_name)

        # 按鈕區域
        confirm_button = QPushButton("確定匯出")
        confirm_button.clicked.connect(lambda: (handel_export(preview_path), dialog.close(), remove_preview()))
        delete_button = QPushButton("清空牌組並取消")
        delete_button.clicked.connect(lambda: (dialog.close(), remove_preview(), self.clear_deck()))
        close_button = QPushButton("取消")
        close_button.clicked.connect(lambda: (remove_preview(), dialog.close()))

        # 加入佈局
        layout.addWidget(img_label)
        layout.addWidget(name_input)
        layout.addWidget(confirm_button)
        layout.addWidget(delete_button)
        layout.addWidget(close_button)

        dialog.exec()

    def clear_deck(self):
        self.deck = []
        self.deck_label.setText("目前牌組張數：0")

    def export_deck_image(self, path, deck_name=None):
        if not deck_name:
            index = 1
            while True:
                filename = f"牌組{index}.jpg"
                if not os.path.exists(f"deck/{filename}"):
                    break
                index += 1
        else:
            filename = f"{deck_name}.jpg"

        try:
            os.rename(path, filename)
            shutil.move(filename, f"deck/{filename}")
        except Exception as e:
            pass


    def load_cards(self):
        series = self.combo_box.currentText()
        # 清除目前的內容區域
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # 建立"卡片"
        for index, card_id in enumerate(self.show_list):
            
            card_info = self.show_list[card_id]

            # 每個卡片都是一個Label，並貼圖上去
            card_label = QLabel()
            card_label.setStyleSheet('border: 1px solid #000;')  # 顯示邊框方便點擊識別
            card_label.mousePressEvent = lambda event, card_id=card_id: self.show_card_info(series, card_id)
            iscx = False

            # 判斷是不是CX
            if card_info['type'] == 'クライマックス':
                iscx = True

            card_label.setFixedSize(150, 200)
            card_label.setStyleSheet('border: 1px solid #000;')
            card_label.setScaledContents(True)
            self.load_image(card_label, series, card_id, iscx)

            self.scroll_layout.addWidget(card_label, index // 8, index % 8)

    def load_image(self, label, series, card_id, iscx):
        try:
            # 生成圖片路徑
            file_path = f"image/{series}/{card_id}.jpg"
            if not os.path.exists(file_path):
                label.setText("圖片不存在")
                return

            # 加載圖片
            pixmap = QPixmap(file_path)
            if iscx:
                pixmap = pixmap.transformed(QTransform().rotate(90))
            label.setPixmap(pixmap)
        except Exception as e:
            label.setText("Image Load Failed")

    def sort_deck(self):
        # 依序排序：series → card_id
        self.deck.sort(key=sort_key)

    def get_card_count(self, series, card_id, card_type, card_level):
        return sum(1 for card in self.deck if card == (series, card_id, card_type, card_level))
    
    #圖片被點擊行為
    def show_card_info(self, series, card_id):

        def add_to_deck(series, card_id):
            card_info = self.data[series][card_id]
            self.deck.append((series, card_id, card_info['type'], card_level))
            self.sort_deck()
            update_count()
            self.deck_label.setText(f"目前牌組張數 : {len(self.deck)}")

        def remove_from_deck(series, card_id):
            card_info = self.data[series][card_id]

            # 尋找並移除卡片
            for i, card in enumerate(self.deck):
                if card == (series, card_id, card_info['type'], card_level):
                    self.deck.pop(i)
                    self.deck_label.setText(f"目前牌組張數 : {len(self.deck)}")
                    self.sort_deck()
                    update_count()
                    return


        
        # 取得卡片資料
        card_info = self.data[series][card_id]
        card_name = card_info['name']

        if card_info['type'] == "クライマックス":
            card_type = "名場面"
        elif card_info['type'] == "イベント":
            card_type = "事件"
        elif card_info['type'] == "キャラ":
            card_type = "角色"
        else:
            card_type = "???"

        if card_info['color'] == "赤":
            card_color = "紅"
        elif card_info['color'] == "青":
            card_color = "藍"
        elif card_info['color'] == "緑":
            card_color = "綠"
        else:
            card_color = card_info.get('color', '???')

        if card_info['souls'] == 0:
            card_soul = f"魂傷 : -"
        else:
            card_soul = f"魂傷 : {str(card_info['souls'])}"
        card_level = f"等級 : {card_info['level']}"
        card_cost = f"費用 : {card_info['cost']}"
        card_power = f"力量 : {card_info.get('power', '???')}"
        card_rarity = card_info.get('rarity', '???')
        card_special = f"特徵 : {card_info.get('special', '-')}"
        card_effect = card_info['effect']
        card_code = card_info['id']
        img_path = f"image/{series}/{card_id}.jpg"

        # 建立 QDialog
        dialog = QDialog(self)
        dialog.setWindowTitle("卡片詳情")
        dialog.setFixedSize(935, 500)

        # 主佈局：橫向佈局
        main_layout = QHBoxLayout(dialog)

        # ===== 左側圖片區域 =====
        left_layout = QVBoxLayout()
        img_label = QLabel()
        img_label.setFixedSize(300, 400)  # 放大圖片區域
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            if card_info['type'] == "クライマックス":
                pixmap = pixmap.transformed(QTransform().rotate(90))
            pixmap = pixmap.scaled(300, 400, Qt.KeepAspectRatio)
            img_label.setPixmap(pixmap)
        else:
            img_label.setText("圖片加載失敗")

        # 卡片數量顯示區域
        count_label = QLabel()
        count_label.setAlignment(Qt.AlignCenter)
        count_label.setStyleSheet("font-size: 18px; color: #000")
        count_label.setFixedHeight(30)

        # 更新卡片數量顯示
        def update_count():
            count = self.get_card_count(series, card_id, card_info['type'], card_level)
            count_label.setText(f"此卡數量：{count}")

        # 初次更新數量
        update_count()

        # 加入左側佈局
        left_layout.addWidget(img_label)
        left_layout.addWidget(count_label)
        main_layout.addLayout(left_layout)

        # ===== 右側資料區域 =====
        right_layout = QVBoxLayout()


        # 資料表格 (3 行 3 列)
        table = QTableWidget(4, 3)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)


        # 第一行：名稱 / 類別 / 顏色
        table.setItem(0, 0, QTableWidgetItem(card_name))
        table.setItem(0, 1, QTableWidgetItem(card_type))
        table.setItem(0, 2, QTableWidgetItem(card_color))

        # 第二行：魂傷 / 攻擊 / 稀有度
        table.setItem(1, 0, QTableWidgetItem(card_soul))
        table.setItem(1, 1, QTableWidgetItem(card_power))
        table.setItem(1, 2, QTableWidgetItem(card_rarity))

        # 第三行：等級、費用
        table.setItem(2, 0, QTableWidgetItem(card_level))
        table.setItem(2, 1, QTableWidgetItem(card_cost))
        table.setItem(2, 2, QTableWidgetItem(card_code))

        # 第四行：特徵 (橫跨三列)
        table.setItem(3, 0, QTableWidgetItem(card_special))
        table.setSpan(3, 0, 1, 3)  # 橫跨三列

        # 調整列寬
        table.setColumnWidth(0, 200)
        table.setColumnWidth(1, 200)
        table.setColumnWidth(2, 200)
        table.setFixedHeight(200)

        # ===== 效果區域 (多行文字框) =====
        effect_edit = QTextEdit()
        effect_edit.setPlainText(card_effect)
        effect_edit.setReadOnly(True)
        effect_edit.setFixedHeight(200)

        button_layout = QHBoxLayout()
        
        add_button = QPushButton("加入")
        remove_button = QPushButton("移除")
        close_button = QPushButton("關閉")

        add_button.clicked.connect(lambda: add_to_deck(series, card_id))
        remove_button.clicked.connect(lambda: remove_from_deck(series, card_id))
        close_button.clicked.connect(dialog.accept)

        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        button_layout.addWidget(close_button)

        # 加入佈局
        right_layout.addWidget(table)
        right_layout.addWidget(effect_edit)
        right_layout.addLayout(button_layout)


        # 將右側佈局加入主佈局
        main_layout.addLayout(right_layout)

        # 顯示視窗
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CardViewer()
    viewer.show()
    sys.exit(app.exec())
