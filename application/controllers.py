from flask import Flask, render_template, request, redirect
from flask import current_app as app
from .models import *


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            username = request.form.get('username')
            pwd = request.form.get('pwd')
            this_user = User.query.filter_by(username=username).first()
            if this_user:
                if this_user.password == pwd:
                    if this_user.type == 'admin':
                        return render_template('admin_dash.html', username=username)
                    else:
                        return render_template('user_dash.html', username=username)
                else:
                    return "Invalid password"
            else:
                return """User does not exist:
                <a href='/register'>Register</a>"""
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        fullname = request.form.get('fullname')
        qualification = request.form.get('qualification')
        dob = request.form.get('dob')
        this_user = User.query.filter_by(username=username).first()
        if this_user:
            return """User already exists:
            <a href='/login'>Login</a>"""
        else:
            new_user = User(username=username, password=pwd, full_name=fullname, qualification=qualification, date_of_birth=dob)
            db.session.add(new_user)
            db.session.commit()
        return redirect('/login')
    return render_template('register.html')