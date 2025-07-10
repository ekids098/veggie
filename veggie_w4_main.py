from typing import Sequence
import streamlit as st # streamlit 是一個 Python 的開源框架，用來快速建立互動式網頁。
from veggie_w1 import apply_url_dataframe # 匯入第一週檔案中的 2.應用函式。
from veggie_w2 import unit_conversion, WeightUnit # 匯入第二週檔案中的 1.單位換算函式。
from veggie_w3 import search, FruitSearchResult # 匯入第三週檔案中的 4.整合查詢函式。
import json # 用來處理 JSON 格式的資料，例如讀取與寫入設定檔。
import re # 正規表達式模組，用來進行文字比對與格式驗證。
from pathlib import Path # 提供物件導向的檔案與路徑處理方式。
import smtplib # Python 的內建郵件傳送模組，用來透過 SMTP 協定發送 Email。
from email.mime.text import MIMEText # 建立純文字格式的 email 內容物件。
from email.mime.multipart import MIMEMultipart # 建立多格式的 email 內容物件。

# 寄信函式。
def send_email(to_email, subject, body):
    from_email = st.secrets["EMAIL_ADDRESS"]
    password = st.secrets["EMAIL_PASSWORD"]

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
    
# 設定網頁的基礎架構、主標題、副標題。
# 分頁顯示文字為「🍹濃縮蔬果汁」，內容整體區塊為置中對齊。
st.set_page_config(page_title="濃縮蔬果汁", page_icon="🍹", layout="centered")

# 1.設定頁首段落。
# 1-1.主標題（置中對齊，<h2>字體大小約 24px）。
st.markdown("<h2 style='text-align: center;'>🍹 濃縮蔬果汁</h2>", unsafe_allow_html=True)
# 1-2.副標題（置中對齊，字體大小 16px）。
st.markdown("<h4 style='text-align: center; font-size: 16px;'>推薦、計算、加通知，一鍵就得資。</h4>", unsafe_allow_html=True)
# 加入水平分隔線，分隔區塊。
st.markdown("---")

# 2.設定主題故事段落。
# 2-1.段落標題（置中對齊，<h4>字體大小約 16px）。
st.markdown("<h4 style='text-align: center;'>一、主題故事</h4>", unsafe_allow_html=True)
# 2-2.段落內文（置中對齊，字體大小為 16px，行距為 2）。
# 三引號是 Python 多行字串的寫法，行尾「兩個空格 + Enter」強制換行。
st.markdown("""
<div style='text-align: center; font-size: 16px; line-height: 2;'>
為了幫助不諳市場、生活忙碌的厝邊隔壁，  
一對熱愛科技的阿公阿嬤，和他們聰明的小狗「果價」，  
攜手打造的全新力作，一杯兼具智慧與營養的濃縮蔬果汁🍹。
</div>
""", unsafe_allow_html=True)
# 加入水平分隔線，分隔區塊。
st.markdown("---")

# 3.設定三大角色與功能介紹段落。
# 3-1.段落標題（置中對齊，<h4>字體大小約 16px）。
st.markdown("<h4 style='text-align: center;'>二、三大角色與功能介紹</h4>", unsafe_allow_html=True)

# 3-2.段落內文。
# 按鈕樣式。
st.markdown("""
<style>
div.stButton > button {
    background-color: #FF914D;          /* 溫橘底色 */
    color: white;                       /* 白色字體 */
    border: 5px solid white;            /* 白色外框 */
    border-radius: 10px;                /* 圓角 */
    padding: 8px 16px;                  /* 內邊距 */
    font-weight: 600;                   /* 字體粗細 */
    cursor: pointer;                    /* 可以點擊（滑鼠變手指）*/
    width: 100%;                        /* 寬度 */
}
div.stButton > button:hover {
    background-color: #7A9E9F;         /* 滑鼠移上變灰藍 */
}
</style>
""", unsafe_allow_html=True)

# 三大角色欄位橫向排列。
col1, col2, col3 = st.columns(3)

