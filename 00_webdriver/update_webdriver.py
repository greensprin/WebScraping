# coding: UTF-8

'''
参考サイト: http://blog.sbfm.jp/archives/182
chromedriver url: https://chromedriver.chromium.org/downloads

webdriverのバージョンとchromeのバージョンを確認し、
古い物になっていたら、webdriverをupdateしてくれる

'''

import os
import re
import zipfile
import urllib.request
from lxml import html

def GetChromeVersion():
  # chrome versionをフォルダ名から取得
  chrome_install_dir = r"C:\Program Files (x86)\Google\Chrome\Application"
  files = os.listdir(chrome_install_dir)

  # フォルダ内のフォルダのみ取得 (ファイルは省く)
  folders = [f for f in files if os.path.isdir(os.path.join(chrome_install_dir, f))]

  # version取得
  version = folders[0]

  print(version)

  return version

def GetWebDriverVersion():
  version = 0
  if (os.path.exists("chromedriver.exe") == True):
    with open("webdriver_version.txt", "r") as fp:
      version = fp.read()
  else:
    print("webdriver is not exists")
    version = 0

  print(version)

  return version

def GetMajorVersion(full_version):
  major_version = 0
  if (full_version != 0):
    return str(re.search("[0-9]*", full_version).group())

  return major_version

def GetURLwebdriver(chrome_major_version):
  # chrome driverのurl設定
  url = "https://chromedriver.chromium.org/downloads"

  # url先のhtml取得
  with urllib.request.urlopen(url) as f:
    htmltext = f.read().decode("utf-8")

  # xpathで項目取得
  title = html.fromstring(htmltext).xpath(r'//*[@id="h.e02b498c978340a_87"]/div/div/ul[1]')

  chromeDriverVesionList = title[0].xpath("li")

  DriverVersion = ""
  for versionValue in chromeDriverVesionList:
    # リンク取得
    versionValueLinkList = versionValue.xpath("p/span/a")

    # 要素が空の場合はスキップ
    if (len(versionValueLinkList) == 0):
      continue

    chromeDriverStatus = versionValueLinkList[0].text

    # メジャーバージョンを取得 (前方の文字がChromeDriver の場合にバージョンを取得する)
    m = re.search("(?<=ChromeDriver )[0-9]*", chromeDriverStatus)

    # ローカルのバージョンと一致するか確認, 一致したら結果を保存
    if (str(m.group()) == str(chrome_major_version)):
      versionOfMajor = re.search("(?<=ChromeDriver ).*", chromeDriverStatus)
      DriverVersion = str(versionOfMajor.group())

  # webdriver zipのurl設定
  target_url = ""
  if (DriverVersion != ""):
    target_url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(DriverVersion)

  return target_url, DriverVersion

def ExtractWebDriverZip(target_url):
  if (target_url != ""):
    print("zip file download from {}".format(target_url))

    # zip file download
    zip_save_path = ".\\temp.zip"
    urllib.request.urlretrieve(target_url, zip_save_path)

    # extract zip file
    with zipfile.ZipFile(zip_save_path) as zipF:
      zipF.extractall(".\\")

    os.remove(zip_save_path)

    with open("webdriver_version.txt", "w") as fp:
      fp.write(DriverVersion)
  else:
    print("webdriver url is not fount")

def DownloadWebDriver(chrome_version, webdriver_version):
  # それぞれのmajor version取得 (major versionが異なる場合のみ、webdriverを取得する)
  chrome_major_version = GetMajorVersion(chrome_version)
  webdriver_major_version = GetMajorVersion(webdriver_version)

  if (chrome_major_version != webdriver_major_version):
    print("start download webdriver for chrome version {}".format(chrome_version))

    # webdriverのzip URL取得
    target_url, DriverVersion = GetURLwebdriver(chrome_major_version)

    # webdriver zipを展開
    ExtractWebDriverZip(target_url)

  else:
    print("this webdriver is not problem.")

if __name__ == "__main__":
  # chrome version取得
  chrome_version = GetChromeVersion()

  # webdriver version取得
  webdriver_version = GetWebDriverVersion()

  # webdriver 取得 
  DownloadWebDriver(chrome_version, webdriver_version)