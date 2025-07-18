# 🍹 濃縮蔬果汁

這是一個整合蔬果推薦、購買量估算，以及價格通知功能的互動式網頁，  

希望即使是生活再忙碌的使用者，也能聰明地選購蔬果，做出更健康、有效率的購買決策。

---

## 主要功能

- **推薦公**：使用爬蟲抓取「當季好蔬果」網站資料 → 列出推薦排行榜前五名的「精選蔬果」。  
- **客製嬤**：使用者輸入人數與天數 → 計算蔬菜應購買總重量（單位：公斤、台斤）。  
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
├── veggie_w3.py              # 果價：「果價汪汪」爬蟲與比價功能模組。
├── veggie_w4_main.py         # Streamlit 網頁主程式：整合 w1, w2, w3 並新增設定喜愛水果清單與寄信通知功能。
├── veggie_w4_schedule.py     # 「自動寄信通知」功能：請使用外部排程器定時執行。
├── fruit_list.json           # 喜愛水果清單。
├── 📁.streamlit/
  └── secrets.toml.tpl        # 寄信設定範本（Email 帳號與應用程式密碼）。
├── task_log.txt              # 排程執行紀錄與錯誤日誌。
├── requirements.txt          # 環境需求。
└── README.md                 # 說明文件。
```

### 備註

- `veggie_w4_main.py` 為 Streamlit 網頁主程式，建議從此檔案啟動網站。
- 若需「自動寄信通知」功能，請使用外部排程器定時執行 `veggie_w4_schedule.py`。
- `.streamlit/secrets.toml.tpl` 為寄信設定範本，請複製為 .streamlit/secrets.toml 並填入帳號與應用程式密碼。

---

## ▶️ 執行方式

1. 安裝所需套件（僅首次執行需要）：

   ```bash
   pip install -r requirements.txt
   ```

2. 啟動網頁主程式：

   ```bash
   streamlit run veggie_w4_main.py
   ```

3. 「自動寄信通知」功能：
- 使用 Windows 內建工具「 工作排程器 Windows Task Scheduler 」。
- 定時執行下列指令發送水果價格通知信。

   ```bash
   veggie_w4_schedule.py
    ```
