from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import html
from デバッグモード管理 import デバッグモードオン

class Paiza:
    driver = None
    ログインURL = "login"
    マイページ="mypage"
    スカウト = "scout"
    URL = {
        ログインURL:"https://paiza.jp/sign_in",
        マイページ:"https://paiza.jp/career/mypage",
        スカウト:"https://paiza.jp/messages",
    }
    url一覧 = []

    def __init__(self, driver):
        self.driver = driver
        self.ログイン()
        self.スカウト画面へ移動()
        self.url一覧設定()

    def ログイン(self):
        #ログイン画面
        self.driver.get(self.URL[self.ログインURL])

        #メールアドレス入力
        self.入力要素へ入力(
            "input[type='email']",
            "xxxxx@yyy.com",
            "メールアドレス"
        )

        #パスワード入力
        self.入力要素へ入力(
            "input[type='password']",
            "xxxxxxxx",
            "パスワード"
        )

        #ログインボタンクリック
        self.ボタンクリック(
            "button.s-cv-button.s-cv-button--primary.s-cv-button--small",
            "ログイン"
        )

        #遷移確認
        self.遷移確認(self.URL[self.ログインURL])

    def 入力要素へ入力(self, 検索ワード, 入力ワード, 対象要素名):
        #入力要素を取得
        入力要素 = self.driver.find_element(By.CSS_SELECTOR, 検索ワード)
        #存在確認
        if not 入力要素:
            print(対象要素名 + "入力要素が見つかりませんでした")
            exit()
        #入力要素に入力
        入力要素.send_keys(入力ワード)

    def ボタンクリック(self, 検索ワード, 対象要素名):
        #ボタン取得
        ボタン要素 = self.driver.find_element(By.CSS_SELECTOR, 検索ワード)
        #存在確認
        if not ボタン要素:
            print(対象要素名 + "ボタンが見つかりませんでした")
            exit()
        #ボタンをクリック
        ボタン要素.click()

    def 遷移確認(self, 遷移先URL):
        #遷移するまで最大10秒待機
        try:
            WebDriverWait(self.driver, 10).until(lambda d: d.current_url != 遷移先URL)
        except:
            print("ページ遷移失敗")
            exit()

    def スカウト画面へ移動(self):
        #スカウト画面
        self.driver.get(self.URL[self.スカウト])
        #遷移確認
        self.遷移確認(self.URL[self.マイページ])

    def url一覧設定(self):
        #スカウト一覧取得
        li要素 = self.スカウト一覧取得()
        #対象スカウトの最大番号取得
        対象スカウト番号の最大値 = self.対象スカウト番号の最大値取得(li要素)
        #デバッグ用に数値固定
        if デバッグモードオン:
            対象スカウト番号の最大値 = 2

        for スカウト番号 in range(対象スカウト番号の最大値 + 1):
            #一番下の未読スカウトをクリック
            li要素[スカウト番号].click()
            #クリックして表示されるのを待ってからurlを取得
            対象url = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.p-messages-offer-box__title"))
            ).get_attribute("href")
            #取得したurlをリストへ追加
            self.url一覧.append(対象url)

    def スクロール(self, スクロール対象):
        #移動前のスクロール位置
        スクロール前 = self.driver.execute_script("return arguments[0].scrollTop;", スクロール対象)
        #移動が発生するまでループ
        while(スクロール前 == self.driver.execute_script("return arguments[0].scrollTop;", スクロール対象)):
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", スクロール対象)

    def スカウト一覧取得(self):
        #スクロール対象取得
        スクロール対象 = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.p-messages-scrollable-frame")
            )
        )
        #スカウト総数が表示されるまで待つ
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "span.p-messages-scout-messages__status-count-num").text != "0"
        )
        #スカウト総数取得
        スカウト数 = int(
            self.driver.find_element(
                By.CSS_SELECTOR, "span.p-messages-scout-messages__status-count-num"
            ).text
        )
        #スカウト一覧
        li要素一覧 = []
        while(len(li要素一覧) < スカウト数):
            #スクロール開始
            self.スクロール(スクロール対象)
            #スカウト一覧取得
            li要素一覧 = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, "li.p-messages-message-card[data-analytics-class='MessageCard']")
                )
            )
        return li要素一覧
    
    def 対象スカウト番号の最大値取得(self, li要素一覧):
        for li要素 in reversed(li要素一覧):
            analytics_info = li要素.get_attribute("data-analytics-info")
            json_str = html.unescape(analytics_info)
            data = json.loads(json_str)
            if data.get("read_flag") == 0:
                return data.get("index")
        return len(li要素一覧) - 1
