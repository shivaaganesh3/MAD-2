"""
JWT Authentication Utilities for Vehicle Parking System
Provides token-based authentication with role-based access control
"""

import jwt
import functools
from datetime import datetime, timedelta
from flask import request, jsonify, current_app
from werkzeug.security import check_password_hash
from models import User, Admin
from database import db

class AuthError(Exception):
    """Custom authentication error"""
    def __init__(self, message, status_code=401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class JWTAuth:
    """JWT Authentication Manager"""
    
    @staticmethod
    def generate_token(user, expires_in_hours=168):  # 7 days = 168 hours
        """Generate JWT token for user or admin"""
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.get_role(),
            'user_type': 'admin' if user.get_role() == 'admin' else 'user',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours)
        }
        
        # Add additional user info based on type
        if user.get_role() == 'admin':
            payload.update({
                'email': user.email,
                'admin_id': user.id
            })
        else:
            payload.update({
                'email': user.email,
                'full_name': user.full_name,
                'is_active': user.is_active
            })
        
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def decode_token(token):
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError('Token has expired', 401)
        except jwt.InvalidTokenError:
            raise AuthError('Invalid token', 401)
    
    @staticmethod
    def get_token_from_request():
        """Extract token from request headers"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        
        try:
            # Expected format: "Bearer <token>"
            token_type, token = auth_header.split(' ', 1)
            if token_type.lower() != 'bearer':
                return None
            return token
        except ValueError:
            return None
    
    @staticmethod
    def get_current_user_from_token():
        """Get current user from JWT token"""
        token = JWTAuth.get_token_from_request()
        if not token:
            return None
        
        try:
            payload = JWTAuth.decode_token(token)
            user_type = payload.get('user_type')
            user_id = payload.get('user_id')
            
            if user_type == 'admin':
                return Admin.query.get(user_id)
            else:
                return User.query.get(user_id)
        except AuthError:
            return None
    
    @staticmethod
    def authenticate_user(username, password, user_type='user'):
        """Authenticate user with username/password"""
        try:
            if user_type == 'admin':
                user = Admin.query.filter_by(username=username).first()
                if user and user.check_password(password):
                    # Update last login
                    user.last_login = datetime.utcnow()
                    db.session.commit()
                    return user
            else:
                user = User.query.filter_by(username=username).first()
                if user and user.check_password(password):
                    # Check if user is active
                    if not user.is_active:
                        raise AuthError('Account is deactivated. Please contact admin.', 403)
                    return user
            
            return None
        except Exception as e:
            db.session.rollback()
            if isinstance(e, AuthError):
                raise e
            raise AuthError('Authentication failed due to server error', 500)

def token_required(f):
    """Decorator to require valid JWT token"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = JWTAuth.get_token_from_request()
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is missing',
                'error_code': 'TOKEN_MISSING'
            }), 401
        
        try:
            payload = JWTAuth.decode_token(token)
            
            # Get user from database to ensure they still exist
            user_type = payload.get('user_type')
            user_id = payload.get('user_id')
            
            if user_type == 'admin':
                current_user = Admin.query.get(user_id)
            else:
                current_user = User.query.get(user_id)
                # Check if user is still active
                if current_user and not current_user.is_active:
                    return jsonify({
                        'success': False,
                        'message': 'Account has been deactivated',
                        'error_code': 'ACCOUNT_DEACTIVATED'
                    }), 403
            
            if not current_user:
                return jsonify({
                    'success': False,
                    'message': 'User no longer exists',
                    'error_code': 'USER_NOT_FOUND'
                }), 401
            
            # Add current_user to request context
            request.current_user = current_user
            
            return f(*args, **kwargs)
            
        except AuthError as e:
            return jsonify({
                'success': False,
                'message': e.message,
                'error_code': 'TOKEN_INVALID'
            }), e.status_code
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Token validation failed',
                'error_code': 'TOKEN_ERROR'
            }), 500
    
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @functools.wraps(f)
    @token_required
    def decorated_function(*args, **kwargs):
        current_user = getattr(request, 'current_user', None)
        
        if not current_user or current_user.get_role() != 'admin':
            return jsonify({
                'success': False,
                'message': 'Admin privileges required',
                'error_code': 'ADMIN_REQUIRED'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def user_required(f):
    """Decorator to require user role (not admin)"""
    @functools.wraps(f)
    @token_required
    def decorated_function(*args, **kwargs):
        current_user = getattr(request, 'current_user', None)
        
        if not current_user or current_user.get_role() != 'user':
            return jsonify({
                'success': False,
                'message': 'User privileges required',
                'error_code': 'USER_REQUIRED'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Get current user from request context"""
    return getattr(request, 'current_user', None) 