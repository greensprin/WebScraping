# coding: UTF-8

import configparser
from selenium import webdriver
import time
import random

# 設定値取得
config = configparser.ConfigParser()
config.read("config.ini")

# 待ち時間設定
wait_time_min = float(config["common"]["wait_time_min"])
wait_time_max = float(config["common"]["wait_time_max"])

# アクセス待ち時間
def TimeWait():
  sec = random.uniform(wait_time_min, wait_time_max)
  print("wait {} sec".format(sec))
  time.sleep(sec)

def SetOptions(options):
  # ブラウザ非表示設定
  if (int(config["browser"]["headless"]) == 1):
    options.add_argument("--headless")

  # Proxy設定 (pass)
  # http_proxy = config["browser"]["http_proxy"]
  # options.add_argument("--proxy-server={}".format(http_proxy)) # {proxy-server}:{port}
  # proxy_auth = config["browser"]["proxy_auth"]
  # options.add_argument("--proxy-auth={}".format(proxy_auth)) # {userid}:{password}

  return options

def SetDriver():
  # webdriver path設定
  web_driver_path = config["browser"]["webdriver_path"]

  # driver設定 (browser = chrome固定)
  driver = ""
  set_browser = config["browser"]["browser"]

  if   (set_browser == "chrome"):
    # options取得
    options = webdriver.ChromeOptions()
    # option設定
    options = SetOptions(options)
    # driver 取得
    driver = webdriver.Chrome(options=options, executable_path=web_driver_path)
  elif (set_browser == "firefox"): # 動作確認未実施
    # options取得
    options = webdriver.firefox.options()
    # option設定
    options = SetOptions(options)
    # driver 取得
    driver = webdriver.Firefox(options=options, executable_path=web_driver_path)
    print("{} not support".format(set_browser))
    quit()
  else:
    print("{} not support".format(set_browser))
    quit()

  return driver
