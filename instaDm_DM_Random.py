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
import re
import os

count_limit = 80

## 로그인
insta_id = input("Insert your id")
insta_pwd = input("insert the password")

webdriver_path = r"chromedriver_win32\chromedriver.exe"  # Webdriver 가 저장된 위치
browser = webdriver.Chrome(webdriver_path)

### 브라우저 크기 설정
browser.set_window_size(1051, 806)

browser.get("https://www.instagram.com/")

wait = WebDriverWait(browser, 30)

user = wait.until(EC.presence_of_element_located((By.NAME, "username")))
passw = browser.find_element_by_name("password")

ActionChains(browser) \
    .move_to_element(user).click() \
    .send_keys(insta_id) \
    .move_to_element(passw).click() \
    .send_keys(insta_pwd) \
    .perform()

passw.submit()
print("로그인 성공")

## "나중에 하기"
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-root > section > main > div > div > div > div > button")))
browser.find_element_by_css_selector("#react-root > section > main > div > div > div > div > button").click()
print("로그인 정보 저장 나중에 하기 성공")

ActionChains(browser).move_to_element(wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, "body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm")))).click().perform()
print("알림 설정 나중에 하기 성공")

print("키워드", 2, "개까지만 랜덤 적용")

key_data_pool = []
message_pool = []

# 대상 인플루언서 파일 목록
for filename in os.listdir("backup"):
    key = re.findall(r"key[0-9].json", filename)
    if len(key) > 0:
        key_data_pool.append(key[0])
key_data_pool.sort()

# 보낼 메시지 목록
for filename in os.listdir("backup/messages"):
    msg = re.findall(r"message[0-9]_[0-9]+.txt", filename)
    if len(msg) > 0:
        message_pool.append(msg[0])

# data_DM data
data_DM ="data_DM_random.json"

