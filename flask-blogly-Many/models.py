"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class User(db.Model):
  __tablename__ = 'users'

  def __repr__(self):
    u = self
    return f'<User id={u.id} first_name={u.first_name} last_name={u.last_name} image_url={u.image_url}>'
  
  id = db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
  
  first_name = db.Column(db.String(30),
                  nullable=False)
  
  last_name = db.Column(db.String(30),
                  nullable=False)
  
  image_url = db.Column(db.String(2000),
                  nullable=True,
                  default='https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-4.png')
  
  
  
  @property
  def full_name(self):
    return f'{self.first_name} {self.last_name}'
  
  def delete_user(self):
    deleted_user = User.query.filter_by(first_name='User', last_name='Deleted').first()
  
    for post in self.posts:
        post.user_id = deleted_user.id
        db.session.add(post)
    
    db.session.commit()
    
    db.session.delete(self)
    db.session.commit()
  
class Post(db.Model):
  __tablename__ = 'posts'

  def __repr__(self):
    u = self
    return f'<Post id={u.id} title={u.title} content={u.content} created_at={u.created_at} user_id={u.user_id}>'
  
  id = db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)
  
  title = db.Column(db.String(50),
                  nullable=True)
  
  content = db.Column(db.String(2000),
                  nullable=False)
  
  created_at = db.Column(db.DateTime,default=datetime.utcnow)
  
  user_id = db.Column(db.Integer,
                      db.ForeignKey('users.id'),
                      nullable=False)
  
  user = db.relationship('User', backref='posts')
  
  @property
  def formatted_date(self):
    return self.created_at.strftime("%b %d %Y %H:%M %p")
  
  
class PostTag(db.Model):
  __tablename__ = 'post_tags'

  def __repr__(self):
    u = self
    return f'<Post id={u.id} Tag id={u.tag_id}>'

  post_id = db.Column(db.Integer,
                      db.ForeignKey('posts.id'),
                      primary_key=True)

  tag_id = db.Column(db.Integer,
                  db.ForeignKey('tags.id'),
                  primary_key=True)

  post = db.relationship('Post', backref=db.backref('post_tags', cascade='all, delete-orphan'), overlaps="post,post_tags")
  tag = db.relationship('Tag', backref=db.backref('post_tags', cascade='all, delete-orphan'), overlaps="tag,post_tags")
  
class Tag(db.Model):
  __tablename__ = 'tags'

  def __repr__(self):
    u = self
    return f'<Tag id={u.id} name={u.name}>'

  id = db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)

  name = db.Column(db.String(50),
                  nullable=False, unique=True)
  
  posts = db.relationship('Post', secondary='post_tags', backref='tags', overlaps="post,post_tags")
