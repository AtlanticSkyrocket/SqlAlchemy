import unittest
from app import app
from models import db, connect_db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
with app.app_context():
  db.drop_all()
  db.create_all()

class BloglyTestCase(unittest.TestCase):
  """Test for model for Users."""
  
  def setUp(self):
    """CLean up any existing users."""
    with app.app_context():
      User.query.delete()
    
  def tearDown(self):
    """Clean up any fouled transaction."""
    with app.app_context():
      db.session.rollback()
    
  def test_get_full_name(self):
    """Test get_full_name method."""
    with app.app_context():
      user = User(first_name='Test', last_name='User')
      self.assertEqual(user.get_full_name(user), 'Test User') 

  def test_homepage_redirect(self):
    """Test that the homepage redirects to list of users."""
    with app.app_context(), app.test_client() as client:
      response = client.get('/')
      self.assertEqual(response.status_code, 302)
      self.assertEqual(response.location, '/users')

  def test_list_users(self):
    """Test that the list users route returns the correct status code."""
    with app.app_context(), app.test_client() as client:
      response = client.get('/users')
      self.assertEqual(response.status_code, 200)

  def test_add_user(self):
    """Test adding a new user."""
    with app.app_context(), app.test_client() as client:
      response = client.post('/users/new', data={
          'first-name': 'John',
          'last-name': 'Doe',
          'image-url': 'https://example.com/image.jpg'
      }, follow_redirects=True)
      self.assertEqual(response.status_code, 200)
      self.assertIn(b'John Doe', response.data)

  def test_delete_user(self):
    """Test deleting a user."""
    # Create a user to delete
    with app.app_context():
      user = User(first_name='John', last_name='Doe',
                  image_url='https://example.com/image.jpg')
      db.session.add(user)
      db.session.commit()

      # Delete the user
      with app.test_client() as client:
        response = client.post(
            f'/users/{user.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)        
        deleted_user = User.query.get(user.id)
        self.assertIsNone(deleted_user)
