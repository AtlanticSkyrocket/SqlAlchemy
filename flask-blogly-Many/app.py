"""Blogly application."""
from flask import Flask, redirect, render_template, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag

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
    users = db.session.query(User).filter(User.first_name != 'User', User.last_name != 'Deleted').order_by(User.first_name.asc()).all()
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
    return render_template('user_details.html', user=user)
  
@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def show_edit_user_form(user_id):
    """Show edit form."""
    user = User.query.get_or_404(user_id)
    if request.method == 'GET':
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
    user.delete_user()
    return redirect('/users')
  
  
"""sumary_line
Tags  """  
  
    
@app.route('/tags')
def list_tags():
    """List users and show add form."""
    tags = db.session.query(Tag).order_by(Tag.name.asc()).all()
    return render_template('tags.html', tags=list(tags))
  
@app.route('/tags/new', methods=['GET', 'POST'])
def show_add_tag_form():
    """Show add form."""
    if request.method == 'GET':
      return render_template('add_tag.html')
    else:
      name = request.form.get('name')

      if name:
        db.session.add(Tag(name=name))
        db.session.commit()
        return redirect('/tags')
      else:
        print(f"Error: {request.form}")
        return "The form had missing data.", 400

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show tag profile."""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag_details.html', tag=tag, posts=posts)
  
@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def show_edit_tag_form(tag_id):
    """Show edit form."""
    tag = Tag.query.get_or_404(tag_id)
    if request.method == 'GET':
      return render_template('edit_tag.html', tag=tag)
    else:
      name = request.form.get('name')

      if name:
        tag.name=name
        db.session.add(tag)
        db.session.commit()
        return redirect('/tags')
      else:
        print(f"Error: {request.form}")
        return "Error updating tag", 400
  
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete user and redirect to tag list."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
  
  
  
"""sumary_line
"""
@app.route('/posts')
def list_posts():
    """List posts and shows add form."""
    posts = db.session.query(Post).order_by(Post.created_at.desc()).all()
    return render_template('posts.html', posts=list(posts), Post=Post)
  
@app.route('/posts/new', methods=['GET', 'POST'])
def show_add_post_form():
    """Show add form."""
    user_id = request.args.get('id') 
    if request.method == 'GET':
      user = User.query.get_or_404(user_id)
      return render_template('add_post.html', user=user, tags=list(Tag.query.all()))
    else:
      title = request.form.get('title')
      content = request.form.get('content')
      selected_tags = request.form.getlist('tags')
      tags = Tag.query.filter(Tag.id.in_(selected_tags)).all()
      if title and content:
        db.session.add(Post(title=title, content=content, user_id=user_id, tags=tags))
        db.session.commit()
        return redirect('/posts')
      else:
        print(f"Error: {request.form}")
        return "The form had missing data.", 400

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show post profile."""
    post = Post.query.get_or_404(post_id)
    tags = list(Tag.query.all())
    return render_template('post_details.html', post=post, tags=tags)
  
@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def show_edit_post_form(post_id):
    """Show edit form."""
    post = Post.query.get_or_404(post_id)
    user = post.user 
    if request.method == 'GET':
      tags = list(Tag.query.all())
      return render_template('edit_post.html', post=post, tags=tags, user=user)
    else:
      title = request.form.get('title')
      content = request.form.get('content')
      selected_tags = request.form.getlist('tags')
      tags = Tag.query.filter(Tag.id.in_(selected_tags)).all()
      if title or  content or tags:
        post.title = title if title else post.title
        post.content = content if content else post.content
        post.tags = tags if tags else post.tags
        db.session.add(post)
        db.session.commit()
        return redirect('/posts')
      else:
        print(f"Error: {request.form}")
        return "Error updating post", 400
  
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete user and redirect to post list."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')