import atexit
from chrome import Chrome
from paiza import Paiza
from ChatGPTへの共有文章 import ChatGPTへの共有文章
from デバッグモード管理 import デバッグモードオン

#デバッグ用
if デバッグモードオン:
	url一覧 = [
		'https://paiza.jp/career/job_offers/36987',
		'https://paiza.jp/career/job_offers/28880',
		'https://paiza.jp/career/job_offers/17518',
	]
	ChatGPTへの共有文章(url一覧)
	exit()

chrome = Chrome()
#プログラム正常終了時に自動実行
atexit.register(chrome.close)
paiza = Paiza(chrome.driver)
ChatGPTへの共有文章(paiza.url一覧)
