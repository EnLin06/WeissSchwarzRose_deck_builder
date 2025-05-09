# WeissSchwarzRose_deck_builder

一個基於 PyQt5 的 Weiß Schwarz Rose 牌組編輯器，支援卡片篩選、圖片顯示與牌組匯出功能。

## 功能
- 系列選擇與切換
- 卡片類型、等級、名稱、效果篩選
- 卡圖顯示與縮放
- 牌組匯出為圖片

## 安裝
- Link : https://drive.google.com/file/d/1Qn9jmCfiR6e1B5H5b7p1YxkmRTUWOzi_/view?usp=sharing
- 在雲端硬碟上的是一個zip檔，執行其中的viewer_V2.exe即可

## 檔案介紹
- /json 底下的json檔案 : 從官方網站爬取的卡片詳細資料
- /images 下的zip檔案 : 從官方網站爬取的卡圖資料
- databuild.py、download_img.py : 爬蟲程式，製作卡片詳細資料的json檔案和下載卡圖
- deck_creater.py : 把牌組資料匯出成圖片
- viewer_V2.py : 主程式，使用者介面本體

## 版權聲明

本專案所使用的所有卡片圖像與數據資料，其版權均屬於 **Bushiroad (武士道)** 所有。  
本專案僅作為個人學習、非營利用途，  
無意侵犯任何版權或商標權，亦不對原版權方之產品構成替代或競爭。

- 卡片圖像來源：官方 Weiß Schwarz Rose卡片資源 (https://ws-rose.com/cardlist/)
- 卡片數據資料來源：同上
- 本專案中的所有圖片僅供學習與測試用途，不得用於商業用途。
