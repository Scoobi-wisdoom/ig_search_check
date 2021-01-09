from bs4 import BeautifulSoup
import json
import requests

# url 변경하자
url = "https://search.shopping.naver.com/category/category/50000009"
sauce = requests.get(url)
soup = BeautifulSoup(sauce.text, 'lxml')

# 클래스 변경하자
base_soup = soup.find("div", class_="__50000009_container__VXecS")

# + 없는 페이지
level1 = {}
for h3 in base_soup.find_all("h3"):
    level2 = {}
    for origin_li in h3.parent.find("ul").find_all("li", recursive=False):
        ul = origin_li.find("ul")
        level3 = list()
        if origin_li.find("a") is None:
            continue
        if ul is None:
            level2[origin_li.find("a").text] = level3
            continue
        for li in ul.find_all("li"):
            level3.append(li.text)
        level2[origin_li.find("a").text] = level3
    level1[h3.find("strong").text] = level2

level0 = {base_soup.find("h2").text: level1}

with open("9.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(level0))