from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models import User, Quiz, Question, Choice, QuizResult
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    quizzes = Quiz.query.all()
    return render_template('home.html', quizzes=quizzes)

@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route("/quiz/<int:quiz_id>")
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', title=quiz.title, quiz=quiz)

@main.route("/quiz/<int:quiz_id>/submit", methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    correct_answers = 0
    for question in quiz.questions:
        selected_choice = request.form.get(str(question.id))
        if selected_choice:
            choice = Choice.query.get(selected_choice)
            if choice and choice.correct:
                correct_answers += 1
    score = (correct_answers / len(quiz.questions)) * 100
    result = QuizResult(score=score, user_id=current_user.id, quiz_id=quiz.id)
    db.session.add(result)
    db.session.commit()
    flash(f'You scored {score}%!', 'success')
    return redirect(url_for('main.home'))