# 👴推薦公。
with col1:
    with st.container():
        # 角色名稱與個性。
        st.markdown("""
        <div style='background-color:#F5F3EA; padding:20px; border-radius:10px; color:black; text-align:center'>
            <h4>👴 推薦公</h4>
            <p style='font-size:16px; font-style:italic;'>* 直率乾脆、快狠準 *</p>
        </div>
        """, unsafe_allow_html=True)

        # 建立按鈕（名稱，識別碼）並置中對齊。
        st.markdown("<div style='margin-top:-40px'></div>", unsafe_allow_html=True)
        btn1_left, btn1_mid, btn1_right = st.columns([0.5, 3, 0.5])
        with btn1_mid:
            button_recommend = st.button("精選蔬果", key="recommend")

# 按按鈕後執行第一週檔案中的 2.應用函式。
if button_recommend:
    try:
        df_veg, df_fruit = apply_url_dataframe()

        # 用 tabulate 美化。
        from tabulate import tabulate

        # 動態置中函式。
        def center_align_table(table: str) -> str:
            lines = table.split("\n")
            for i, line in enumerate(lines):
                # 找出只包含 '-' 和 ':' 的那一行（即第二行）。
                if set(line.replace("|", "").strip()) <= {"-", ":"}:
                    segments = line.split("|")
                    # 對每個非空欄位加上置中格式。
                    segments = [":---:" if seg.strip() else "" for seg in segments]
                    lines[i] = "|".join(segments)
                    break
            return "\n".join(lines)

        table_veg = tabulate(df_veg, headers="keys", tablefmt="github", floatfmt=".1f", stralign="center", numalign="decimal", showindex=False)
        table_veg = center_align_table(table_veg)

        table_fruit = tabulate(df_fruit, headers="keys", tablefmt="github", floatfmt=".1f", stralign="center", numalign="decimal", showindex=False)
        table_fruit = center_align_table(table_fruit)

        # 顯示輸出畫面。
        st.success("👴 這週這五樣最讚，卡緊買，等下漲你會嘸甘啦！")
        tab1, tab2 = st.tabs(["🥬 蔬菜排行榜", "🍎 水果排行榜"])

        with tab1:
            st.markdown(table_veg, unsafe_allow_html=False)  

        with tab2:
            st.markdown(table_fruit, unsafe_allow_html=False)  

    except Exception as e:
        st.error("👴 精選蔬果載入失敗")
        with st.expander("🔧 錯誤詳情（開發者用）"):
            st.exception(e)

# 👵客製嬤。
# 第二週檔案中🍹主程式🍹函式（調整成 streamlit 適用版）。
def user_input_streamlit():

    # 功能說明（置中對齊，字體大小 16px）。
    st.markdown(
        """<h4 style='text-align: center; font-size: 16px;'>
        功能說明：輸入人數與天數 ➡️ 計算蔬菜應購買總重量（單位：公斤、台斤）。</h4>""",
        unsafe_allow_html=True
    )
    # 選擇語言。
    lang = st.selectbox("選擇語言", ["國語", "台語"])

    # 依據語言顯示提示文字。
    if lang == "國語":
        intro = "👵 裡面坐，今天幾位要喝果汁？"
        prepare = "👵 阿嬤幫你多準備，帶回去慢慢喝嘿！"
    else:
        intro = "👵 內底坐，今仔日有幾個人欲飲？"
        prepare = "👵 阿嬤幫你多準備，帶返去慢慢飲嘿！"

    # 顯示輸入畫面：執行整數輸入函式。
    st.markdown(intro)
    # 整數輸入函式。
    def check_input_streamlit(label):
        val = st.number_input(label, min_value=0, step=1)
        return val
    
    child_count = check_input_streamlit("👶 小朋友（12 歲以下）： __ 人")
    female_count = check_input_streamlit("👩 女性（12 歲以上）： __ 人")
    male_count = check_input_streamlit("👨 男性（12 歲以上）： __ 人")

    st.markdown(prepare)

    days = st.number_input("📅 想要準備幾天的份量： __ 天", min_value=1, step=1)

    # 按按鈕後執行第二週檔案中的 1.單位換算函式。
    if st.button('一鍵得資'):
        try:
            result = unit_conversion(child_count, female_count, male_count, days)
            # 顯示輸出畫面。
            st.success(f"🥬 蔬菜總共要買 {result[WeightUnit.KILOGRAM]} 公斤（約 {result[WeightUnit.TAI_JIN]} 台斤）🥬")
        except Exception as e:
            st.error("👵 秤斤秤重載入失敗")
            with st.expander("🔧 錯誤詳情（開發者用）"):
                st.exception(e)
