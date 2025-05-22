from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db # Import db from the app package (__init__.py)

# Note: The user_loader is typically defined in __init__.py where login_manager is configured.
# If it's also here, ensure it's not causing conflicts. The one in __init__.py is preferred.

class User(UserMixin, db.Model):
    """User model for storing user accounts."""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    # Relationships
    # 'dynamic' allows for further querying on the relationship
    # cascade='all, delete-orphan' ensures related objects are deleted/orphaned when a user is deleted
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    savings_goals = db.relationship('SavingsGoal', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Transaction(db.Model):
    """Transaction model for income and expenses."""
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    description = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Transaction {self.id} {self.type} {self.amount} for User {self.user_id}>'

class SavingsGoal(db.Model):
    """SavingsGoal model for tracking financial goals."""
    __tablename__ = 'savings_goals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, nullable=False, default=0.0)
    deadline = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<SavingsGoal {self.name} Target: {self.target_amount} for User {self.user_id}>'
