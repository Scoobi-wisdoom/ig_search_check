import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import json
import pandas as pd

###################################################################################
## 아래에 message라는 항목에 보낼 메시지를 입력한다.

## 로그인
insta_id = input("Insert your id")
insta_pwd= input("insert the password")

## getID.py로 만든 데이터를 로드. 열 이름은 [celeb_id, followers]
with open("data1.json", "r", encoding="utf-8") as f:
    json_data = f.read()

pd_data = pd.DataFrame(json.loads(json_data))
pd_data = pd_data.astype({"celeb_id": str, "followers": int})

## dm.py로 만든 데이터를 로드. 열 이름은 [celeb_id, followers, message]
with open("data_DM.json", "r", encoding="utf-8") as f:
    json_data = f.read()
message_data = pd.DataFrame(json.loads(json_data))

## pd_data와 message_data의 괴리를 없앤다.
additional_celebid = list(set(pd_data["celeb_id"]) - set(message_data["celeb_id"]))
if len(additional_celebid) > 0:
    data_to_append = pd_data[pd_data["celeb_id"].str.contains("|".join(additional_celebid))]
    message_data = message_data.append([data_to_append], ignore_index=True, sort=True).fillna("")

## 메시지를 아직 안 보낸 celeb 목록
message_data_not_yet = message_data[message_data["message"] == ""]

webdriver_path = r"chromedriver_win32\chromedriver.exe" # Webdriver 가 저장된 위치
browser = webdriver.Chrome(webdriver_path)

### 브라우저 크기 설정
browser.set_window_size(1051, 806)

browser.get("https://www.instagram.com/")

wait = WebDriverWait(browser, 30)


user = wait.until(EC.presence_of_element_located((By.NAME, "username")))
passw = browser.find_element_by_name("password")

ActionChains(browser)\
    .move_to_element(user).click()\
    .send_keys(insta_id)\
    .move_to_element(passw).click()\
    .send_keys(insta_pwd)\
    .perform()

passw.submit()
print("로그인 성공")

## "나중에 하기"
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-root > section > main > div > div > div > div > button")))
browser.find_element_by_css_selector("#react-root > section > main > div > div > div > div > button").click()
print("로그인 정보 저장 나중에 하기 성공")

ActionChains(browser).move_to_element(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm")))).click().perform()
print("알림 설정 나중에 하기 성공")


############################################ https://github.com/Donald-K-Lee/InstagramDMBot/blob/master/InstagramDMBot.py ############################################
## DM 버튼 클릭
try:
    dmbtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.xWeGp')))
    dmbtn.click()
except:
    print ("DM 버튼 클릭 실패")

for celeb in message_data_not_yet["celeb_id"]:
    ### 보낼 메시지를 입력한다. celeb_id는 자동으로 메시지에 포함되게 한다.
    message =  f"안녕하세요 {celeb}님"
    ## DM 쓰기 버튼 클릭
    try:
        searchuser = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.EQ1Mr')))
        searchuser.click()
    except:
        print ("DM 쓰기 버튼 클릭 실패")

    ## DM 받는 사람 입력
    try:
        searchuserbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div.TGYkm > div > div.HeuYH > input')))
        searchuserbox.send_keys(celeb)
    except:
        print ("DM 받는 사람 입력 실패")

    ## DM 받는 사람 목록 중에서 첫 번째 사람을 선택
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='                    Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                   XfCBB          HVWg4                 ']")))
        sleep(2)
        firstuser = browser.find_element_by_xpath("//div[@class='                    Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                   XfCBB          HVWg4                 ']")
        firstuser.click()
    except:
        print("DM 받는 사람 선택 실패")

    ## 다음 버튼 누르기
    try:
        pressingnext = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.rIacr')))
        pressingnext.click()
    except:
        print ("다음 버튼 누르기 실패")

    ## 텍스트 박스 찾기
    try:
        textbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.focus-visible')))
    except:
        print("텍스트 박스 찾기 실패")

    ## DM 보내기
    try:
        textbox.send_keys(message)
        textbox.send_keys(Keys.RETURN)
        print("메지지 보내기 성공")
    except:
        print(celeb, "에게 DM 보내기 실패")

    ## DM 내역 저장하기
    #message_data.loc[message_data['celeb_id'] == celeb, "message"] = message
    message_data.loc[message_data['celeb_id'] == celeb, "message"] = "test"
    with open("data_DM.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(message_data.to_dict(), ensure_ascii=False))
    sleep(random.uniform(60,120))