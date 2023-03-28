import requests
from bs4 import BeautifulSoup
import datetime
import pyautogui
import time

# 아니 근데 페이지 여러 개면 페이지간 이동하는거 어떻게 구현하지? aws app.py 한 개랑, index.html 한 개밖에 안올라가지 않나? css에서 page 조건별 display:none 줘야하나?
### 설명할 부분+ (구현 논의 필요.)
# 1. 홈에서 포스터를 누르면 포스터의 고유 num을 가지고(div > a(url) > span ~ img(이미지))리뷰 작성 페이지로 넘어가도록 태그 구성할 것(그건 HTML 맡은 분이...).) num 을 페이지 별로 넘겨야 함.
# 2. 홈에서 몇 개 정도의 보여주기식 댓글이 보이게 할 것인지?

## 내가 생각해야 하는 부분.
# 3. 평점순, 조회순, 평점순(현재상영) 별로 구현하고 싶다면 아예 맨처음에 크롤링 때 두 가지 종류 크롤링 더 추가해서 저장하는 장소 movie2, movie3 이런 식으로 더 만들어야 할 듯.
#    또 if문 써서 상태에 따라 불러올 데이터베이스 구성해놔야 할 듯. (역시 한 번 불러온 이후에는 리로딩 없도록 설계할 것.)
# 4. 페이지별 고유 쿼리를 배열에 넣고 let sel = [cnt, pnt, cur],   페이지는 if문 써서 왔다갔다 해야 할 듯?   if(보여줄페이지==메인페이지){  }


# 랭크 페이지( 영화랭킹 - 평점순(모든영화) - 밑에 숫자 버튼눌러서 페이지 왔다갔다 해보면 바뀌는 부분 확인 가능. )
# https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20230326&page=1
# url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date={today}&page={i}'

# 영화랭킹 - 평점순(모든영화)  => (url사용) =>  포스트(한 개) 내부 페이지
# https://movie.naver.com/movie/bi/mi/basic.naver?code=224494
# https://movie.naver.com/movie/bi/mi/basic.naver?code=81888

# 영화랭킹 - 조회순 (페이지 한 개밖에 없음, 페이지 쿼리 없음.)
# https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&date=20230327
# url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel={cnt}&date={today}'

# 영화랭킹 - 평점순(현재상영영화) (페이지 한 개밖에 없음, 페이지 쿼리 없음.)
# https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cur&date=20230327
# url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel={cur}&date={today}'


# 여러 페이지
import requests
from bs4 import BeautifulSoup
import datetime
today = datetime.datetime.today()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# 가져올 페이지 입력
# lastpage = int(pyautogui.prompt("총 검색할 페이지 수를 입력하세요."))
# 순위는 수동으로 지정했음. 아이디 클래스 태그 속성 심지어 위아래 태그까지 아예 똑같은데 값은 다른게 겹쳐 있어서 못 뽑음.
lastpage = 1
rank = 0
for i in range(1, lastpage+1):
    # + str(i)
    url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date={today}&page={i}'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    link = soup.select("div.tit5 > a[href]")
    name = soup.select('div.tit5')
    score = soup.select('td.point')
    for n, s, l in zip(name, score, link):
        rank += 1
        print(rank, n.text.strip(), s.text.strip(), l['href'], sep="\t"*2)
        # 코드 확인
        code = int(l['href'].split("=")[-1])
        print(type(code))  #<class 'int'>
        star = float(s.text.strip())
        print(type(star))  #<class 'float'> ex) 9.xx  별로 어떻게 구현할꺼? css 처리 필요함.(네이버 별 그림 참고)
        # 오늘 가져온 것 확인


# 날짜별 검색
# today = datetime.datetime.today()
# for i in range(1, 3):
#     day = today - datetime.timedelta(days=i)
#     strDay= day.strftime('%Y%m%d')
#     url = 'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&tg=0&date='+ strDay
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     datas=soup.select('div.tit5')
#     scores = soup.select('td.point')
#     for data, score in zip(datas, scores):
#         print(data.text.strip(), score.text.strip())


# # 별 모양(평점에 따라 채워진 정도 조절)
# <img src="https://ssl.pstatic.net/imgmovie/2007/img/common/point_type_2_bg_on.gif" width="79" height="14" alt="">
# #old_content > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > img
# 스타일 복사
#     border-collapse: collapse;
#     border-spacing: 0;
#     color: #656565;
#     text-align: left;
#     width: 79px;
#     aspect-ratio: auto 79 / 14;
#     height: 14px;
#     margin: 0;
#     padding: 0;
#     font-style: normal;
#     font-size: 12px;
#     font-family: "돋움", Dotum, "굴림", Gulim,Helvetica,AppleSDGothicNeo-Medium,AppleGothic, Sans-serif;
#     border: none;
#     vertical-align: middle;
#     display: block;


## 검색한 메서드
# findAll(tag, attributes, recursive, text, limit, keywords)
# find(tag, attributes, recursive, text, keywords)
# select, selectAll


# ## 날짜 내장 함수 사용
# import datetime
# today = datetime.datetime.today()
# for i in range(1,4):
#     startday = today - datetime.timedelta(days=i)
#     print(startday.strftime('%Y%m%d'))


# # zip >> 자료형을 (끼리끼리) 묶어주는 역할 (첫 번째 인수는 첫 번째끼리 ,,)
# print(list(zip([1,2,3],[4,5,6],[7,8,9])))  ## [(1, 4, 7), (2, 5, 8), (3, 6, 9)]
# print(list(zip("abc","def")))  ## [('a', 'd'), ('b', 'e'), ('c', 'f')]
# print(list(zip('abcdefg',range(4)))) ## [('a', 0), ('b', 1), ('c', 2), ('d', 3)]


# # zip 조심
# numbers = [1, 2, 3, 4]
# letters = ['a', 'b', 'c', 'd']
 
# zipped = zip(numbers, letters)
# print(type(zipped))  ## <class 'zip'>
 
# zipped = list(zipped)
# print(zipped)
