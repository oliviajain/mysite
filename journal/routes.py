from flask import Flask, Blueprint, render_template, request, redirect, url_for
from .database import init_db, db, User, Answer
from .questions import QUESTIONS

journal_bp = Blueprint('journal', __name__, url_prefix='/journal')


@journal_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_name = request.form['name']
        user = User.query.filter_by(name=user_name).first()
        if user:
            return redirect(url_for('journal.questions', user_id=user.id))
        else:
            user = User(name=user_name)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('journal.questions', user_id=user.id))

    return render_template('journal/home.html')


@journal_bp.route('/questions/<int:user_id>', methods=['GET', 'POST'])
def questions(user_id):
    user = User.query.get_or_404(user_id)

    if user.current_question >= len(QUESTIONS):
        return redirect(url_for('thanks', user_id=user.id))

    current_question_text = QUESTIONS[user.current_question]

    if request.method == 'POST':
        answer_text = request.form['answer']
        answer = Answer(
            question=current_question_text,
            answer=answer_text,
            user_id=user.id)
        db.session.add(answer)

        user.current_question += 1
        db.session.commit()

        return redirect(url_for('journal.questions', user_id=user.id))

    return render_template(
        'journal/questions.html',
        question=current_question_text,
        user=user)


@journal_bp.route('/thanks/<int:user_id>')
def thanks(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('journal/thanks.html', user=user)


@journal_bp.route('/responses/<int:user_id>')
def responses(user_id):
    user = User.query.get_or_404(user_id)
    answers = Answer.query.filter_by(user_id=user.id).all()
    return render_template('journal/responses.html', user=user, answers=answers)
