from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from debug_flag import debugging

class Chrome:
    driver = None

    def __init__(self):
        #ブラウザのオプション
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")

        #デバッグ用にブラウザを非表示で起動する
        if not debugging:
            options.add_argument("--headless")

        #ドライバを自動更新
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

        #ブラウザ起動
        self.driver.get("https://www.google.com")

    def close(self):
        #ブラウザを閉じる
        self.driver.quit()