# 실행 횟수 체크
count = 0
# message_pool 편집으로 DM 을 보낸다.
while len(message_pool) > 0 and count < count_limit:
    # 실행 횟수
    count += 1

    # messages 중 무작위로 선택
    message_txt = random.sample(message_pool, 1)[0]
    # key 선택: 1, 2, 3, ...
    key = re.findall(r"message(.*)_.*$", message_txt)[0]
    key_data = key_data_pool[int(key)-1]

    # key_data 중 안 보낸 목록이 있는지 체크
    ## 메시지를 보낼 목록
    ## getID.py로 만든 데이터를 로드. 열 이름은 [celeb_id, followers]
    print("대상 key 데이터",key_data)
    with open("backup/" + key_data, "r", encoding="utf-8") as f:
        json_data = f.read()

    pd_data = pd.DataFrame(json.loads(json_data))
    pd_data = pd_data.astype({"celeb_id": str, "followers": int})

    ## dm.py로 만든 데이터를 로드. 열 이름은 [celeb_id, followers, message, key]
    ## 메시지를 이미 보낸 목록
    with open("backup/"+ data_DM, "r", encoding="utf-8") as f:
        json_data = f.read()
    message_data = pd.DataFrame(json.loads(json_data))

    ## pd_data 에서 다음을 제외한다.
    ## 이미 메시지를 전송한 celeb. message_data
    additional_celebid = list(set(pd_data["celeb_id"]) - set(message_data["celeb_id"]))
    if len(additional_celebid) < 1:
        print("메시지는 이미 key", key, "에 모두 보냈습니다.")
        # 이미 보낸 key 는 message_pool 에서 제외
        for message in message_pool:
            exclude = re.findall(r"message"+ key +"_.*$", message)[0]
            message_pool.remove(exclude)
        continue

    ## 메시지를 아직 안 보낸 celeb 목록
    message_data_not_yet = pd_data[pd_data["celeb_id"].isin(additional_celebid)]


    ###################################################################################
    ## 보낼 메시지를 입력한다.
    with open("backup/messages/"+message_txt, "r", encoding="utf-8") as f:
        message = f.read()


    ############################################ https://github.com/Donald-K-Lee/InstagramDMBot/blob/master/InstagramDMBot.py ############################################
    ## DM 버튼 클릭
    try:
        dmbtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.xWeGp')))
        dmbtn.click()
    except:
        print ("DM 버튼 클릭 실패")
        raise Exception

    celeb = message_data_not_yet["celeb_id"][0]
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
        sleep(2)
        searchuserbox = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.RnEpo.Yx5HN > div > div > div.Igw0E.IwRSH.eGOV_.vwCYk.i0EQd > div.TGYkm > div > div.HeuYH > input')))
        searchuserbox.click()
        sleep(2)
        searchuserbox.send_keys(Keys.CONTROL, 'a')
        sleep(2)
        searchuserbox.send_keys(Keys.DELETE)
        sleep(2)
        searchuserbox.send_keys(celeb)
    except:
        print("DM 받는 사람 입력 실패")
        print("data_DM_random.json 에 저장하지 않는다.")
        webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
        ## DM 내역 저장하기: 실패. 공란 처리
        #message_data_to_append = message_data_not_yet.loc[message_data_not_yet['celeb_id'] == celeb].to_dict('r')[0]
        #message_data_to_append["message"] = ""
        #message_data = message_data.append(message_data_to_append, ignore_index=True)
        #with open("backup/data_DM.json", "w", encoding="utf-8") as f:
        #    f.write(json.dumps(message_data.to_dict(), ensure_ascii=False))
        continue

    ## DM 받는 사람 목록 중에서 첫 번째 사람을 선택
    try:
        sleep(5)
        #wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='                    Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                   XfCBB          HVWg4                 ']")))
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div')))
        #firstuser = browser.find_element_by_xpath("//div[@class='                    Igw0E   rBNOH        eGOV_     ybXk5    _4EzTm                                                                                   XfCBB          HVWg4                 ']")
        firstuser = browser.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div')
        # 검색 결과 첫 번째 사람이 celeb 과 일치할 경우만 다음 단계로 진행
        #if celeb != firstuser.text.split("\n")[0]:
        if celeb != firstuser.text:
            print(celeb, "은 아이디를 변경함")
            ## DM 내역 저장하기: 공란 처리
            message_data_to_append = message_data_not_yet.loc[message_data_not_yet['celeb_id'] == celeb].to_dict('r')[0]
            message_data_to_append["message"] = ""
            message_data_to_append["key"] = int(key)
            message_data = message_data.append(message_data_to_append, ignore_index=True)
            with open("backup/"+data_DM, "w", encoding="utf-8") as f:
                f.write(json.dumps(message_data.to_dict(), ensure_ascii=False))
            webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
            continue
        firstuser.click()
    except:
        print("DM 받는 사람 선택 실패")
        print(celeb, "은 아이디를 변경함")
        ## DM 내역 저장하기: 공란 처리
        message_data_to_append = message_data_not_yet.loc[message_data_not_yet['celeb_id'] == celeb].to_dict('r')[0]
        message_data_to_append["message"] = ""
        message_data_to_append["key"] = int(key)
        message_data = message_data.append(message_data_to_append, ignore_index=True)
        with open("backup/"+data_DM, "w", encoding="utf-8") as f:
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

    ## DM 대상자가 그 대상자가 맞는지 check. 아니면 insta 에서 우리 계정을 막은 것
    try:
        sleep(5)
        # dm 대상자의 profile name xpath
        #profile_name_path = '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/button/div/div/div'
        profile_name_path = '/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/div[2]/button/div/div/div'
        wait.until(EC.element_to_be_clickable((By.XPATH, profile_name_path)))
        profile_name = wait.until(EC.element_to_be_clickable((By.XPATH, profile_name_path))).text
        if profile_name != celeb:
            print("문제가 발생했습니다. 다시 시도해주세요")
            break
    except:
        print("우리 계정 block 여부 판단 실패")
        break

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
        message_data_to_append["key"] = int(key)
        message_data = message_data.append(message_data_to_append, ignore_index=True)
        with open("backup/"+data_DM, "w", encoding="utf-8") as f:
            f.write(json.dumps(message_data.to_dict(), ensure_ascii=False))
    except:
        print(celeb, "에게 DM 보내기 실패")


    sleep(random.uniform(180,240))
    #sleep(random.uniform(6,10))
print("메시지 발송을 완료했습니다.")
