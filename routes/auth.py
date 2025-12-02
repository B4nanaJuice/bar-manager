from flask import Blueprint, request, redirect, url_for, current_app, session, flash, render_template
import os

page = Blueprint(name = 'auth', import_name = __name__, url_prefix = '/auth', template_folder = 'templates', static_folder = 'static')

@page.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':

        current_app.logger.info('Someone is trying to log in.')
        username: str = request.form.get('username')
        password: str = request.form.get('password')

        if username != os.getenv('ADMIN_USERNAME') or password != os.getenv('ADMIN_PASSWORD'):
            current_app.logger.warning('Someone entered wrong credientials.')
            flash('Wrong credientials', 'error')
            return render_template('auth/login.html')
        
        session['auth'] = username
        current_app.logger.info('Someone logged in.')

        if 'redirect' in session:
            return redirect(session.pop('redirect'))
        return redirect(url_for('admin.admin_panel'))
    
    return render_template('auth/login.html')

@page.route('/logout', methods = ['GET'])
def logout():

    if 'auth' in session:
        session.pop('auth')
        current_app.logger.info('Someone logged out.')

    return redirect(url_for('public.home'))