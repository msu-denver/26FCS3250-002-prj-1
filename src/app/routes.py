'''
CS3250 - Software Development Methods and Tools
Instructor: Thyago Mota
Student: 
Description: Project 1 - GPA Calculator
'''

from app import app, db
from app.models import User, Course, Enrollment
from app.forms import SignUpForm, LoginForm, EnrollmentForm, DeleteEnrollmentForm, UpdateEnrollmentForm
from gpa_calculator import calculate_gpa
from flask import render_template, redirect, url_for, request
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    return render_template('index.html')

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    from app.forms import SignUpForm
    form = SignUpForm()
    if form.validate_on_submit():
        if form.passwd.data != form.passwd_confirm.data:
            return redirect(url_for('error_page'))
        hashed = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
        user = User(
            id=form.id.data,
            name=form.name.data,
            about=form.about.data,
            passwd=hashed
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('list_enrollments'))
    return render_template('signup.html', form=form)
    
@app.route('/users/login', methods=['GET', 'POST'])
def login():
    from app.forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and user.passwd and bcrypt.checkpw(form.passwd.data.encode('utf-8'), user.passwd):
            login_user(user)
            return redirect(url_for('list_enrollments'))
    return render_template('login.html', form=form)

@app.route('/users/signout', methods=['GET', 'POST'])
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/users/error', methods=['GET'])
def error_page():
    return render_template('error.html')

@app.route('/enrollments')
@login_required
def list_enrollments():
    enrollments = current_user.enrollments
    gpa = calculate_gpa(enrollments)
    delete_form = DeleteEnrollmentForm()
    return render_template('enrollments.html', enrollments=enrollments, gpa=gpa, delete_form=delete_form)

@app.route('/enrollments/delete/<course_prefix>/<course_number>', methods=['POST'])
@login_required
def delete_enrollment(course_prefix, course_number):
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_prefix=course_prefix,
        course_number=course_number
    ).first()
    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()
    return redirect(url_for('list_enrollments'))

@app.route('/enrollments/update/<course_prefix>/<course_number>', methods=['GET', 'POST'])
@login_required
def update_enrollment(course_prefix, course_number):
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        course_prefix=course_prefix,
        course_number=course_number
    ).first()
    if not enrollment:
        return redirect(url_for('list_enrollments'))
    form = UpdateEnrollmentForm()
    if form.validate_on_submit():
        enrollment.grade = form.grade.data
        db.session.commit()
        return redirect(url_for('list_enrollments'))
    if request.method == 'GET':
        form.grade.data = enrollment.grade
    return render_template('update_enrollment.html', form=form, course=enrollment.course)

@app.route('/enrollments/create', methods=['GET', 'POST'])
@login_required
def create_enrollment():
    from app.forms import EnrollmentForm
    form = EnrollmentForm()
    # populate course choices
    courses = Course.query.order_by(Course.prefix, Course.number).all()
    form.course.choices = [
        (f"{c.prefix}-{c.number}", f"{c.prefix} {c.number} - {c.name} ({c.credits} cr)")
        for c in courses
    ]
    if form.validate_on_submit():
        try:
            course_value = form.course.data  # e.g. "CS-1050"
            if '-' in course_value:
                prefix, number = course_value.split('-', 1)
            else:
                # fallback
                parts = course_value.split()
                prefix, number = parts[0], parts[1] if len(parts) > 1 else ''
            enrollment = Enrollment(
                user_id=current_user.id,
                course_prefix=prefix,
                course_number=number,
                grade=form.grade.data
            )
            db.session.add(enrollment)
            db.session.commit()
        except Exception:
            db.session.rollback()
        return redirect(url_for('list_enrollments'))
    return render_template('create_enrollment.html', form=form)