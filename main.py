from flask import Flask, flash, render_template, request, redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask.db"
app.secret_key='ygrenys'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Notes(db.Model):
	id = db.Column(db.Integer, primary_key = True) #primary_key - первичный ключ
	title = db.Column(db.String, nullable=False) #unique - уникальность каждой записи, nullable - непустое значение
	subtitle = db.Column(db.String)
	text = db.Column(db.String, nullable=False)

class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password_hash = db.Column(db.String, nullable=False)
	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

def generate_token():
	return secrets.token_hex()

@app.route("/")
def index():
	return render_template('index.html')

@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method == 'POST':
		usr = request.form['username']
		email = request.form['email']
		pwd = request.form['password']

		user = Users(username=usr, email=email)
		user.set_password(pwd)
		db.session.add(user)
		db.session.commit()
		
		return redirect(url_for('login'))
	else:
		return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		email = request.form['email']
		password = request.form['password']
		user = Users.query.filter_by(email=email).first()
		if not user or not user.check_password(password):
			return "Неверный email или пароль"
		else:
			token = generate_token()
			return redirect(url_for('index'))

#Очистка\удаление всех сообщений в дневнике
@app.route('/delete')
def delete_messages():
	db.session.query(Notes).delete()
	db.session.commit()
	return "<b>Все сообщения удалены.</b><br><a href='/'>На главную</a><br><a href='note'>Назад</a>"

#Форма дневник программиста
@app.route("/note", methods=["GET", "POST"])
def note():
	result = db.session.execute(db.select(Notes)).scalars()
	notes = result.all()

	if request.method == 'POST':
		message = Notes(title=request.form['title'], subtitle=request.form['subtitle'], text=request.form['string'])
		db.session.add(message)
		db.session.commit()
		return redirect(url_for('note', notes=notes))
	return render_template('/note.html', notes=notes)

@app.errorhandler(404)
def not_found(e):
	return render_template('/templates/404.html', 404)

if __name__ == "__main__":
	app.run(debug=True)