with col2:
    with st.container():
        # 角色名稱與個性。
        st.markdown("""
        <div style='background-color:#F5F3EA; padding:20px; border-radius:10px; color:black; text-align:center'>
            <h4>👵 客製嬤</h4>
            <p style='font-size:16px; font-style:italic;'>* 內向細膩、相信數字 *</p>
        </div>
        """, unsafe_allow_html=True)

        # 建立按鈕（名稱，識別碼）並置中對齊。
        st.markdown("<div style='margin-top:-40px'></div>", unsafe_allow_html=True)
        btn2_left, btn2_mid, btn2_right = st.columns([0.5, 3, 0.5])
        with btn2_mid:
            button_weight = st.button("秤斤秤重", key="weight")

# 按按鈕後執行第二週檔案中🍹主程式🍹（調整成 streamlit 適用版）。
# 使用 session_state 控制是否持續顯示輸入頁面。
if 'show_weight_input' not in st.session_state:
    st.session_state.show_weight_input = False

if button_weight:
    st.session_state.show_weight_input = True

if st.session_state.show_weight_input:
    user_input_streamlit()

# 🐶果價。
with col3:
    with st.container():
        st.markdown("""
        <div style='background-color:#F5F3EA; padding:20px; border-radius:10px; color:black; text-align:center'>
            <h4>🐶 果價</h4>
            <p style='font-size:16px; font-style:italic;'>* 忠誠靈敏、嗅覺超準 *</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 建立按鈕（名稱，識別碼）並置中對齊。
        st.markdown("<div style='margin-top:-40px'></div>", unsafe_allow_html=True)
        btn3_left, btn3_mid, btn3_right = st.columns([0.5, 3, 0.5])
        with btn3_mid:
            button_dog = st.button("果價汪汪", key="dog")

# 顯示輸入畫面，按按鈕後執行儲存功能、查詢並寄信通知功能、每週ㄧ早上八點自動查詢功能與預覽畫面。
# 使用 session_state 控制是否持續顯示輸入頁面。
if 'show_fruit_input' not in st.session_state:
    st.session_state.show_fruit_input = False

if button_dog:
    st.session_state.show_fruit_input = True

def search_and_render_fruit_price(fruits: Sequence[str]) -> tuple[FruitSearchResult]:
    """果價搜尋並顯示於頁面，並回傳划算的水果資訊"""
    search_results = tuple(map(lambda fruit: search(fruit), fruits))
    
    # display error message
    for result in search_results:
        if result["message"] == "success":
            continue

        st.error(f"{result["fruit"]} 查詢錯誤：{result["message"]}")
        if result["errors"]:
            st.error("詳細資訊:")
            st.error("\n".join(result["errors"]))
    
    # display successful result
    success_results = tuple(filter(
        lambda result: result["message"] == "success",
        search_results,
    ))
    for result in success_results:
        fruit_info = result["data"]
        st.markdown((
            f"- **{result["fruit"]}**: "
            f"週期：{fruit_info.period}，"
            f"成交價：{fruit_info.average_price} 元，"
            f"成交價：{fruit_info.average_price} 元，"
            f"全年度平均成交價：{fruit_info.year_average_price} 元 "
        ))
    
    # display inexpensive price
    good_price_results = tuple(filter(
        lambda result: result["data"].lower_than_average,
        success_results,
    ))
    for result in good_price_results:
        st.success(f"🐶 汪！你喜歡的 {result["fruit"]} 最近便宜了汪，我幫你聞到了汪！")

    return good_price_results

if st.session_state.show_fruit_input:
    # 顯示輸入畫面。
    # 功能說明（置中對齊，字體大小 16px）。
    st.markdown(
    "<h4 style='text-align: center; font-size: 16px;'>功能說明：自訂喜愛水果清單 ➡️ 查詢水果成交價格（最近一週）➡️ 低於年度平均即寄信通知。</h4>",
    unsafe_allow_html=True
    )
    fav_fruits_input = st.text_input("🐶 請輸入水果名稱-品種（用逗號分隔）", "例如：西瓜-大西瓜, 荔枝-糯米")
    email_input = st.text_input("🐶 請輸入 Email", "")

    # 按按鈕後執行儲存功能。
    if st.button("儲存喜愛水果清單", key="save_dog"):
        fruits = [f.strip() for f in fav_fruits_input.split(",") if f.strip()]
        email = email_input.strip()

        # 簡易 email 格式驗證函式。
        # 設定 email 格式。
        def is_valid_email(email):
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            return re.match(pattern, email) is not None
        # 驗證 email 格式。
        if not fruits or not email:
            st.warning("🐶 汪！請輸入水果與 Email 汪！")
        elif not is_valid_email(email):
            st.warning("🐶 汪！Email 格式不正確，請重新輸入汪！")
        # 儲存喜愛水果清單。
        else:
            data = {
                "email": email,
                "fruits": fruits
            }
            with open("fruit_list.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            st.session_state.data = data
            st.success("🔔 喜愛水果清單儲存成功！")
            st.code(json.dumps(data, ensure_ascii=False, indent=2), language="json")
    
    # 按按鈕後執行查詢並寄信通知功能。
    if st.button("查詢並寄信通知", key="btn_notify"):
        st.session_state.search_notify = True

    # 查詢。
    if st.session_state.get("search_notify", False):
        st.markdown("🐶 果價搜尋中…")

        if not (data := st.session_state.get("data", None)):
            st.error("🐶 汪！要先儲存喜愛水果清單，才能查詢寄信！")

        elif not (good_results := search_and_render_fruit_price(data.get("fruits", tuple()))):
            st.info("🐶 沒有水果價格低於平均，暫不寄信汪～")

        else:
            try:
                body = "\n\n".join(map(
                    lambda result: (
                        f"🐶 汪！你喜歡的 {result["fruit"]} 最近便宜了汪，我幫你聞到了汪！\n"
                        f"（ 週期：{result["data"].period}，"
                        f"成交價：{result["data"].average_price} 元，"
                        f"全年度平均成交價：{result["data"].year_average_price} 元 ）"
                    ),
                    good_results,
                ))
                send_email(data['email'], "🐶 果價汪汪", body)
                st.success(f"🔔 寄信成功！降價資訊已寄給 {data['email']}：")
            except Exception as e:
                st.error(f"寄信失敗：{e}")

        st.session_state.search_notify = False

    # 顯示預覽畫面與功能。
    st.markdown("---")
    st.markdown("🍹 目前已儲存的喜愛水果清單")
    fruit_file = Path("fruit_list.json")
    if fruit_file.exists():
        try:
            with open(fruit_file, "r", encoding="utf-8") as f:
                saved_data = json.load(f)
            st.code(json.dumps(saved_data, ensure_ascii=False, indent=2), language="json")
        except Exception as e:
            st.error(f"讀取失敗：{e}")
    else:
        st.info("🍹 尚未儲存任何清單")

# 4.設定頁尾段落。
# 加入水平分隔線，分隔區塊。
st.markdown("---")
st.caption("Powered by 推薦公 👴、客製嬤 👵 與果價 🐶 。")

# 開啟網站（在終端機輸入以下兩行）：
# 安裝所有需要的套件。
# 1.pip install -r veggie/requirements.txt
# 執行網站。
# streamlit run veggie/veggie_w4_main.py
