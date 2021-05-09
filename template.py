# coding: UTF-8

import os
import sys
import re

# local
sys.path.append(os.pardir)
import scraping_util as scr_util

if __name__ == "__main__":
  # driver設定
  driver = scr_util.SetDriver()

  # url設定
  target_url = ""
  print("access url:{}".format(target_url))

  # webアクセス
  driver.get(target_url)
  scr_util.TimeWait()

  # ===== 処理開始 =====


  # ===== 処理終了 =====

  # windowを閉じる
  driver.close()
  driver.quit()