"""
Dashboard API routes with role-based access control
Backend-focused with JSON responses
"""

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models import User, Admin, ParkingLot, ParkingSpot, Reservation, db
from datetime import datetime, timedelta
from sqlalchemy import func

# Create dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        if not hasattr(current_user, 'get_role') or current_user.get_role() != 'admin':
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    """Decorator to require user role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        if hasattr(current_user, 'get_role') and current_user.get_role() == 'admin':
            return jsonify({
                'success': False,
                'message': 'User access required (admin not allowed)'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/admin', methods=['GET'])
@admin_required
def admin_dashboard():
    """Admin dashboard with system overview"""
    try:
        # Get system statistics
        stats = {
            'total_users': User.query.count(),
            'active_users': User.query.filter_by(is_active=True).count(),
            'inactive_users': User.query.filter_by(is_active=False).count(),
            'total_parking_lots': ParkingLot.query.count(),
            'active_parking_lots': ParkingLot.query.filter_by(is_active=True).count(),
            'total_parking_spots': ParkingSpot.query.count(),
            'available_spots': ParkingSpot.query.filter_by(status='A').count(),
            'occupied_spots': ParkingSpot.query.filter_by(status='O').count(),
            'total_reservations': Reservation.query.count(),
            'active_reservations': Reservation.query.filter_by(status='active').count(),
            'completed_reservations': Reservation.query.filter_by(status='completed').count(),
        }
        
        # Recent activity
        recent_users = []
        for user in User.query.order_by(User.created_at.desc()).limit(5).all():
            recent_users.append({
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'email': user.email,
                'created_at': user.created_at.isoformat(),
                'is_active': user.is_active
            })
        
        recent_reservations = []
        for reservation in Reservation.query.order_by(Reservation.created_at.desc()).limit(5).all():
            recent_reservations.append({
                'id': reservation.id,
                'user_name': reservation.user.full_name,
                'spot_number': reservation.parking_spot.spot_number,
                'lot_name': reservation.parking_spot.parking_lot.prime_location_name,
                'status': reservation.status,
                'created_at': reservation.created_at.isoformat(),
                'vehicle_number': reservation.vehicle_number
            })
        
        # Parking lot details
        parking_lots = []
        for lot in ParkingLot.query.filter_by(is_active=True).all():
            parking_lots.append({
                'id': lot.id,
                'name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'price_per_hour': lot.price_per_hour,
                'total_spots': lot.number_of_spots,
                'available_spots': lot.available_spots_count,
                'occupied_spots': lot.occupied_spots_count,
                'occupancy_rate': round((lot.occupied_spots_count / lot.number_of_spots) * 100, 1) if lot.number_of_spots > 0 else 0
            })
        
        return jsonify({
            'success': True,
            'data': {
                'stats': stats,
                'recent_users': recent_users,
                'recent_reservations': recent_reservations,
                'parking_lots': parking_lots,
                'admin_info': current_user.to_dict()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error loading admin dashboard data'
        }), 500

@dashboard_bp.route('/user', methods=['GET'])
@user_required
def user_dashboard():
    """User dashboard with personal parking information"""
    try:
        # User's reservation statistics
        user_stats = {
            'total_reservations': current_user.reservations.count(),
            'active_reservations': current_user.reservations.filter_by(status='active').count(),
            'completed_reservations': current_user.reservations.filter_by(status='completed').count(),
            'cancelled_reservations': current_user.reservations.filter_by(status='cancelled').count(),
        }
        
        # Current active reservation
        active_reservation = None
        active_res = current_user.reservations.filter_by(status='active').first()
        if active_res:
            duration_minutes = (datetime.utcnow() - active_res.parking_timestamp).total_seconds() / 60
            active_reservation = {
                'id': active_res.id,
                'spot_number': active_res.parking_spot.spot_number,
                'lot_name': active_res.parking_spot.parking_lot.prime_location_name,
                'lot_address': active_res.parking_spot.parking_lot.address,
                'vehicle_number': active_res.vehicle_number,
                'parking_timestamp': active_res.parking_timestamp.isoformat(),
                'duration_minutes': int(duration_minutes),
                'current_cost_estimate': round(duration_minutes / 60 * active_res.parking_spot.parking_lot.price_per_hour, 2)
            }
        
        # Recent reservations
        recent_reservations = []
        for reservation in current_user.reservations.order_by(Reservation.created_at.desc()).limit(10).all():
            recent_reservations.append({
                'id': reservation.id,
                'spot_number': reservation.parking_spot.spot_number,
                'lot_name': reservation.parking_spot.parking_lot.prime_location_name,
                'status': reservation.status,
                'vehicle_number': reservation.vehicle_number,
                'parking_timestamp': reservation.parking_timestamp.isoformat(),
                'leaving_timestamp': reservation.leaving_timestamp.isoformat() if reservation.leaving_timestamp else None,
                'duration_minutes': reservation.duration_minutes,
                'parking_cost': reservation.parking_cost
            })
        
        # Available parking lots
        available_lots = []
        for lot in ParkingLot.query.filter_by(is_active=True).all():
            if lot.available_spots_count > 0:
                available_lots.append({
                    'id': lot.id,
                    'name': lot.prime_location_name,
                    'address': lot.address,
                    'pin_code': lot.pin_code,
                    'price_per_hour': lot.price_per_hour,
                    'available_spots': lot.available_spots_count,
                    'total_spots': lot.number_of_spots,
                    'description': lot.description
                })
        
        return jsonify({
            'success': True,
            'data': {
                'user_stats': user_stats,
                'active_reservation': active_reservation,
                'recent_reservations': recent_reservations,
                'available_lots': available_lots,
                'user_info': current_user.to_dict()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error loading user dashboard data'
        }), 500

@dashboard_bp.route('/redirect', methods=['GET'])
@login_required
def dashboard_redirect():
    """API endpoint to get appropriate dashboard route based on user role"""
    if hasattr(current_user, 'get_role') and current_user.get_role() == 'admin':
        return jsonify({
            'success': True,
            'redirect_to': '/api/dashboard/admin',
            'user_role': 'admin'
        }), 200
    else:
        return jsonify({
            'success': True,
            'redirect_to': '/api/dashboard/user',
            'user_role': 'user'
        }), 200

@dashboard_bp.route('/admin/users', methods=['GET'])
@admin_required
def admin_users_list():
    """Get list of all users for admin"""
    try:
        users = []
        for user in User.query.order_by(User.created_at.desc()).all():
            user_data = user.to_dict()
            user_data['total_reservations'] = user.reservations.count()
            user_data['active_reservations'] = user.reservations.filter_by(status='active').count()
            users.append(user_data)
        
        return jsonify({
            'success': True,
            'data': {
                'users': users,
                'total_count': len(users)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error loading users data'
        }), 500

@dashboard_bp.route('/admin/parking-lots', methods=['GET'])
@admin_required
def admin_parking_lots():
    """Get detailed parking lots information for admin"""
    try:
        lots_data = []
        for lot in ParkingLot.query.order_by(ParkingLot.created_at.desc()).all():
            lot_data = {
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'price_per_hour': lot.price_per_hour,
                'number_of_spots': lot.number_of_spots,
                'description': lot.description,
                'is_active': lot.is_active,
                'created_at': lot.created_at.isoformat(),
                'available_spots': lot.available_spots_count,
                'occupied_spots': lot.occupied_spots_count,
                'occupancy_rate': round((lot.occupied_spots_count / lot.number_of_spots) * 100, 1) if lot.number_of_spots > 0 else 0
            }
            lots_data.append(lot_data)
        
        return jsonify({
            'success': True,
            'data': {
                'parking_lots': lots_data,
                'total_count': len(lots_data)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error loading parking lots data'
        }), 500 