from enum import StrEnum


class Category(StrEnum):
    CHILD = 'child'
    MALE = 'male'
    FEMALE = 'female'

class WeightUnit(StrEnum):
    TAI_JIN = '台斤'
    KILOGRAM = '公斤'


def unit_conversion(child_count: int, female_count: int, male_count: int, days: int):
    """1.單位換算函式：計算各類人數的應攝取蔬菜總量（公克），換算成蔬菜的應購買總量（公斤、台斤）。"""
    # 四個參數：12 歲以下兒童人數 child_count 、12歲以上女性人數 female_count 、12歲以上男性人數 male_count 及單次須購買的蔬菜份量天數 days 。
    # 設定字典：每人每日應攝取蔬菜量，每份蔬菜 100 克。
    unit_daily_grams = {
        Category.CHILD: 3 * 100,   # 300 克。
        Category.FEMALE: 4 * 100,  # 400 克。
        Category.MALE: 5 * 100     # 500 克。
    }

    # 使用字典，計算各類人數的應攝取蔬菜總量（公克）。
    # 各類人數的應攝取蔬菜總量 = 各類人數的每日總應攝取蔬菜量 x 單次須購買的蔬菜份量天數。
    total_days_grams = (
        child_count * unit_daily_grams[Category.CHILD] +
        female_count * unit_daily_grams[Category.FEMALE] +
        male_count * unit_daily_grams[Category.MALE]
    ) * days

    # 將公克換算成公斤與台斤，每 600 公克等於 1 台斤。
    # 台斤的英文是 Taiwanese catty 或 Taiwan catty。
    kilogram = total_days_grams / 1000
    Taiwan_catty = total_days_grams / 600

    # 回傳換算後的蔬菜應購買總量（公斤、台斤），四捨五入到指定的小數第 2 位。
    # round(number, num)：將數值 number 四捨五入到指定的小數位數 num 。
    return {
        WeightUnit.KILOGRAM: round(kilogram, 2),
        WeightUnit.TAI_JIN: round(Taiwan_catty, 2)
    }


# 🍹主程式🍹。
def user_input():
    """2.使用者輸入函式：先執行 2.確認輸入函式 ，讓使用者輸入人數與天數後，再執行 1.單位換算函式 並輸出（見上方）。"""
    
    print('👵 內底坐，今仔日有幾個人欲飲？')
    print('（裡面坐，今天幾位要喝果汁？）\n')


    def check_input(prompt):
        """3.確認輸入函式：使用者須輸入整數數字，並且不含文字、小數點、符號等，才能正確轉換成整數，否則須重新輸入。"""
        # prompt 代表輸入的提示文字字串。
        while True:
            user_input = input(prompt).strip()

            # ❌空字串。
            if user_input == "":
                print('\n❌ 請寫個數字嘿，毋通空白啦！')
                continue

            # ✅整數。
            if user_input.isdigit():
                return int(user_input)

            # ❌小數點。
            elif "." in user_input:
                print('\n❌ 阿嬤不會算啦～寫整數就好！')

            # ❌含有單位。
            elif any(unit in user_input for unit in ["人", "天"]):
                print('\n❌ 寫數字就好，阿嬤知道單位！')

            # ❌其他文字、特殊符號等。
            else:
                print('\n❌ 阿嬤看不懂這是什麼，寫數字（像 1、2、3）就好！')

            print('\n👵 再寫一次嘿～\n')

    
    # 4.輸入：執行確認輸入函式，讓使用者依序輸入。
    child_count = check_input('👶 小朋友（12 歲以下）： __ 人（請輸入整數數字）')
    female_count = check_input('👩 女性（12 歲以上）： __ 人（請輸入整數數字）')
    male_count = check_input('👨 男性（12 歲以上）： __ 人（請輸入整數數字）')

    print('\n👵 阿嬤幫你多準備，帶返去慢慢飲嘿！')
    print('（阿嬤幫你多準備，帶回去慢慢喝嘿！）\n')

    days = check_input('📅 想要準備幾天的份量： __ 天（請輸入整數數字）')
    print()

    
    # 5.輸出：執行單位換算函式，輸出蔬菜購買總量（公斤、台斤）。
    input('🍹 按 Enter 一鍵得資🍹')
    result = unit_conversion(child_count, female_count, male_count, days)
    print(f"🍹 蔬菜總共要買 {result['公斤']} 公斤（約 {result['台斤']} 台斤）🍹")
