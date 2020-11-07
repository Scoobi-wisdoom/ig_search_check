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
import sys

###################################################################################
## 보낼 메시지를 입력한다.
with open("backup/message.txt", "r", encoding="utf-8") as f:
    message = f.read()
#browser.find_element_by_tag_name("h2").text == '죄송합니다. 페이지를 사용할 수 없습니다.'

## 로그인
insta_id = input("Insert your id")
insta_pwd= input("insert the password")

## filename 변경
## getID.py로 만든 데이터를 로드. 열 이름은 [celeb_id, followers]
## 메시지를 보낼 목록
filename = "test.json"
print("대상 key 데이터",filename)
with open("backup/" + filename, "r", encoding="utf-8") as f:
    json_data = f.read()

pd_data = pd.DataFrame(json.loads(json_data))
pd_data = pd_data.astype({"celeb_id": str, "followers": int})

## dm.py로 만든 데이터를 로드. 열 이름은 [celeb_id, followers, message]
## 메시지를 이미 보낸 목록
with open("backup/data_DM.json", "r", encoding="utf-8") as f:
    json_data = f.read()
message_data = pd.DataFrame(json.loads(json_data))

## celeb 중에 아이디를 변경한 celeb. 그래서 쪽지를 못 보냄.
#try:
#    with open("backup/changed_name.txt", "r") as f:
#        changed_name = eval(f.read())
#except:
#    changed_name = []

## pd_data 에서 다음 두 가지를 제외한다.
## 1. 이미 메시지를 전송한 celeb. message_data
additional_celebid = list(set(pd_data["celeb_id"]) - set(message_data["celeb_id"]))
if len(additional_celebid) > 0:
    ## 메시지를 아직 안 보낸 celeb 목록
    message_data_not_yet = pd_data[pd_data["celeb_id"].str.contains("|".join(additional_celebid))]
else:
    sys.exit("메시지는 이미 모두 보냈습니다.")

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
    raise Exception

for celeb in message_data_not_yet["celeb_id"]:
    sleep(2)
    ## DM 쓰기 버튼 클릭
    try:
        searchuser = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.EQ1Mr')))
        searchuser.click()
    except:
        print ("DM 쓰기 버튼 클릭 실패")
        raise Exception
    ## DM 받는 사람 입력
    try:
        searchuserbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div.TGYkm > div > div.HeuYH > input')))
        #ActionChains(browser)\
        #.move_to_element(searchuserbox).click()\
        #.send_keys(Keys.CONTROL, 'a')\
        #.send_keys(Keys.DELETE)\
        #.send_keys(celeb)\
        #.perform()
        searchuserbox.click()
        sleep(2)
        searchuserbox.send_keys(Keys.CONTROL, 'a')
        sleep(2)
        searchuserbox.send_keys(Keys.DELETE)
        sleep(2)
        searchuserbox.send_keys(celeb)
    except:
        print("DM 받는 사람 입력 실패")
        webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        ## DM 내역 저장하기: 실패. 공란 처리
        #message_data_to_append = message_data_not_yet.loc[message_data_not_yet['celeb_id'] == celeb].to_dict('r')[0]
        #message_data_to_append["message"] = ""
        #message_data = message_data.append(message_data_to_append, ignore_index=True)
        #with open("backup/data_DM.json", "w", encoding="utf-8") as f:
        #    f.write(json.dumps(message_data.to_dict(), ensure_ascii=False))
        #continue

    ## DM 받는 사람 목록 중에서 첫 번째 사람을 선택
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='                    Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                   XfCBB          HVWg4                 ']")))
        sleep(2)
        firstuser = browser.find_element_by_xpath("//div[@class='                    Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                   XfCBB          HVWg4                 ']")
        # 검색 결과 첫 번째 사람이 celeb 과 일치할 경우만 다음 단계로 진행
        if celeb != firstuser.text.split("\n")[0]:
            print(celeb, "은 아이디를 변경함")
            ## DM 내역 저장하기: 실패. 공란 처리
            message_data_to_append = message_data_not_yet.loc[message_data_not_yet['celeb_id'] == celeb].to_dict('r')[0]
            message_data_to_append["message"] = ""
            message_data = message_data.append(message_data_to_append, ignore_index=True)
            with open("backup/data_DM.json", "w", encoding="utf-8") as f:
                f.write(json.dumps(message_data.to_dict(), ensure_ascii=False))
            webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
            continue
        firstuser.click()
    except:
        print("DM 받는 사람 선택 실패")
        print(celeb, "은 아이디를 변경함")
        message_data_to_append = message_data_not_yet.loc[message_data_not_yet['celeb_id'] == celeb].to_dict('r')[0]
        message_data_to_append["message"] = ""
        message_data = message_data.append(message_data_to_append, ignore_index=True)
        with open("backup/data_DM.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(message_data.to_dict(), ensure_ascii=False))
        webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        continue

    ## 다음 버튼 누르기
    try:
        pressingnext = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.rIacr')))
        pressingnext.click()
    except:
        print ("다음 버튼 누르기 실패")
        continue

    ### 텍스트 박스 찾기
    #try:
    #    textbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')))
    #except:
    #    print("텍스트 박스 찾기 실패")
    #    continue

    ## DM 보내기
    try:
        ## textbox에 메시지 입력
        sleep(5)
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')))
        textbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')))
        print("textbox clicked")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')))
        browser.execute_script("arguments[0].value = arguments[1]", browser.find_element_by_xpath('//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea'), message)
        sleep(2)
        textbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')))
        textbox.click()
        textbox.send_keys(Keys.END)
        textbox.send_keys(Keys.SPACE)
        ## 버튼 클릭
        send_xpath = '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button'
        wait.until(EC.element_to_be_clickable((By.XPATH, send_xpath)))
        browser.find_element_by_xpath(send_xpath).click()
        print("메시지 보내기 성공")
        ## DM 내역 저장하기: 성공
        message_data_to_append = message_data_not_yet.loc[message_data_not_yet['celeb_id'] == celeb].to_dict('r')[0]
        message_data_to_append["message"] = message
        message_data = message_data.append(message_data_to_append, ignore_index=True)
        with open("backup/data_DM.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(message_data.to_dict(), ensure_ascii=False))
    except:
        print(celeb, "에게 DM 보내기 실패")

    
    sleep(random.uniform(60,180))
    #sleep(random.uniform(6,10))
print("메시지 발송을 완료했습니다.")
