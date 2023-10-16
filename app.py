from flask import Flask, render_template, redirect, url_for, session, request, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired
from flask_bcrypt import Bcrypt

app = Flask(__name__)
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:system@localhost/users'
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)

class Authenticate(db.Model, UserMixin):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.username} - {self.password}"
    def get_id(self):
        return str(self.sno)

@login_manager.user_loader
def load_user(user_id):
    return Authenticate.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']

        user = Authenticate.query.filter_by(username=uname).first()
        if user and user.password==pwd:
            login_user(user)
            if current_user.is_authenticated:
                flash('Login Successful!','info')
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template("login.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html") 

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('login'))

@app.route('/addstudent')
def to_addStudent():
    return render_template('addStudent.html')

if __name__ == "__main__":
    app.run(debug=True)