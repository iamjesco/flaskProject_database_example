from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projectdb.db"

from models.database import User


@app.route('/')
def home():
	return redirect(url_for('users'))


@app.route('/users/')
def users():
	all_users = db.session.execute(db.select(User).order_by(User.username)).scalars()
	return render_template("userslist.html", all_users=all_users)


@app.route("/users/create", methods=["GET", "POST"])
def add_user():
	if request.method == "POST":
		user = User(
			username=request.form.get('username'),
			email=request.form.get('email'),
		)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('users'))
	return render_template('form.html')


@app.route("/users/<int:userid>")
def find_user(userid):
	user = db.session.execute(db.select(User).filter_by(id=userid)).scalar_one()
	return render_template('user.html', user=user)


if __name__ == '__main__':
	app.run()
