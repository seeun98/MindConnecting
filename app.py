from flask import Flask, render_template, request, jsonify, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from pymongo import MongoClient
from datetime import datetime
from forms import UserCreateForm, UserLoginForm, ProfessorOfficeForm, CommunicateForm, CommunicateReForm, ProfessorCommunicateForm
import uuid
import config

client = MongoClient('localhost', 27017)
db = client.mindConnecting

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def home():
    return redirect(url_for('professorList'))

#----회원가입-----
@app.route("/joinus", methods=['GET', 'POST'])
def joinus():
    form = UserCreateForm()
    
    if request.method == 'POST':
        user = db.member.find_one({'id': form.userid.data})
        if not user:
            user = {
                'id' : form.userid.data,
                'password' : generate_password_hash(form.password1.data),
                'name': form.name.data,
                'email' : form.email.data,
                'is_student' : form.is_student.data,
                'department' : form.department.data
            }
            print(user)
            db.member.insert_one(user)
            return redirect(url_for('login'))
        else:
            flash('이미 존재하는 사용자입니다')

    return render_template('joinus.html', form=form)



#----로그인 인증 -----
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = UserLoginForm()

    if request.method == 'POST':
        error = None
        user = db.member.find_one({'id' : form.userid.data })
        print(user)
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user['password'], form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['user_is_student'] = user['is_student']
            print(session['user_id'], session['user_is_student'])
            if  session['user_is_student'] == 'Professor':
                return redirect(url_for('professorOfficeForm'))
           
            return redirect(url_for('home'))
                

            
    return render_template('login.html', form=form)

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.member.find_one({ 'id' : user_id})['name']
        g.is_professor = db.member.find_one({ 'id':user_id})['is_student']
        if g.is_professor == 'Professor':
            g.is_professor = True
        else:
            g.is_professor = False
        

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

#------professorList--------
@app.route('/professorList', methods=['GET'])
def professorList():
    schedule_list = list(db.schedule.find({},
                                            {'_id':0,
                                            'subject':1,
                                            'professor':1,
                                            'time_location':1,
                                            'code':1}))
    professor_status_list = list(db.professorStatus.find({}, {'_id':0}))
    professor_status_dict = {item.get('name'):item.get('status')
                                for item in professor_status_list}

    color_dict = {
        '재실': 'success',
        '퇴근': 'danger',
        '연구중':'warning',
        '휴식중':'secondary',
    }
    print(professor_status_dict)
    for sc in schedule_list:
        sc['status'] = professor_status_dict.get(sc['professor'],None)
        sc['color'] = color_dict.get(sc['status'], '')
        
    print(schedule_list)
    return render_template("professorIndex.html", schedule_list = schedule_list)

#-----professorOfficeForm--------
@app.route("/professorOfficeForm", methods=['GET','POST'])
def professorOfficeForm():
    form = ProfessorOfficeForm()
    if request.method == 'POST':
        professor = db.member.find_one({'name':form.name.data, 'is_student':'Professor'})
        if professor:
            info = {
                'name':form.name.data,
                'status' : form.status.data
            }
            db.professorStatus.delete_many({'name':info['name']})
            db.professorStatus.insert_one(info)
            return redirect(url_for('home'))
        else:
            flash("데이터베이스에 없습니다.")

    return render_template("professorOfficeForm.html", form=form)

#-------communicate---------
#게시판 들어가기

@app.route("/communicate/<code>", methods=['GET', 'POST'])
def communicate_page(code):
    form = CommunicateForm()
    
    if request.method == 'POST':
        print("communicate Here")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        communicate_id = uuid.uuid4().hex
        info = {
            'communicate_id':communicate_id,
            'code' : code,
            'title' : form.title.data,
            'content' : form.content.data,
            'timestamp' : timestamp
        }
        db.communicate.insert_one(info)

    
    communicate_list = list(db.communicate.find({'code':code}, {'_id' : 0}))
    return render_template('communicate.html', communicate_list = communicate_list, form= form)


#-----게시판 댓글 가기
@app.route("/communicate/<code>/<communicate_id>", methods=['POST', 'GET'])
def communicateRe_page(code, communicate_id):
    print("HERE")
    form = CommunicateReForm()

    if request.method == 'POST':
        print("HERE")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        info = {
            'code' : code,
            'communicate_id' : communicate_id,
            'REcontent' : form.REcontent.data,
            'timestamp' : timestamp
        }
        print(info)
        db.communicateComment.insert_one(info)
        
    else:
        print("Not Here")

    communicate_code = list(db.communicate.find({'code':code,'communicate_id' : communicate_id}))
    print(communicate_code)
    communicateRe_code = list(db.communicateComment.find({'code':code, 'communicate_id':communicate_id}))
    print(communicateRe_code)
    return render_template('communicateRe.html', communicate_code = communicate_code, communicateRe_code = communicateRe_code, form=form )


# -----------------내시간표 고르기------------------
@app.route("/mySchedule", methods=['POST', 'GET'])
def mySchedule():
    print("HERE")
    
    schedule_list = list(db.schedule.find({},
                                            {'_id':0,
                                            'subject':1,
                                            'professor':1,
                                            'time_location':1,
                                            'code':1}))
    print(schedule_list)

    mySchedule_list = list(db.mySchedule.find({'user':g.user}))
    print(mySchedule_list)
    return render_template('mySchedule.html', schedule_list = schedule_list, mySchedule_list = mySchedule_list)

# -----------------담기---------------------------
@app.route("/mine/<code>", methods=['GET'])
def mine(code):
    print("HELLO")
    print(code)
    box = list(db.schedule.find({'code':code}))
    
    for b in box:
        subject = b['subject']
        professor = b['professor']
        time_location = b['time_location']
    
    print(subject, professor, time_location)

    mine = {
        'user' : g.user,
        'code' : code,
        'subject' : subject,
        'professor' : professor,
        'time_location' : time_location,

    }
    print(mine)
    db.mySchedule.insert_one(mine)

    return redirect(url_for('mySchedule'))

# ----------공지게시판-------------
@app.route("/professorCommunicateList/<code>", methods=['GET'])
def professorCommunicateList(code):
    

    professorCommunicateInfo = list(db.professorCommunicate.find({},{'_id':0, 'title':1, 'content':1, 'timestamp':1, 'user':1}))

    return render_template('professorCommunicate.html', professorCommunicateInfo = professorCommunicateInfo)


#---------공지게시판 등록---------
@app.route("/professorCommunicateForm", methods=['GET', 'POST'])
def professorCommunicateForm():
    form = ProfessorCommunicateForm

    if request.method == 'POST':
        print("HERE")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        professorCommunicateInfo = {          
            'title': form.title.data,
            'content': form.content.data,
            'timestamp' : timestamp,
            'user' : g.user
        }
        print(professorCommunicateInfo)
        db.professorCommunicate.insert_one(professorCommunicateInfo)


    return render_template('professorCommunicateForm.html', form=form)


if __name__ == '__main__':
    app.run("0.0.0.0", port=5050, debug=True)