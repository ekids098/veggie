import os
import sys
from veggie_w3 import search # 匯入第三週檔案中的 4.整合查詢函式。
import json # 用來處理 JSON 格式的資料，例如讀取與寫入設定檔。
from pathlib import Path # 提供物件導向的檔案與路徑處理方式。
import smtplib # Python 的內建郵件傳送模組，用來透過 SMTP 協定發送 Email。
from email.mime.text import MIMEText # 建立純文字格式的 email 內容物件。
from email.mime.multipart import MIMEMultipart # 建立多格式的 email 內容物件。

# 寄信函式。
def send_email(to_email, subject, body):
    from_email = "ekids098@gmail.com"        # 改成你的寄件信箱。
    password = "mkdlbzluhodtvrbh"            # 改成你的信箱應用程式密碼。

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print("🔔 寄信成功！")
    except Exception as e:
        print(f"寄信失敗：{e}")
        raise e

# 任務函式。
def task():
    try:
        # 載入已儲存的喜愛水果清單。
        base_dir = os.path.dirname(os.path.abspath(__file__))  # 加入絕對路徑
        fruit_file = Path(base_dir) / "fruit_list.json"
        if not fruit_file.exists():
            print("沒有喜愛水果清單，故無法執行。")
            return
        
        with open(fruit_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 查詢。
        print(f"👉 準備處理 {data.get('email')}，水果清單：{data.get('fruits')}")
        notify_list = []
        for fruit in data.get('fruits', []):
            try:
                result = search(fruit)
                print(f"🔍 查詢結果：{result}")  # 每種水果結果。

                if result.get("是否低於平均價") == "是":
                    line = (
                        f"🐶 汪！你喜歡的 {result['水果名稱']} 最近便宜了汪，我幫你聞到了汪！\n"
                        f"（ 週期：{result['週期']}，成交價：{result['成交價']} 元，全年度平均成交價：{result['全年度平均成交價']} 元 ）"
                    )
                    notify_list.append(line)
            except Exception as e:
                print(f"{fruit} 查詢錯誤：{e}")
        
        # 寄信通知。
        if notify_list:
            body = "\n".join(notify_list)
            send_email(data['email'], "🐶 果價汪汪", body)
            print(f"🔔 每週通知已寄給 {data['email']}！")
        else:
            print("🐶 沒有水果價格低於平均，暫不寄信汪～")

    except Exception as e:
        print(f"任務函式錯誤：{e}")

if __name__ == "__main__":
    try:
        log_file = Path(__file__).parent / "task_log.txt"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write("🟢 程式開始執行\n")
            sys.stdout = f
            sys.stderr = f
            task()
            f.write("✅ 程式執行完成\n")
    except Exception as e:
        # 這段要額外捕捉錯誤，不依賴 sys.stderr。
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"❌ 發生例外：{e}\n")