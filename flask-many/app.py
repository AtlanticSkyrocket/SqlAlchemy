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