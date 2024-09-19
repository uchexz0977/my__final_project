from flask import Flask,render_template,request,session,redirect,url_for
import requests,json
import os
from dotenv import load_dotenv
load_dotenv()
import random
from html import unescape
import firebase_admin
from firebase_admin import credentials,auth
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask import flash, get_flashed_messages




app = Flask(__name__)

app.secret_key  = os.getenv('FLASK_SECRET_KEY')

cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
if cred_path is None:
	raise ValueError("Missing GOOGLE_APPLICATION_CREDENTIALS environment variable")

print("Current Working Directory:", os.getcwd())  # Print the current working directory
print("GOOGLE_APPLICATION_CREDENTIALS:", cred_path)  # Print the path to verify

cred = credentials.Certificate(cred_path)

firebase_admin.initialize_app(cred)
'''Define authentication for users'''
def check_auth():
    user_id = session.get('user_id')
    if not user_id:
        return False
    try:
        auth.get_user(user_id)
        return True
    except:
        return False


''' Initialize questions '''

TOTAL_QUESTIONS = 10  

''' Fetch questions from API '''

def fetch_question():   
    response = requests.get('https://opentdb.com/api.php?amount=10&category=17&difficulty=hard&type=multiple')
    data = response.json()
    question_info = data['results'][0]
    question = unescape(question_info['question'])
    correct_answer = unescape(question_info['correct_answer'])
    incorrect_answers = [unescape(ans) for ans in question_info['incorrect_answers']]
    all_answers = incorrect_answers + [correct_answer]
    random.shuffle(all_answers)
    return question, correct_answer, all_answers

''' Define forms '''

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Signup')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
    
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

'''Define  app routes '''

@app.route('/signup', methods=['GET', 'POST'])
def  Signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            user = auth.create_user(
                email=email,
                password=password
            )            
            flash('You have successfully registered!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Registration failed. Please try again.', 'error')            
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            response = requests.post(
                'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
                params={'key': 'AIzaSyAHtMKSJmPonfI-1GK8g6PMQ9BE405BYW4',},  
                json={
                    'email': email,
                    'password': password,
                    'returnSecureToken': True
                }
            )
            user_data = response.json()
            if 'idToken' in user_data:                
                session['user_id'] = user_data['localId']
                flash('You have successfully logged in!', 'success')
                return redirect(url_for('index'))
            else:                
                error_message = user_data.get('error', {}).get('message', 'Login failed. Please try again.')
                flash(error_message, 'danger')
        except Exception as e:
            flash('An error occurred during login. Please try again later.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()  
    return redirect(url_for('home'))



@app.route('/request-password-reset', methods=['GET'])
def request_password_reset():   
    return render_template('password_reset_request.html')    


@app.route('/')
def home():
    return render_template('home.html')  


@app.route('/index', methods=['GET', 'POST'])
def index(): 
    if not check_auth():        
        return redirect(url_for('login'))

    session.setdefault('attempted_count', 0)
    session.setdefault('correct_count', 0)

    if session['attempted_count'] >= TOTAL_QUESTIONS:
        return render_template('quiz_completed.html', correct_count=session['correct_count'], total_questions=TOTAL_QUESTIONS)
    
    if request.method == 'POST':
        user_answer = request.form.get('answers')
        correct_answer = session.get('correct_answer')
        if user_answer == correct_answer:
            session['correct_count'] += 1
            message = "Correct!"
        else:
            message = f"Incorrect! The correct answer was {correct_answer}."  
    else:
        message = None
    
    
    if request.method == 'GET' or session.get('fetch_new', True):
        question, correct_answer, all_answers = fetch_question()
        session['correct_answer'] = correct_answer
        session['current_question'] = question
        session['current_answers'] = all_answers
        session['fetch_new'] = False
    else:
        question = session['current_question']
        all_answers = session['current_answers']
    
    return render_template('index.html', question=question, answers=all_answers, message=message, correct_count=session['correct_count'], attempted_count=session['attempted_count'], total_questions=TOTAL_QUESTIONS)


@app.route('/next')
def next_question():
    if session.get('attempted_count', 0) < TOTAL_QUESTIONS:
        session['attempted_count'] += 1
        session['fetch_new'] = True
    return redirect(url_for('index'))


@app.route('/restart')
def restart_quiz():
    session['attempted_count'] = 0
    session['correct_count'] = 0
    session['fetch_new'] = True
    return redirect(url_for('index'))
   
""" Error handler """
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error=error), 500



if __name__ == '__main__':    
    app.run(debug=True, Port=8000)
