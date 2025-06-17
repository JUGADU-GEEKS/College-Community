from flask import session, redirect, url_for

def is_logged_in():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
