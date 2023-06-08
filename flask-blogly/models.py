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
  
  first_name = db.Column(db.String(30),
                  nullable=False)
  
  last_name = db.Column(db.String(30),
                  nullable=False)
  
  image_url = db.Column(db.String(200),
                  nullable=True,
                  default='https://www.freeiconspng.com/uploads/person-icon-user-person-man-icon-4.png')
  
  
  
  @classmethod
  def get_full_name(self, user):
    return f'{user.first_name} {user.last_name}'