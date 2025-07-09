from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import os
from database import db
from auth_utils import JWTAuth

# Initialize Flask app
app = Flask(__name__)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "parking_system.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'parking-system-secret-key-change-in-production-2024'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Initialize CORS for cross-origin requests
CORS(app, 
     origins=['http://localhost:3000', 'http://localhost:5173', 'http://localhost:8080'],  # Vue.js dev servers
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'],
     supports_credentials=True)

# Import models after db initialization to avoid circular imports
from models import User, Admin, ParkingLot, ParkingSpot, Reservation

# Register blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(admin_bp)

# Main application routes
@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        'message': 'Vehicle Parking System V2 API',
        'version': '2.0',
        'status': 'active',
        'authentication': 'enabled',
        'endpoints': {
            'auth': {
                'login': '/api/auth/login',
                'register': '/api/auth/register',
                'logout': '/api/auth/logout',
                'profile': '/api/auth/profile',
                'status': '/api/auth/status'
            },
            'dashboard': {
                'admin': '/api/dashboard/admin',
                'user': '/api/dashboard/user',
                'redirect': '/api/dashboard/redirect'
            },
            'health': '/health'
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint with authentication status"""
    try:
        # Test database connection
        user_count = User.query.count()
        admin_count = Admin.query.count()
        lot_count = ParkingLot.query.count()
        spot_count = ParkingSpot.query.count()
        reservation_count = Reservation.query.count()
        
        # JWT Authentication status
        current_user = JWTAuth.get_current_user_from_token()
        auth_status = {
            'authenticated': current_user is not None,
            'user_id': current_user.id if current_user else None,
            'user_role': current_user.get_role() if current_user else None,
            'authentication_method': 'JWT'
        }
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': {
                'status': 'connected',
                'users': user_count,
                'admins': admin_count,
                'parking_lots': lot_count,
                'parking_spots': spot_count,
                'reservations': reservation_count
            },
            'authentication': auth_status,
            'jwt_auth': 'enabled',
            'cors': 'enabled'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/api/info')
def api_info():
    """Get API information and available endpoints"""
    endpoints = {
        'authentication': {
            'POST /api/auth/login': 'User/Admin login',
            'POST /api/auth/register': 'User registration (admin registration not allowed)',
            'POST /api/auth/logout': 'Logout (requires authentication)',
            'GET /api/auth/profile': 'Get user profile (requires authentication)',
            'GET /api/auth/status': 'Check authentication status'
        },
        'dashboard': {
            'GET /api/dashboard/admin': 'Admin dashboard (admin only)',
            'GET /api/dashboard/user': 'User dashboard (users only)',
            'GET /api/dashboard/redirect': 'Get dashboard redirect based on role'
        },
        'admin_management': {
            'GET /api/admin/parking-lots': 'List all parking lots with filters (admin only)',
            'GET /api/admin/parking-lots/{id}': 'Get detailed parking lot info (admin only)',
            'POST /api/admin/parking-lots': 'Create new parking lot (admin only)',
            'PUT /api/admin/parking-lots/{id}': 'Update parking lot (admin only)',
            'DELETE /api/admin/parking-lots/{id}': 'Delete parking lot (admin only)',
            'GET /api/admin/users': 'List all users with stats (admin only)',
            'GET /api/admin/users/{id}': 'Get detailed user info (admin only)',
            'POST /api/admin/users/{id}/toggle-status': 'Toggle user active status (admin only)',
            'GET /api/admin/statistics': 'Get system statistics (admin only)'
        }
    }
    
    return jsonify({
        'api_name': 'Vehicle Parking System V2',
        'version': '2.0',
        'authentication': 'Flask-Login with sessions',
        'role_based_access': True,
        'endpoints': endpoints,
        'default_admin': {
            'username': 'admin',
            'note': 'Default password set during database initialization'
        }
    })

# Error handlers
@app.errorhandler(401)
def unauthorized_error(error):
    """Handle unauthorized access"""
    return jsonify({
        'success': False,
        'message': 'Authentication required',
        'error_code': 'UNAUTHORIZED'
    }), 401

@app.errorhandler(403)
def forbidden_error(error):
    """Handle forbidden access"""
    return jsonify({
        'success': False,
        'message': 'Access forbidden - insufficient permissions',
        'error_code': 'FORBIDDEN'
    }), 403

@app.errorhandler(404)
def not_found_error(error):
    """Handle page not found"""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found',
        'error_code': 'NOT_FOUND'
    }), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    """Handle method not allowed"""
    return jsonify({
        'success': False,
        'message': 'Method not allowed for this endpoint',
        'error_code': 'METHOD_NOT_ALLOWED'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error"""
    db.session.rollback()
    return jsonify({
        'success': False,
        'message': 'Internal server error',
        'error_code': 'INTERNAL_ERROR'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
