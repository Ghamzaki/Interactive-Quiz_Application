from flask import Flask, render_template, redirect, request, session
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key for session management

# Firebase Configuration
firebaseConfig = {
    "apiKey": "AIzaSyBk6-VhDoOiXXTig9eUSUMPRWTzMoPf7Ns",
    "authDomain": "interactive-quiz-applica-ff179.firebaseapp.com",
    "projectId": "interactive-quiz-applica-ff179",
    "storageBucket": "interactive-quiz-applica-ff179.appspot.com",
    "messagingSenderId": "796048412407",
    "appId": "1:796048412407:web:5a53f1de3fcc97735a4df2",
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']
            return redirect('/quiz')
        except:
            return "Login Failed"
    return render_template('login.html')

# Quiz Page
@app.route('/quiz')
def quiz():
    if 'user' in session:
        # Get quiz questions from Firebase
        quiz_data = db.child("quizzes").get().val()
        return render_template('quiz.html', quiz_data=quiz_data)
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
