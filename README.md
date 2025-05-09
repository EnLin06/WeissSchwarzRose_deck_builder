# WeissSchwarzRose_deck_builder

一個基於 PyQt5 的 Weiß Schwarz Rose 牌組編輯器，支援卡片篩選、卡圖顯示與牌組圖片匯出功能。

## 功能
- 系列選擇與切換
- 卡片類型、等級、名稱、效果篩選
- 卡圖顯示與縮放
- 牌組匯出為圖片

## 安裝
對於沒有python環境，想直接使用現成.exe的使用者 : 
- Link : https://drive.google.com/file/d/1Qn9jmCfiR6e1B5H5b7p1YxkmRTUWOzi_/view?usp=sharing
- 在雲端硬碟上的是一個zip檔，解壓縮後執行其中的viewer_V2.exe即可

對於有python環境，想編輯或檢視程式的使用者 : 
- 請下載 viewer_V2.py 、 deck_creater.py 、 databuild.py 、 download_img.py 四個檔案 和 json、image資料夾，其中， databuild.py 和 download_img.py 為抓取資料用的程式，並不影響主程式的運行
- 請把image資料夾下的檔案解壓縮
- 確保你的文件結構像這樣 :

  /WS-Card-Viewer/
  
  ├── json/            # JSON 資料庫
  
  ├── image/           # 卡片圖片
  
  ├── viewer_V2.py
  
  ├── deck_creater.py
  
  ├── databuild.py
  
  └── download_img.py



## 檔案介紹
- /json 底下的json檔案 : 從官方網站爬取的卡片詳細資料
- /images 下的zip檔案 : 從官方網站爬取的卡圖資料
- databuild.py、download_img.py : 爬蟲程式，製作卡片詳細資料的json檔案和下載卡圖
- deck_creater.py : 把牌組資料匯出成圖片
- viewer_V2.py : 主程式，使用者介面本體

## 未來更新
目前有些功能尚未實作，將於未來進行更新 (我很閒的時候W) ，包括
- 動態更新 JSON 數據庫
- 卡片詳情視窗優化 (如卡圖縮放)
- 牌組匯出為 PDF

關於新系列 / 商品推出時如何更新卡表 : 

對於有python、requests、bs4環境的使用者，請在和viewer_V2.py同一資料夾中執行 databuild.py，待程式執行完畢後再執行 download_img.py 爬取卡圖

## 版權聲明

本專案所使用的所有卡片圖像與數據資料，其版權均屬於 **Bushiroad (武士道)** 所有。  
本專案僅作為個人學習、非營利用途，  
無意侵犯任何版權或商標權，亦不對原版權方之產品構成替代或競爭。
此外，還請多使用官方的DeckLog系統 (https://decklog-en.bushiroad.com/)

- 卡片圖像來源：官方 Weiß Schwarz Rose卡片資源 (https://ws-rose.com/cardlist/)
- 卡片數據資料來源：同上
- 本專案中的所有圖片僅供學習與測試用途，不得用於商業用途。

如果您認為這些內容侵犯了您的版權，請聯絡 [jhihen@gmail.com]，我將馬上刪除任何親權內容。
If you believe that this project infringes your copyright, please contact me immediately at [jhihen@gmail.com].
