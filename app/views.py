from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, PostForm
from .models import User, Post
from config import POSTS_PER_PAGE
import datetime


@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
	user = g.user
	p = Post.query.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
	return render_template('index.html',
							title='Home',
							user=user,
							posts=p)

@app.route('/login', methods=['GET', 'POST'])
def login():
	u = User.query.get(1)
	if request.method == 'GET':
		return render_template('login.html')
	form = LoginForm()
	username = request.form['username']
	password = request.form['password']
	registered_user = User.query.filter_by(username=username,password=password).first()
	if registered_user is None:
		flash('Username or Password is invalid' , 'error')
		return redirect(url_for('login'))
	if login_user(registered_user):
		return redirect(url_for('index'))
	return render_template('login.html', 
							title='Sign In',
							form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
	form = PostForm()
	if form.validate_on_submit():
		#u = User.query.get(1)
		post = Post(body = form.post.data, title = form.title.data, timestamp = datetime.datetime.utcnow(), author = g.user)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('add_post.html',
							title='Add post',
							form=form)

@app.route('/delete_post<int:id>')
@login_required
def delete_post(id=0):
	p = Post.query.get(id)
	db.session.delete(p)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/post_<int:id>')
def read_more(id=0):
	#p = Post.query.filter_by(id=id).first()
	p = Post.query.get(id)
	return render_template('read_more.html',
							post=p)
