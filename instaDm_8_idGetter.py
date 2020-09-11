import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import json
import pandas as pd
import re

insta_id = input("Insert your id:")
insta_pwd= input("Insert the password")
#search_word = input("insert the search keyword")
#keyword1: 공구진행, 공구, 공구마켓
#keyword2: 운동
#keyword3: 뷰티
#keyword4: 셀카
#keyword5: 다이어트
#keyword5: 맘스타그램

## instagram 피드에서 end키를 몇 번 눌렀는지 체크
end_key_count = 0

## 이번 프로그램 실행을 통해 접근한 celeb_id의 목록(pd_data에 저장하지 않는다)
# current_search = []
try:
    with open("backup/current_search.txt", "r") as f:
        current_search = eval(f.read())

except:
    current_search = []

## json에서 데이터 로드. 열 이름은 ["celeb_id", "followers"]
with open("backup/data1.json", "r", encoding="utf-8") as f:
    json_data = f.read()

pd_data = pd.DataFrame(json.loads(json_data))
pd_data = pd_data.astype({"celeb_id": str, "followers": int})


webdriver_path = r"chromedriver_win32\chromedriver.exe" # Webdriver 가 저장된 위치
browser = webdriver.Chrome(webdriver_path)

### 브라우저 크기 설정
browser.set_window_size(1051, 806)

browser.get("https://www.instagram.com/")

wait = WebDriverWait(browser, 30)

## 로그인

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

############################################ 사용자 함수 Start ############################################
### 1. try 사진 클릭. except 사진이 로드 되지 않는 오류가 생긴다면?
class ig_class:
    def __init__(self):
        self.num_except = 0
    
    def photo_click(self, photo):
        try:
            photo.click()
            ### div class="e1e1d" 셀럽 아이디
            if(self.num_except < 3):
                print("사용자 정의 함수 photo_click: try")
                wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='e1e1d']")))
            elif(self.num_except == 3):
                print("rightpagination 클릭")
                wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@class=' _65Bje  coreSpriteRightPaginationArrow']")))
                browser.find_element_by_xpath("//a[@class=' _65Bje  coreSpriteRightPaginationArrow']").click()
                self.num_except = 0
                wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='e1e1d']")))
            else:
                print("photo.click() 오류 발생")
        except:
            print("사용자 정의 함수 photo_click: except 시작")
            ActionChains(browser).send_keys(Keys.ESCAPE).perform()
            sleep(2)
            ActionChains(browser).send_keys(Keys.PAGE_DOWN).perform()
            sleep(2)
            ActionChains(browser).send_keys(Keys.PAGE_UP).perform()
            sleep(2)
            self.num_except += 1
            print("exception 발생 횟수", self.num_except)
            print("사용자 정의 함수 photo_click: except 끝")
            self.photo_click(photo)

### 2. 인스타그램의 스팸 방지 시스템을 우회하기 위해 클릭한 인스타를 꼭 눈팅하기로 하자.
### 똑같은 패턴을 보이면 안 되니까 random을 사용하자.
def look_blog():
    print("블로그 보는 척 시작")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='v1Nh3 kIKUG  _bz0w']")))
    blog_photo_list = browser.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']")
    ### 2 개에서 6개의 사진을 무작위로 추출
    blog_photo_to_look = random.sample(blog_photo_list, min(random.randint(2,6), len(blog_photo_list)))

    for photo in blog_photo_to_look:
        ### photo_click(): 사용자 정의 함수
        try:
            photo.click()
            ### 1초에서 10초 사이의 무작위 시간 동안 사진을 보자
            sleep(random.uniform(1,10)) 
            ActionChains(browser).send_keys(Keys.ESCAPE).perform()
            sleep(random.uniform(0,3))
        except:
            continue
    print("블로그 보는 척 끝")

### 3. 코멘트 다는 함수 -> deprecated
############################################ 사용자 함수 End ############################################
        
## "나중에 하기"
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-root > section > main > div > div > div > div > button")))
browser.find_element_by_css_selector("#react-root > section > main > div > div > div > div > button").click()
print("로그인 정보 저장 나중에 하기 성공")

