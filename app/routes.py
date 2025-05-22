from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Transaction, SavingsGoal
from app.forms import LoginForm, SignupForm, TransactionForm, SavingsGoalForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index') # Common alias for homepage
@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page displaying user's financial overview."""
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    user_goals = SavingsGoal.query.filter_by(user_id=current_user.id).order_by(SavingsGoal.name).all()
    
    total_income = sum(t.amount for t in user_transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in user_transactions if t.type == 'expense')
    balance = total_income - total_expenses
    
    # Data for charts (example structure, actual charting library will dictate format)
    # Spending by category
    spending_categories = {}
    for t in user_transactions:
        if t.type == 'expense':
            spending_categories[t.category] = spending_categories.get(t.category, 0) + t.amount
    
    # Income vs Expense trend (simplified - could be monthly)
    # This would typically require more complex querying/processing for a real chart
    income_vs_expense_data = {
        "labels": ["Total Income", "Total Expenses"],
        "values": [total_income, total_expenses]
    }

    return render_template('dashboard.html', title='Dashboard', 
                           transactions_summary=user_transactions[:5], # Show recent 5 transactions
                           goals=user_goals,
                           total_income=total_income, total_expenses=total_expenses, balance=balance,
                           spending_categories=spending_categories,
                           income_vs_expense_data=income_vs_expense_data)

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! Please login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('signup.html', title='Sign Up', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page) if next_page and next_page.startswith('/') else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
@login_required
def logout():
    """Logs out the current user."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

# Transaction Routes
@main.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    """Page to view and add transactions."""
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            user_id=current_user.id,
            type=form.type.data,
            category=form.category.data,
            amount=form.amount.data,
            date=form.date.data, # WTForms DateField provides a datetime.date object
            description=form.description.data
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('main.transactions'))
    
    page = request.args.get('page', 1, type=int)
    user_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).paginate(page=page, per_page=10)
    return render_template('transactions.html', title='Transactions', form=form, transactions_pagination=user_transactions, current_page_name='transactions')

@main.route('/transactions/edit/<int:transaction_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    """Page to edit an existing transaction."""
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        abort(403) 
    form = TransactionForm(obj=transaction) # Pre-populate form
    if form.validate_on_submit():
        transaction.type = form.type.data
        transaction.category = form.category.data
        transaction.amount = form.amount.data
        transaction.date = form.date.data
        transaction.description = form.description.data
        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('main.transactions'))
    # For rendering, we can pass the form and indicate it's an edit operation
    return render_template('edit_transaction.html', title='Edit Transaction', form=form, transaction_id=transaction_id)

@main.route('/transactions/delete/<int:transaction_id>', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    """Deletes a transaction."""
    transaction = Transaction.query.get_or_404(transaction_id)
    if transaction.user_id != current_user.id:
        abort(403)
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('main.transactions'))

# Savings Goal Routes
@main.route('/savings-goals', methods=['GET', 'POST'])
@login_required
def savings_goals():
    """Page to view and add savings goals."""
    form = SavingsGoalForm()
    if form.validate_on_submit():
        goal = SavingsGoal(
            user_id=current_user.id,
            name=form.name.data,
            target_amount=form.target_amount.data,
            current_amount=form.current_amount.data,
            deadline=form.deadline.data if form.deadline.data else None # Handle optional date
        )
        db.session.add(goal)
        db.session.commit()
        flash('Savings goal added successfully!', 'success')
        return redirect(url_for('main.savings_goals'))
    
    user_goals = SavingsGoal.query.filter_by(user_id=current_user.id).order_by(SavingsGoal.name).all()
    return render_template('savings_goals.html', title='Savings Goals', form=form, goals=user_goals, current_page_name='savings_goals')

@main.route('/savings-goals/edit/<int:goal_id>', methods=['GET', 'POST'])
@login_required
def edit_savings_goal(goal_id):
    """Page to edit an existing savings goal."""
    goal = SavingsGoal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        abort(403)
    form = SavingsGoalForm(obj=goal) # Pre-populate form
    if form.validate_on_submit():
        goal.name = form.name.data
        goal.target_amount = form.target_amount.data
        goal.current_amount = form.current_amount.data
        goal.deadline = form.deadline.data if form.deadline.data else None
        db.session.commit()
        flash('Savings goal updated successfully!', 'success')
        return redirect(url_for('main.savings_goals'))
    return render_template('edit_savings_goal.html', title='Edit Savings Goal', form=form, goal_id=goal_id)

@main.route('/savings-goals/delete/<int:goal_id>', methods=['POST'])
@login_required
def delete_savings_goal(goal_id):
    """Deletes a savings goal."""
    goal = SavingsGoal.query.get_or_404(goal_id)
    if goal.user_id != current_user.id:
        abort(403)
    db.session.delete(goal)
    db.session.commit()
    flash('Savings goal deleted successfully!', 'success')
    return redirect(url_for('main.savings_goals'))
