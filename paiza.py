from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import html
from debug_flag import debugging

class Paiza:
    driver = None
    LOGIN = "login"
    MYPAGE="mypage"
    SCOUT = "scout"
    URL = {
        LOGIN:"https://paiza.jp/sign_in",
        MYPAGE:"https://paiza.jp/career/mypage",
        SCOUT:"https://paiza.jp/messages",
    }
    url_list = []

    def __init__(self, driver):
        self.driver = driver
        self.login()
        self.go_to_scout_screen()
        self.set_url_list()

    def login(self):
        #ログイン画面
        self.driver.get(self.URL[self.LOGIN])

        #メールアドレス入力
        self.input_to_input_element(
            "input[type='email'][placeholder='メールアドレス']",
            "非公開",
            "メールアドレス"
        )

        #パスワード入力
        self.input_to_input_element(
            "input[type='password'][placeholder='パスワード']",
            "非公開",
            "パスワード"
        )

        #ログインボタンクリック
        self.button_click(
            "button.s-cv-button.s-cv-button--primary.s-cv-button--small",
            "ログイン"
        )

        #遷移確認
        self.confirm_transition(self.URL[self.LOGIN])

    def input_to_input_element(self, search_word, input_word, target_element_name):
        #入力要素を取得
        input_element = self.driver.find_element(By.CSS_SELECTOR, search_word)
        #存在確認
        if not input_element:
            print(target_element_name + "入力要素が見つかりませんでした")
            exit()
        #メールアドレス入力要素に入力
        input_element.send_keys(input_word)

    def button_click(self, search_word, target_element_name):
        #ボタン取得
        button_element = self.driver.find_element(By.CSS_SELECTOR, search_word)
        #存在確認
        if not button_element:
            print(target_element_name + "ボタンが見つかりませんでした")
            exit()
        #ボタンをクリック
        button_element.click()

    def confirm_transition(self, transition_source_URL):
        #遷移するまで最大10秒待機
        try:
            WebDriverWait(self.driver, 10).until(lambda d: d.current_url != transition_source_URL)
        except:
            print("ページ遷移失敗")
            exit()

    def go_to_scout_screen(self):
        #スカウト画面
        self.driver.get(self.URL[self.SCOUT])
        #遷移確認
        self.confirm_transition(self.URL[self.MYPAGE])

    def set_url_list(self):
        #スカウト一覧取得
        li_elements = self.get_scouts_list()
        #対象スカウトの最大番号取得
        maximum_number_of_target_scouts = self.maximum_number_of_target_scouts(li_elements)
        #デバッグ用に数値固定
        if debugging:
            maximum_number_of_target_scouts = 2

        for number in range(maximum_number_of_target_scouts + 1):
            #一番下の未読スカウトをクリック
            li_elements[number].click()
            #クリックして表示されるのを待ってからurlを取得
            target_url = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.p-messages-offer-box__title"))
            ).get_attribute("href")
            #取得したurlをリストへ追加
            self.url_list.append(target_url)

    def scroll(self, scroll_target):
        #移動前のスクロール位置
        before_change = self.driver.execute_script("return arguments[0].scrollTop;", scroll_target)
        #移動が発生するまでループ
        while(before_change == self.driver.execute_script("return arguments[0].scrollTop;", scroll_target)):
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll_target)

    def get_scouts_list(self):
        #スクロール対象取得
        scroll_target = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.p-messages-scrollable-frame")
            )
        )
        #スカウト総数が表示されるまで待つ
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "span.p-messages-scout-messages__status-count-num").text != "0"
        )
        #スカウト総数取得
        total_scouts = int(
            self.driver.find_element(
                By.CSS_SELECTOR, "span.p-messages-scout-messages__status-count-num"
            ).text
        )
        #スカウト一覧
        li_elements = []
        while(len(li_elements) < total_scouts):
            #スクロール開始
            self.scroll(scroll_target)
            #スカウト一覧取得
            li_elements = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "li.p-messages-message-card[data-analytics-class='MessageCard']")
                )
            )
        return li_elements
    
    def maximum_number_of_target_scouts(self, li_elements):
        for li_element in reversed(li_elements):
            analytics_info = li_element.get_attribute("data-analytics-info")
            json_str = html.unescape(analytics_info)
            data = json.loads(json_str)
            if data.get("read_flag") == 0:
                return data.get("index")
        return len(li_elements) - 1