ActionChains(browser).move_to_element(wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm")))).click().perform()
print("알림 설정 나중에 하기 성공")


## 검색
#search_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.LWmhU._0aCwM > input")))
#search_box.send_keys(search_word)
#wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#react-root > section > nav > div._8MQSO.Cx7Bp > div > div > div.LWmhU._0aCwM > div.aIYm8.coreSpriteSearchClear")))
#print("엑스 박스 생성")
#search_box.send_keys(Keys.ENTER)
#search_box.send_keys(Keys.ENTER)
search_done = input("검색을 완료했으면 y키를 누른 후 엔터")
if(search_done.lower() != 'y'):
    raise Exception

## 검색 실행 후 UI
### instagram ui에서 1행 3개 사진이 div class="Nnq7C weEfm"로 묶여 있다.
### 각 사진 div class="v1Nh3 kIKUG  _bz0w"
photo = ''

while(True):
    ## 셀럽의 인스타 홈페이지는 새 탭에서 열 것임. 그렇기 때문에 원래 탭을 저장해야 함.
    ### 원래 윈도우 저장
    feed_window = browser.current_window_handle
    ### 검색 후 목록이 나타낼 때까지 기다린다.
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='v1Nh3 kIKUG  _bz0w']")))
    photo_list = browser.find_elements_by_xpath("//div[@class='v1Nh3 kIKUG  _bz0w']")

    ## end키를 눌러도 더 이상 새로운 사진이 없을 경우 while문을 종료한다.
    if(photo == photo_list[-1]):
        break

    ## end키를 눌러서 새로운 사진이 나타날 경우, 새로운 사진부터 photo_list를 설정한다.
    if(photo in photo_list):
        photo_list = photo_list[photo_list.index(photo)+1:]
    
    for photo in photo_list:

        ## 검색된 목록 중 한 개를 클릭
        ### photo_click: 사용자 지정 함수
        ig_class().photo_click(photo)

        ### 아이디가 나타나는 a tag를 인식하여 https://www.instagram.com/셀럽아이디/ 를 획득
        try:
            ###사진
            #wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div[1]/div/div/a[2]')))
            #celeb_url = browser.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]').get_attribute('href')
            wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='e1e1d']")))
            celeb_url = browser.find_element_by_xpath("//div[@class='e1e1d']").find_element_by_tag_name('a').get_attribute('href')
            
        except:
            ###이름
            #wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/article/header/div[1]/div/a')))
            #celeb_url = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[1]/div/a').get_attribute('href')
            #wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@class='_2dbep qNELH kIKUG']")))
            #celeb_url = browser.find_element_by_xpath("//a[@class='_2dbep qNELH kIKUG']").get_attribute('href')
            #wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/h2/div/span/a")))
            #celeb_url = browser.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]/h2/div/span/a").get_attribute('href')
            wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a")))
            celeb_url = browser.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a").get_attribute('href')

        ### https://www.instagram.com/셀럽아이디/ 에서 셀럽아이디를 regex로 획득
        celeb_id = re.search(r'.com/(.*)/.*', celeb_url).group(1)
        print("version 5 셀럽아이디:",celeb_id)


        
        
        ## celeb_id가 이미 json 데이터에 있으면, 해당 블로그를 열지 않는다.
        ## 또는 celeb_id가 이미 current_search에 있으면 해당 블로그는 열지 않는다.
        sleep(random.uniform(0,3))
        if(celeb_id in pd_data.celeb_id.values or celeb_id in current_search):
            ### esc를 눌러 종료한 후에 continue
            ActionChains(browser).send_keys(Keys.ESCAPE).perform()
            sleep(random.uniform(0,2))
            continue


        ### 새 탭에서 셀럽 블로그 열기
        ActionChains(browser) \
        .key_down(Keys.CONTROL) \
        .click(browser.find_element_by_xpath("//div[@class='e1e1d']")) \
        .key_up(Keys.CONTROL) \
        .perform()


        ### 새 탭으로 넘어가기
        browser.switch_to.window(browser.window_handles[-1])

        ## 셀럽 인스타 팔로워 체크
        ### 게시물[0] 팔로워[1] 팔로잉[2] span class="g47SY " title= 수
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='g47SY ']")))
        num_of_followers = browser.find_elements_by_xpath("//span[@class='g47SY ']")[1].get_attribute('title')
        if(len(num_of_followers) == 0):
            num_of_followers = browser.find_elements_by_xpath("//span[@class='g47SY ']")[1].text

        ### 팔로워 수가 1000명 미만이면 콤마가 없다.
        if(len(num_of_followers) > 3):
            num_of_followers = int(num_of_followers.replace(',',''))
        else:
            num_of_followers = int(num_of_followers)

        ## 해당 셀럽의 팔로워 수가 700명 이상인지 체크 
        if(num_of_followers >= 700):
            print(celeb_id, "의 팔로워 수:", num_of_followers)
            big_followers = True
        else:
            big_followers = False
            

        ## 셀럽 팔로워가 많은 경우 블로그를 살펴보는 척을 하자.
        ## look_blog(): 사용자 지정 함수
        if(big_followers):
            look_blog()
        
        ## 해당 새 탭 닫기
        browser.close()
        browser.switch_to.window(feed_window)

        ## ## big_followers True 이면 댓글을 달자
        ### leave_comment(): 사용자 지정 함수
        if(big_followers):
            pd_data = pd_data.append(pd.Series([celeb_id, num_of_followers], index=pd_data.columns), ignore_index=True)
        else:
            ## celeb_id의 블로그에 접속하면 기록에 남긴다.
            current_search.append(celeb_id)
            with open("backup/current_search.txt", "w") as f:
                f.write(json.dumps(current_search))


        ## pd_data를 로컬에 저장
        with open("backup/data1.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(pd_data.to_dict(), ensure_ascii=False))

        ## 피드 중 열린 사진 x 표 누르기
        ### ESC 키보드 클릭
        ActionChains(browser).send_keys(Keys.ESCAPE).perform()

    ## for문 종료
        
    ### 키보드로 end키를 눌러서 사진을 더 많이 불러오자. 10초 sleep
    print("end 키를 눌러보자")
    ActionChains(browser).send_keys(Keys.END).perform()
    end_key_count += 1
    print('end 키를 누른 총 횟수',end_key_count)
    sleep(10)

print("마지막 사진에 도달하여 프로그램 종료")
