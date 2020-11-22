from flask import Flask, render_template, request
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.computerScience  # 'computerScience'라는 이름의 db 사용
app = Flask(__name__)

db.computer.insert_one({'code': 'LC001200-001', 'campus': '', 'subject': '데이터베이스', 'professor': '장재경', 'credits': '3',
                        'time_location': '목/1-3', 'grade': '2'})
db.computer.insert_one({'code': 'LC001300-001', 'campus': '', 'subject': '알고리즘', 'professor': '김도형', 'credits': '3',
                        'time_location': '수/7-9', 'grade': '2'})
db.computer.insert_one(
    {'code': 'LC001500-001', 'campus': '', 'subject': '운영체제', 'professor': '심광섭', 'credits': '3', 'time_location': '화/7-9',
     'grade': '2'})
db.computer.insert_one({'code': 'LC001600-001', 'campus': '', 'subject': '컴퓨터구조', 'professor': '김종완', 'credits': '3',
                        'time_location': '화/1-3', 'grade': '2'})
db.computer.insert_one(
    {'code': 'LC001800-001', 'campus': '', 'subject': '자바프로그래밍기초', 'professor': '우종정', 'credits': '3',
     'time_location': '월/4-6', 'grade': '2'})
db.computer.insert_one(
    {'code': 'LC001500-002', 'campus': '', 'subject': '자바프로그래밍기초', 'professor': '우종정', 'credits': '3',
     'time_location': '수/4-6', 'grade': '2'})
db.computer.insert_one({'code': 'LC002200-001', 'campus': '', 'subject': '프로젝트설계', 'professor': '이재원', 'credits': '3',
                        'time_location': '목/7-9', 'grade': '3'})
db.computer.insert_one(
    {'code': 'LC002300-001', 'campus': '', 'subject': '데이터베이스프로그래밍', 'professor': '장윤재', 'credits': '3',
     'time_location': '화/4-6', 'grade': '3'})
db.computer.insert_one({'code': 'LC002500-001', 'campus': '', 'subject': '모바일소프트웨어', 'professor': '우종정', 'credits': '3',
                        'time_location': '화/1-3', 'grade': '3'})
db.computer.insert_one({'code': 'LC002600-001', 'campus': '', 'subject': '네트워크분석실습', 'professor': '이윤경', 'credits': '3',
                        'time_location': '목/1-3', 'grade': '3'})
db.computer.insert_one(
    {'code': 'LC003600-001', 'campus': '', 'subject': '상업 논리 및 논술', 'professor': '강수영', 'credits': '3',
     'time_location': '금/7-9', 'grade': '3'})
db.computer.insert_one(
    {'code': 'LC003700-001', 'campus': '', 'subject': '정보.컴퓨터 교과교재연구 및 지도법', 'professor': '장윤재', 'credits': '3',
     'time_location': '월/4-6', 'grade': '3'})
db.computer.insert_one({'code': 'LC003800-001', 'campus': '', 'subject': '파이썬프로그래밍', 'professor': '홍의석', 'credits': '3',
                        'time_location': '수/4-6', 'grade': '3'})
db.computer.insert_one({'code': 'LC003800-002', 'campus': '', 'subject': '파이썬프로그래밍', 'professor': '이윤경', 'credits': '3',
                        'time_location': '목/4-6', 'grade': '3'})
db.computer.insert_one(
    {'code': 'LC003200-001', 'campus': '', 'subject': '빅데이터프로그래밍', 'professor': '김종완', 'credits': '3',
     'time_location': '수/4-6', 'grade': '4'})
db.computer.insert_one({'code': 'LC003400-001', 'campus': '', 'subject': '소프트웨어공학', 'professor': '장재경', 'credits': '3',
                        'time_location': '월/1-3', 'grade': '4'})



def getAllSchedules():
    all_schedule = [x for x in list(db.computer.find({},{'_id':0, 'code':1, 'subject':1, 'professor':1}))]
    return all_schedule