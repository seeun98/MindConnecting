from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserCreateForm(FlaskForm):
    userid = StringField('아이디', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')
    ])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    name = StringField('이름', validators=[DataRequired(), Length(min=3, max=25)])
    email = EmailField('이메일', [DataRequired(), Email()])
    is_student = SelectField('학생/교수',
                            choices=['Professor', 'Student', 'Other'],
                            validators = [DataRequired()])
    department = StringField('학과', validators=[DataRequired(), Length(min=2, max=25)])


class UserLoginForm(FlaskForm):
    userid = StringField('아이디', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])


class ProfessorOfficeForm(FlaskForm):
    name = StringField('이름', validators=[DataRequired(), Length(min=3, max=25)])
    status = SelectField('재실 여부',
                         choices=['재실', '퇴근', '연구중', '휴식중'],
                         validators=[DataRequired()])


class CommunicateForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired(), Length(min=3, max=25)])
    content = StringField('내용', validators=[DataRequired(), Length(max=140)])

class CommunicateReForm(FlaskForm):
    REcontent = StringField('내용', validators=[DataRequired(), Length(max=140)])

class ProfessorCommunicateForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired(), Length(min=3, max=25)])
    content = StringField('내용', validators=[DataRequired(), Length(max=1000)])