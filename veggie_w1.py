import requests
from bs4 import BeautifulSoup
import pandas as pd # pandas 的 DataFrame 可以將一筆筆資料以表格形式組織起來，方便以欄與列的結構來操作和分析資料。
from tabulate import tabulate # tabulate 可以調整原終端機輸出的表格畫面，變得更整齊易讀。
from wcwidth import wcswidth # wcswidth（text）會回傳整段文字在終端機中的實際顯示寬度。英文字母、數字：寬度 1，中文：寬度 2。


def scrape_tw_food_top5(url) -> list[dict]:
    """1.爬蟲函式：從網頁（參數）抓取推薦前五名的品項名稱、批發價、零售價。"""
    # 先設定 User-Agent：隱藏爬蟲目的的假身分，讓網站以為你只是用你的設備（假身分）在上網。
    # 設備：Windows 10 / 64 位元作業系統 / Chrome 瀏覽器 v85。
    try:
        # 使用假身分自我介紹，取得網頁內容。
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/85.0.4183.83 Safari/537.36'
            ),
        }
        res = requests.get(url, headers=headers) 
    except Exception as e:
        print(f"爬取失敗：{url} → {e}")
        return list()

    # 尋找網頁全部品項，即推薦排行榜前五名的各品項資料（名稱、批發價、零售價等），並以串列 list 存放。
    # 每個品項的大結構為<div class="col-xs-6 col-sm-6 col-md-12 vege_price">。
    food_top5 = BeautifulSoup(res.text, 'html.parser').find_all('div', class_='vege_price') # 放寬匹配條件降低尋找失誤。

    # 各品項處理。
    items_data = []
    for item in food_top5:
        # 1.品項名稱。
        # 若處理前 text = ' 推薦No: 1 菜豆-青色 '，處理後 text = '菜豆-青色'。                                       
        name = item.find('a').text.strip().split('推薦No:')[1].split()[1]
        # 2.所有價格資料。
        prices = item.find_all('span', class_='text-price')
        # 2-1.本週平均批發價（元/台斤）。
        avg_wholesale_jin = float(prices[1].text.strip())
        # 2-2.預估零售價（元/台斤）。
        est_retail_jin = float(prices[3].text.strip())

        # 存入字典串列 list。
        items_data.append({
            '名稱': name,
            '平均批發價(元/台斤)': avg_wholesale_jin,
            '預估零售價(元/台斤)': est_retail_jin,
        })

    # 回傳字典串列 list。
    return items_data


def apply_url_dataframe():
    """2.應用函式：將蔬菜與水果分頁丟進爬蟲函式，並建立 DataFrame。"""

    # 蔬菜前五名分頁網址。
    url_veg = 'https://www.twfood.cc/vege'
    # 水果前五名分頁網址。
    url_fruit = 'https://www.twfood.cc/fruit'
    
    # 丟進爬蟲函式取得字典串列 list。
    list_veg = scrape_tw_food_top5(url_veg)
    list_fruit = scrape_tw_food_top5(url_fruit)

    # 建立 DataFrame。
    df_veg = pd.DataFrame(list_veg)
    df_fruit = pd.DataFrame(list_fruit)

    for df in (df_veg, df_fruit):
        # 新增「合理價格區間」欄位，並針對每一品項計算「合理價格區間」= 本週平均批發價 + (預估零售價-本週平均批發價) × [25%, 75%]。
        df['合理價格區間'] = df.apply(
            lambda row: f"{(row['平均批發價(元/台斤)'] + (row['預估零售價(元/台斤)'] - row['平均批發價(元/台斤)'])*0.25):.1f}"
                        + " - " + 
                        f"{(row['平均批發價(元/台斤)'] + (row['預估零售價(元/台斤)'] - row['平均批發價(元/台斤)'])*0.75):.1f}", # .1f 代表顯示到小數點後一位。
            axis=1
        )
        
        # 簡化欄位名稱。
        df.rename(columns={
            '名稱': '名稱',
            '平均批發價(元/台斤)': '平均批發價',
            '預估零售價(元/台斤)': '預估零售價',
            '合理價格區間': '合理價區間'
        }, inplace=True)

        # 寬度調整函式：依照目標寬度參數 width 補齊文字參數 text 寬度。
        def pad_text(text, width):
            pad = width - wcswidth(text)
            return text + ' ' * pad if pad > 0 else text
        # 將 DataFrame 各欄位丟進寬度調整函式，統一顯示寬度（自訂 10 寬度）。
        df.columns = [pad_text(col, 10) for col in df.columns]

    return df_veg, df_fruit


# 3.輸出：執行應用函式後，設定表格的美化格式並輸出。
df_veg, df_fruit = apply_url_dataframe()

print("蔬菜排行榜前五名(元/台斤):")
table_veg = tabulate(df_veg, headers='keys', tablefmt='github', floatfmt=".1f", stralign="center", numalign="decimal", showindex=False)
table_veg = table_veg.replace(
    "|--------------|--------------|--------------|--------------|",
    "|:------------:|:------------:|:------------:|:------------:|"
)
print(table_veg)

print("\n水果排行榜前五名(元/台斤):")
table_fruit = tabulate(df_fruit, headers='keys', tablefmt='github', floatfmt=".1f", stralign="center", numalign="decimal", showindex=False)
table_fruit = table_fruit.replace(
    "|--------------|--------------|--------------|--------------|",
    "|:------------:|:------------:|:------------:|:------------:|"
)
print(table_fruit)
