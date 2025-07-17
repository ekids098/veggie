# 🍹 濃縮蔬果汁

這是一個整合蔬果推薦、購買量估算，以及價格通知功能的互動式網頁，  

希望即使是生活再忙碌的使用者，也能聰明地選購蔬果，做出更健康、有效率的購買決策。

---

## 主要功能

- **推薦公**：爬蟲「當季好蔬果」網站資料 → 列出推薦排行榜前五名的「精選蔬果」。  
- **客製嬤**：使用者輸入人數與天數 → 換算蔬菜應購買總重量（單位：公斤、台斤）。  
- **果價**：使用者自訂喜愛水果清單 → 當成交價格低於年度平均即寄信通知。

---

## 環境需求

- Python 3.11 以上  
- 安裝套件（可使用 requirements.txt）：

```bash
pip install -r requirements.txt
```

---

## 📁資料結構說明

```
📁veggie/
├── veggie_w1.py              # 推薦公：「精選蔬果」功能模組。
├── veggie_w2.py              # 客製嬤：「秤斤秤重」功能模組。
├── veggie_w3.py              # 果價：「果價汪汪」爬蟲與比較水果價格功能模組。
├── veggie_w4_main.py         # Streamlit 網頁主程式：整合 w1, w2, w3 並新增設定喜愛水果清單、發送 Email 通知功能。
├── veggie_w4_schedule.py     # 排程執行 Email 通知功能：須使用外部排程器定時執行。
├── fruit_list.json           # 喜愛水果清單。
├── 📁.streamlit/
  └── secrets.toml            # 寄信用的 Email 帳號與應用程式密碼。
├── task_log.txt              # 排程執行狀態與錯誤日誌記錄檔。
├── requirements.txt          # 環境需求。
└── README.md                 # 說明文件。
```

### 備註

- `veggie_w4_main.py` 為 Streamlit 網頁主程式，建議從此檔案啟動網站。
- 若想實現「自動通知」功能，請使用外部排程器定時執行 `veggie_w4_schedule.py`。
- `.streamlit/secrets.toml` 應填入寄信用帳密（建議使用 Gmail 應用程式密碼），請勿上傳公開。

---

## ▶️ 執行方式

1. 安裝所需套件（僅第一次需要）：

   ```bash
   pip install -r requirements.txt
   ```

2. 啟動網頁主程式：

   ```bash
   streamlit run veggie_w4_main.py
   ```

3. 若想啟用排程執行 Email 通知功能：

   ```bash
   可使用 Windwos 內建工具「工作排程器 Windows Task Scheduler」，並定時執行 `veggie_w4_schedule.py`，自動發送水果價格通知信件。
    ```
