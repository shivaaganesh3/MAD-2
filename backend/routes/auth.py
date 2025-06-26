"""
Authentication API routes for login, logout, and registration
Backend-focused with JSON responses
"""

from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Admin, db
from datetime import datetime
import re

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def validate_email(email):
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Password validation - minimum 6 characters"""
    return len(password) >= 6

@auth_bp.route('/login', methods=['POST'])
def login():
    """Handle user and admin login via JSON API"""
    # Check if already logged in
    if current_user.is_authenticated:
        return jsonify({
            'success': True,
            'message': 'Already logged in',
            'user': current_user.to_dict(),
            'redirect_to': get_dashboard_route(current_user)
        }), 200
    
    # Get JSON data
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'No JSON data provided'
        }), 400
    
    # Validate required fields
    username = data.get('username', '').strip()
    password = data.get('password', '')
    user_type = data.get('user_type', 'user').lower()
    
    if not username or not password:
        return jsonify({
            'success': False,
            'message': 'Username and password are required'
        }), 400
    
    if user_type not in ['user', 'admin']:
        return jsonify({
            'success': False,
            'message': 'Invalid user type. Must be "user" or "admin"'
        }), 400
    
    try:
        user_obj = None
        
        if user_type == 'admin':
            # Admin login
            user_obj = Admin.query.filter_by(username=username).first()
            if user_obj and user_obj.check_password(password):
                # Update last login time
                user_obj.last_login = datetime.utcnow()
                db.session.commit()
                
                login_user(user_obj, remember=True)
                
                return jsonify({
                    'success': True,
                    'message': f'Welcome back, Admin {user_obj.username}!',
                    'user': user_obj.to_dict(),
                    'redirect_to': '/api/dashboard/admin'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid admin credentials'
                }), 401
        
        else:
            # User login
            user_obj = User.query.filter_by(username=username).first()
            if user_obj and user_obj.check_password(password):
                if not user_obj.is_active:
                    return jsonify({
                        'success': False,
                        'message': 'Account is deactivated. Please contact admin.'
                    }), 403
                
                login_user(user_obj, remember=True)
                
                return jsonify({
                    'success': True,
                    'message': f'Welcome back, {user_obj.full_name}!',
                    'user': user_obj.to_dict(),
                    'redirect_to': '/api/dashboard/user'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid user credentials'
                }), 401
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Login failed due to server error'
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Handle user registration (admin registration not allowed)"""
    # Check if already logged in
    if current_user.is_authenticated:
        return jsonify({
            'success': False,
            'message': 'Already logged in. Please logout first.'
        }), 400
    
    # Get JSON data
    data = request.get_json()
    if not data:
        return jsonify({
            'success': False,
            'message': 'No JSON data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['username', 'email', 'full_name', 'password']
    for field in required_fields:
        if not data.get(field, '').strip():
            return jsonify({
                'success': False,
                'message': f'{field.replace("_", " ").title()} is required'
            }), 400
    
    username = data.get('username').strip()
    email = data.get('email').strip()
    full_name = data.get('full_name').strip()
    password = data.get('password')
    phone_number = data.get('phone_number', '').strip() or None
    address = data.get('address', '').strip() or None
    
    # Validate data
    if len(username) < 3 or len(username) > 80:
        return jsonify({
            'success': False,
            'message': 'Username must be between 3 and 80 characters'
        }), 400
    
    if not validate_email(email):
        return jsonify({
            'success': False,
            'message': 'Invalid email format'
        }), 400
    
    if not validate_password(password):
        return jsonify({
            'success': False,
            'message': 'Password must be at least 6 characters long'
        }), 400
    
    if len(full_name) < 2 or len(full_name) > 100:
        return jsonify({
            'success': False,
            'message': 'Full name must be between 2 and 100 characters'
        }), 400
    
    try:
        # Check if username already exists (including admin)
        existing_user = User.query.filter_by(username=username).first()
        existing_admin = Admin.query.filter_by(username=username).first()
        
        if existing_user or existing_admin:
            return jsonify({
                'success': False,
                'message': 'Username already exists. Please choose a different one.'
            }), 409
        
        # Check if email already exists (including admin)
        existing_user_email = User.query.filter_by(email=email).first()
        existing_admin_email = Admin.query.filter_by(email=email).first()
        
        if existing_user_email or existing_admin_email:
            return jsonify({
                'success': False,
                'message': 'Email already registered. Please use a different email.'
            }), 409
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            address=address
        )
        user.set_password(password)
        
        # Add to database
        db.session.add(user)
        db.session.commit()
        
        # Auto-login the new user
        login_user(user, remember=True)
        
        return jsonify({
            'success': True,
            'message': f'Registration successful! Welcome, {user.full_name}!',
            'user': user.to_dict(),
            'redirect_to': '/api/dashboard/user'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Registration failed due to server error'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Handle user and admin logout"""
    user_name = current_user.username if hasattr(current_user, 'username') else 'User'
    logout_user()
    
    return jsonify({
        'success': True,
        'message': f'Logged out successfully. Goodbye, {user_name}!'
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """Get current user/admin profile"""
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    }), 200

@auth_bp.route('/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict(),
            'dashboard_route': get_dashboard_route(current_user)
        }), 200
    else:
        return jsonify({
            'authenticated': False,
            'user': None
        }), 200

def get_dashboard_route(user):
    """Get appropriate dashboard route based on user role"""
    if hasattr(user, 'get_role') and user.get_role() == 'admin':
        return '/api/dashboard/admin'
    else:
        return '/api/dashboard/user' 