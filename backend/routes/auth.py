"""
JWT-based Authentication API routes for Vehicle Parking System
Provides secure token-based authentication with role-based access control
"""

from flask import Blueprint, request, jsonify
from auth_utils import JWTAuth, AuthError, token_required, get_current_user
from models import User, Admin
from database import db
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

def validate_username(username):
    """Username validation"""
    if not username or len(username) < 3 or len(username) > 80:
        return False
    # Only allow alphanumeric characters and underscores
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None

@auth_bp.route('/login', methods=['POST'])
def login():
    """Handle user and admin login via JWT authentication"""
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided',
                'error_code': 'INVALID_REQUEST'
            }), 400
        
        # Validate required fields
        username = data.get('username', '').strip()
        password = data.get('password', '')
        user_type = data.get('user_type', 'user').lower()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required',
                'error_code': 'MISSING_CREDENTIALS'
            }), 400
        
        if user_type not in ['user', 'admin']:
            return jsonify({
                'success': False,
                'message': 'Invalid user type. Must be "user" or "admin"',
                'error_code': 'INVALID_USER_TYPE'
            }), 400
        
        # Authenticate user
        try:
            user = JWTAuth.authenticate_user(username, password, user_type)
            
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'Invalid credentials',
                    'error_code': 'INVALID_CREDENTIALS'
                }), 401
            
            # Generate JWT token
            token = JWTAuth.generate_token(user)
            
            # Prepare response
            response_data = {
                'success': True,
                'message': f'Welcome back, {user.username}!',
                'token': token,
                'user': user.to_dict(),
                'expires_in': 168 * 60 * 60  # 7 days in seconds
            }
            
            # Add role-specific redirect
            if user.get_role() == 'admin':
                response_data['redirect_to'] = '/admin/dashboard'
            else:
                response_data['redirect_to'] = '/user/dashboard'
            
            return jsonify(response_data), 200
            
        except AuthError as e:
            return jsonify({
                'success': False,
                'message': e.message,
                'error_code': 'AUTH_ERROR'
            }), e.status_code
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Login failed due to server error',
            'error_code': 'SERVER_ERROR'
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Handle user registration (admin registration not allowed)"""
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided',
                'error_code': 'INVALID_REQUEST'
            }), 400
        
        # Validate required fields
        required_fields = ['username', 'email', 'full_name', 'password']
        for field in required_fields:
            if not data.get(field, '').strip():
                return jsonify({
                    'success': False,
                    'message': f'{field.replace("_", " ").title()} is required',
                    'error_code': 'MISSING_FIELD'
                }), 400
        
        username = data.get('username').strip()
        email = data.get('email').strip().lower()
        full_name = data.get('full_name').strip()
        password = data.get('password')
        phone_number = data.get('phone_number', '').strip() or None
        address = data.get('address', '').strip() or None
        
        # Validate data
        if not validate_username(username):
            return jsonify({
                'success': False,
                'message': 'Username must be 3-80 characters and contain only letters, numbers, and underscores',
                'error_code': 'INVALID_USERNAME'
            }), 400
        
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email format',
                'error_code': 'INVALID_EMAIL'
            }), 400
        
        if not validate_password(password):
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters long',
                'error_code': 'INVALID_PASSWORD'
            }), 400
        
        if len(full_name) < 2 or len(full_name) > 100:
            return jsonify({
                'success': False,
                'message': 'Full name must be between 2 and 100 characters',
                'error_code': 'INVALID_FULL_NAME'
            }), 400
        
        # Check if username already exists (including admin)
        existing_user = User.query.filter_by(username=username).first()
        existing_admin = Admin.query.filter_by(username=username).first()
        
        if existing_user or existing_admin:
            return jsonify({
                'success': False,
                'message': 'Username already exists. Please choose a different one.',
                'error_code': 'USERNAME_EXISTS'
            }), 409
        
        # Check if email already exists (including admin)
        existing_user_email = User.query.filter_by(email=email).first()
        existing_admin_email = Admin.query.filter_by(email=email).first()
        
        if existing_user_email or existing_admin_email:
            return jsonify({
                'success': False,
                'message': 'Email already registered. Please use a different email.',
                'error_code': 'EMAIL_EXISTS'
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
        
        # Generate JWT token for immediate login
        token = JWTAuth.generate_token(user)
        
        return jsonify({
            'success': True,
            'message': f'Registration successful! Welcome, {user.full_name}!',
            'token': token,
            'user': user.to_dict(),
            'redirect_to': '/user/dashboard',
            'expires_in': 168 * 60 * 60  # 7 days in seconds
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Registration failed due to server error',
            'error_code': 'SERVER_ERROR'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """Handle user and admin logout"""
    current_user = get_current_user()
    user_name = current_user.username if current_user else 'User'
    
    # Note: With JWT, we can't invalidate tokens server-side easily.
    # In a production environment, you might want to implement a token blacklist
    # or use short-lived tokens with refresh tokens.
    
    return jsonify({
        'success': True,
        'message': f'Logged out successfully. Goodbye, {user_name}!',
        'note': 'Please remove the token from your client storage'
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user/admin profile"""
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({
            'success': False,
            'message': 'User not found',
            'error_code': 'USER_NOT_FOUND'
        }), 404
    
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update current user profile (not available for admin)"""
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({
            'success': False,
            'message': 'User not found',
            'error_code': 'USER_NOT_FOUND'
        }), 404
    
    if current_user.get_role() == 'admin':
        return jsonify({
            'success': False,
            'message': 'Admin profile updates not supported via this endpoint',
            'error_code': 'ADMIN_PROFILE_UPDATE_NOT_ALLOWED'
        }), 403
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided',
                'error_code': 'INVALID_REQUEST'
            }), 400
        
        # Update allowed fields only
        updatable_fields = ['full_name', 'phone_number', 'address']
        updated_fields = []
        
        for field in updatable_fields:
            if field in data:
                value = data[field].strip() if data[field] else None
                
                if field == 'full_name' and value:
                    if len(value) < 2 or len(value) > 100:
                        return jsonify({
                            'success': False,
                            'message': 'Full name must be between 2 and 100 characters',
                            'error_code': 'INVALID_FULL_NAME'
                        }), 400
                
                setattr(current_user, field, value)
                updated_fields.append(field)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': current_user.to_dict(),
            'updated_fields': updated_fields
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Profile update failed due to server error',
            'error_code': 'SERVER_ERROR'
        }), 500

@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """Verify JWT token and return user info"""
    token = JWTAuth.get_token_from_request()
    
    if not token:
        return jsonify({
            'valid': False,
            'message': 'No token provided',
            'error_code': 'TOKEN_MISSING'
        }), 401
    
    try:
        payload = JWTAuth.decode_token(token)
        user = JWTAuth.get_current_user_from_token()
        
        if not user:
            return jsonify({
                'valid': False,
                'message': 'User not found',
                'error_code': 'USER_NOT_FOUND'
            }), 404
        
        # Check if user is still active (for regular users)
        if user.get_role() == 'user' and not user.is_active:
            return jsonify({
                'valid': False,
                'message': 'Account has been deactivated',
                'error_code': 'ACCOUNT_DEACTIVATED'
            }), 403
        
        return jsonify({
            'valid': True,
            'user': user.to_dict(),
            'expires_at': payload.get('exp')
        }), 200
        
    except AuthError as e:
        return jsonify({
            'valid': False,
            'message': e.message,
            'error_code': 'TOKEN_INVALID'
        }), e.status_code
    except Exception as e:
        return jsonify({
            'valid': False,
            'message': 'Token verification failed',
            'error_code': 'VERIFICATION_ERROR'
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@token_required
def refresh_token():
    """Refresh JWT token"""
    current_user = get_current_user()
    
    if not current_user:
        return jsonify({
            'success': False,
            'message': 'User not found',
            'error_code': 'USER_NOT_FOUND'
        }), 404
    
    try:
        # Generate new token
        new_token = JWTAuth.generate_token(current_user)
        
        return jsonify({
            'success': True,
            'message': 'Token refreshed successfully',
            'token': new_token,
            'user': current_user.to_dict(),
            'expires_in': 168 * 60 * 60  # 7 days in seconds
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Token refresh failed',
            'error_code': 'REFRESH_FAILED'
        }), 500 