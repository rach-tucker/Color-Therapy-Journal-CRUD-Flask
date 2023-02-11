#this imports app from the __init__.py file that contains Flask(__name__)
from app import app
#renders templates by the name given to said template
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LogInForm, ColorForm, EntryForm
from app.models import User, Entry


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    #validate goes through the forms.py validators for sign up form 
    if form.validate_on_submit():
        print('Form Submitted')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        #check if user already exists in User table by using SQLAlchemy query filter
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        if check_user:
            flash('A user with that email and/or username already exists', 'danger')
        #create new user and save to database
        new_user = User(email=email, username=username, password=password)
        #flash message that apppears in alerts {{ message }} and success is {{ category }}
        flash(f'Thank you {new_user.username} for signing up!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        #check table by querying 
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))


@app.route('/color-entry', methods=['GET', 'POST'])
@login_required
def color_entry():
    print("test")
    return render_template('color_entry.html')

@app.route('/create-entry/<entry_color>', methods = ["GET", "POST"])
@login_required
def create_entry(entry_color):
    color_image=Entry.getImage(entry_color)
    form = EntryForm()
    print(entry_color)
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        new_entry = Entry(color=entry_color, title=title, body=body, color_image=Entry.getImage(entry_color), user_id=current_user.id)
        flash(f"{new_entry.title} has been created!", "success")
        return get_entries()
    return render_template('create_entry.html', form=form, color_image=color_image)


@app.route('/entries')
def get_entries():
    entries = Entry.query.filter(Entry.user_id == current_user.id)
    return render_template('entries.html', entries=entries)

@app.route('/entries/<entry_id>')
def get_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        flash(f"an entry with and ID of {entry_id} does not exist", "danger")
        return redirect(url_for('index'))
    return render_template('get_entry.html', entry=entry)

@app.route('/entries/<entry_id>/edit', methods = ["GET", "POST"])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        flash(f"an entry with and ID of {entry_id} does not exist", "danger")
        return redirect(url_for('index'))
    #can only edit if current user is author
    if entry.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return render_template(url_for('index'))
    form = EntryForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        entry.update(title=title, body=body)
        flash(f"{entry.title} has been updated", "success")
        return redirect(url_for('get_entry', entry_id=entry.id))
    if request.method == 'GET':
        form.title.data = entry.title
        form.body.data = entry.body
    return render_template('edit_entry.html', entry=entry, form=form)

@app.route('/entries/<entry_id>/delete')
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get(entry_id)
    if not entry:
        flash(f"An entry with and ID of {entry_id} does not exist", "danger")
        return redirect(url_for('index'))
    if entry.author != current_user:
        flash("You do not have permission to delete this entry", "danger")
        return render_template(url_for('index'))
    entry.delete()
    flash(f"{entry.title} has been deleted", "info")
    return redirect(url_for('index'))