from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
       if not value or len(value.strip()) == 0:
        raise ValueError("Author name cannot be empty")
       existing_author = Author.query.filter_by(name=value).first()
       if existing_author:
        raise ValueError(f"Author name '{value}' is already taken")
       return value


    @validates('phone_number')
    def validate_phone_number(self, key, value):
        """Ensure phone number is exactly 10 digits"""
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value

    def __repr__(self):
        return f'<Author id={self.id}, name={self.name}>'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, value):
        """Ensure content is at least 250 characters"""
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        """Ensure summary is at most 250 characters"""
        if len(value) > 250:
            raise ValueError("Post summary must be 250 characters or less")
        return value

    @validates('category')
    def validate_category(self, key, value):
        """Ensure category is either Fiction or Non-Fiction"""
        if value not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'")
        return value

    @validates('title')
    def validate_title(self, key, value):
        """Ensure title contains clickbait phrases"""
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in value for phrase in clickbait_words):
            raise ValueError("Title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return value

    def __repr__(self):
        return f'<Post id={self.id}, title={self.title}>'
