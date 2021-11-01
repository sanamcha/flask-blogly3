"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE ="https://tse1.mm.bing.net/th?id=OIP.WVEv6Qe2gHKa1qk_gzY0UwHaMK&pid=Api&P=0&w=118&h=195"



class User(db.Model):
    """User Table."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False, unique=True)
    last_name = db.Column(db.String, nullable=True)

    image_url = db.Column(db.Text, nullable=False, default = DEFAULT_IMAGE)
    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    @property
    def full_name(self):
        """Return full name"""
        return f"{self.first_name} {self.last_name} "

class Post(db.Model):
    """Post table"""
    __tablename__ ="posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.now )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



class PostTag(db.Model):
    """PostTag table"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)



class Tag(db.Model):
    """Tag table"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', secondary='posts_tags', backref='tags') 



def connect_db(app):
    db.app = app
    db.init_app(app)