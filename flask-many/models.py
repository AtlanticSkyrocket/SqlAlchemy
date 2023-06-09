"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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