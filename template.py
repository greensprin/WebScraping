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

  # ===== 処理開始 =====


  # ===== 処理終了 =====

  # windowを閉じる
  driver.close()
  driver.quit()