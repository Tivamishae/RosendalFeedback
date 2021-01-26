from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hugo:Hugo1234@localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://bvxygbbufczhma:b4d1ef65b596b562560f39644072151667fd2e7091b0b7f09d333a835e084c2b@ec2-54-159-113-254.compute-1.amazonaws.com:5432/d4rq0hqcqep6l0'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String(200), unique=True)
    SSID = db.Column(db.Float, unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, student, SSID, dealer, rating, comments):
        self.student = student
        self.SSID = SSID
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        student = request.form['student']
        SSID = request.form['SSID']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        if student == '' or SSID == '':
            return render_template('index.html', message='Var vänlig och fyll i alla fält.')
        if db.session.query(Feedback).filter(Feedback.student == student).count() == 0:
            data = Feedback(student, SSID, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(student, SSID, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='Du har redan skickat feedback.')

if __name__ == '__main__':
    app.run()