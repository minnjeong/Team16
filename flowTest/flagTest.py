from bs4 import BeautifulSoup
import requests
import datetime
import pyautogui
import time
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

## 주석 풀고 id password 입력후 사용하세요!!
# client = MongoClient("mongodb+srv://id:password@cluster16.b0dkofq.mongodb.net/?retryWrites=true&w=majority")
# db = client.movie

@app.route('/')
def home():
    return render_template('test.html')

@app.route("/movie/flag", methods=["GET"])
def flag_check():
    # flag 값 가져오기.(맨 처음에 비어있으면 True로 값 넣어줌. 이후부터는 False로 바꿔줌.)
    flagList = list(db.flag.find({},{"_id":False}))
    if flagList == None or len(flagList)==0 :
        db.flag.insert_one({"flag":True})
        flagList = list(db.flag.find({},{"_id":False}))
    else:
        flagList = list(db.flag.find({},{"_id":False}))
    flag = flagList[-1]
    print(flag)  ## {'flag': True}
    ## 여기 밑에서  {"flag":{'flag': True}} 이렇게 넘어감.
    return jsonify({ "flag": flag })
    
@app.route("/movie", methods=["POST"])
def movie_crawl():
    ## 다시 플래그 상태 바꿔서 영화 데이터 더 이상 못 불러오게 하기.
    db.flag.update_one({"flag": True}, {"$set":{"flag": False}})
    flagList = list(db.flag.find({},{"_id":False}))
    flag = flagList[-1]
    print(flag) ## {'flag': False}
    return jsonify({"flag": flag})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)