"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """Homepage redirects to list of users."""
    return redirect('/users')

@app.route('/users')
def list_users():
    """List users and show add form."""
    users = db.session.query(User).all()
    return render_template('users.html', users=list(users))
  
@app.route('/users/new', methods=['GET', 'POST'])
def show_add_user_form():
    """Show add form."""
    if request.method == 'GET':
      return render_template('add_user.html')
    else:
      first_name = request.form.get('first-name')
      last_name = request.form.get('last-name')
      image_url = request.form.get('image-url', None)

      if first_name and last_name:
        db.session.add(User(first_name=first_name, last_name=last_name, image_url=image_url))
        db.session.commit()
        return redirect('/users')
      else:
        print(f"Error: {request.form}")
        return "Form submission error", 400

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show user profile."""
    user = User.query.get_or_404(user_id)
    user.full_name = user.get_full_name(user)
    return render_template('user_details.html', user=user)
  
@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def show_edit_user_form(user_id):
    """Show edit form."""
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
      user.full_name = user.get_full_name(user)
      return render_template('edit_user.html', user=user)
    else:
      first_name = request.form.get('first-name')
      last_name = request.form.get('last-name')
      image_url = request.form.get('image-url')

      if first_name and last_name and image_url:
        user.first_name=first_name
        user.last_name=last_name
        user.image_url=image_url
        db.session.commit()
        return redirect('/users')
      else:
        print(f"Error: {request.form}")
        return "Form submission error", 400
  
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user and redirect to user list."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    #db.session.expunge(user)
    return redirect('/users')