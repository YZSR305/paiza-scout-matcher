import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import atexit
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import html
from chrome import Chrome
from paiza import Paiza
from chatGPT import ChatGPT

chrome = Chrome()
#プログラム正常終了時に自動実行
atexit.register(chrome.close)
paiza = Paiza(chrome.driver)
chatGPT = ChatGPT(chrome.driver, paiza.url_list)
