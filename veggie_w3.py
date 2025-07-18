from typing import Optional, List
from dataclasses import dataclass
import traceback
import requests
from bs4 import BeautifulSoup
import json # 用來處理 JSON 格式的資料，例如讀取與寫入設定檔。
import re # 正規表達式模組，用來進行文字比對與格式驗證。
from selenium import webdriver # 用來控制瀏覽器自動化操作。
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


@dataclass
class FruitInfo:
    period: str
    average_price: float
    year_average_price: float
    lower_than_average: bool

@dataclass
class FruitSearchResult:
    fruit: str
    message: str
    data: Optional[FruitInfo] = None
    errors: Optional[list[str]] = None

class FruitSearchException(Exception):
    def __init__(
            self,
            message: str,
            exc_stack: Optional[List[str]] = None
        ):
        super().__init__(message)
        self.message = message
        self.exc_stack = exc_stack


def get_fruit_code(fruit_name):
    """
    取得水果代碼。
    """
    url = "https://www.twfood.cc/search"
    params = {"q": fruit_name}

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
    except Exception as e:
        raise FruitSearchException(
            "爬取水果代碼失敗",
            exc_stack=traceback.format_exception(e),
        )

    try:
        soup = BeautifulSoup(res.text, "html.parser")
        # 找出 div.blog-posts 裡第一個 <a> 超連結。
        link = soup.select_one("div.blog-posts a")
    except Exception as e:
        raise FruitSearchException(
            "解析水果代碼失敗",
            exc_stack=traceback.format_exception(e),
        )
    
    if not (link and "href" in link.attrs):
        raise FruitSearchException("Target element not found")

    if "/fruit/" not in (href := link.get("href")):
        raise FruitSearchException("Target element not found")
    
    parts = href.split("/fruit/")[1].split("/")
    fruit_code = parts[0] if len(parts) > 0 else None

    return fruit_code, href


def get_fruit_price(fruit_code):
    """
    取得水果「每週成交價」。
    「每週成交價」：週期 endDay、成交價 avgPrice。
    """
    url = "https://www.twfood.cc/api/FarmTradeSumWeeks"
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
    except Exception as e:
        raise FruitSearchException(
            "爬取每週成交價失敗",
            exc_stack=traceback.format_exception(e),
        )
    
    # 確認 data 是串列且不是空的。
    if not isinstance(data, list) or not data:
        raise FruitSearchException("資料錯誤：回傳非串列或為空")
    
    # 取最後一筆（最新的一週）。
    latest = data[-1]
    avg_price = latest.get("avgPrice")
    period = latest.get("endDay")

    if not avg_price or not period:
        raise FruitSearchException("Target element not found")

    return avg_price, period


def get_fruit_year_price(href: str) -> float:
    """
    取得水果「全年度平均成交價」。
    """
    base = "https://www.twfood.cc"
    url = base + href

    # 模擬真實瀏覽器。
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    
    # 啟動瀏覽器。
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tspan"))
        )

        target_spans = filter(
            lambda span: "全年度平均成交價" in span.text,
            driver.find_elements(By.TAG_NAME, "tspan"),
        )
        
        target_texts = list(map(
            lambda span: span.text,
            target_spans,
        ))
    except TimeoutException:
        raise FruitSearchException("Timeout when scraping tspan")
    except Exception as e:
        raise FruitSearchException(
            "Error in scraping fruit year price",
            exc_stack=traceback.format_exception(e),
        )
    finally:
        driver.quit()

    if not target_texts:
        raise FruitSearchException("Tspan element not found")

    if not (match := re.search(r"NT\$ ?([\d.]+)", target_texts[0])):
        raise FruitSearchException("Tspan pricing not found")
    
    return float(match.group(1))


def search(fruit_name: str) -> FruitSearchResult:
    """整合查詢函式：內含上述三個函式。"""
    try:
        fruit_code, href = get_fruit_code(fruit_name)
        avg_price, period = get_fruit_price(fruit_code)
        year_price = get_fruit_year_price(href)

        fruit_info = FruitInfo(
            period=period,
            average_price=avg_price,
            year_average_price=year_price,
            lower_than_average=year_price > avg_price
        )

        return FruitSearchResult(
            fruit = fruit_name,
            message = "success",
            data = fruit_info
        )
    except FruitSearchException as e:
        return FruitSearchResult(
            fruit=fruit_name,
            message=e.message,
            errors=e.exc_stack
        )
