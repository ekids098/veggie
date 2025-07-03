import requests
from bs4 import BeautifulSoup
import json # 用來處理 JSON 格式的資料，例如讀取與寫入設定檔。
import re # 正規表達式模組，用來進行文字比對與格式驗證。
from selenium import webdriver # 用來控制瀏覽器自動化操作。
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 1.取得水果代碼函式。
def get_fruit_code(fruit_name):
    url = "https://www.twfood.cc/search"
    params = {"q": fruit_name} # 搜尋參數。
    try:
        try:
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status() # 檢查請求是否成功。
        except Exception as e:
            print(f"請求失敗: {e}")
            return None
    
        soup = BeautifulSoup(res.text, "html.parser")
        # 找出 div.blog-posts 裡第一個 <a> 超連結。
        link = soup.select_one("div.blog-posts a") 
        if link and "href" in link.attrs:
            href = link["href"]
            if "/fruit/" in href:
                parts = href.split("/fruit/")[1].split("/")
                fruit_code = parts[0] if len(parts) > 0 else None
                return fruit_code, href
    except Exception as e:
        print(f"取得水果代碼失敗: {e}")
        return None, None

# 2.取得水果「每週成交價」函式。
# 「每週成交價」：週期 endDay、成交價 avgPrice。
def get_fruit_price(fruit_code):
    url = "https://www.twfood.cc/api/FarmTradeSumWeeks"
    # 搜尋參數。
    params = {
        "order": "endDay asc",
        "where": {
            "itemCode": fruit_code,
            "startDay": {"gte": "2023/12/29"}
            
        }
    }

    try:
        # json.dumps()：把 Python 物件變成 JSON 字串。
        res = requests.get(url, params={"filter": json.dumps(params)})
        res.raise_for_status() # 檢查請求是否成功。
        data = res.json() # 把 JSON 字串變成 Python 物件。

        # 確認 data 是串列且不是空的。
        if not isinstance(data, list) or not data:
            print(f"資料錯誤：回傳非列表或為空")
            return None
        
        # 取最後一筆（最新的一週）。
        latest = data[-1]
        avgPrice = latest.get("avgPrice")
        period = latest["endDay"]
        return avgPrice, period
        
    except Exception as e:
        return None, str(e)

# 3.取得水果「全年度平均成交價」函式。
def get_fruit_year_price(href):
    base = "https://www.twfood.cc"
    url = base + href

    # 模擬真實瀏覽器。
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    
    # 啟動瀏覽器。
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "tspan"))
            )
        except TimeoutException:
            print("等候 tspan 超時")
            return None

        tspans = driver.find_elements(By.TAG_NAME, "tspan")
        for t in tspans:
            text = t.text
            if "全年度平均成交價" in text:
                match = re.search(r"NT\$ ?([\d.]+)", text)
                if match:
                    year_price = float(match.group(1))
                    return year_price
        return None
    finally:
        driver.quit()

# 4.整合查詢函式：內含上述三個函式。
def search(fruit_name):
    fruit_code, href = get_fruit_code(fruit_name)
    if not fruit_code or not href:
        return {"錯誤": "找不到水果代碼或網址"}

    avg_price, period = get_fruit_price(fruit_code)
    if avg_price is None:
        return {"錯誤": "找不到成交價資料"}

    year_price = get_fruit_year_price(href)
    if year_price is None:
        return {"錯誤": "找不到全年度平均成交價"}

    is_cheaper = "是" if avg_price < year_price else "否"

    return {
        "水果名稱": fruit_name,
        "週期": period,
        "成交價": avg_price,
        "全年度平均成交價": year_price,
        "是否低於平均價": is_cheaper
    }

