"""
Dashboard API routes with role-based access control
Backend-focused with JSON responses
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from functools import wraps
from models import User, Admin, ParkingLot, ParkingSpot, Reservation, db
from datetime import datetime, timedelta
from sqlalchemy import func, desc

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

# ==================== USER PARKING LOT MANAGEMENT ====================

@dashboard_bp.route('/user/parking-lots', methods=['GET'])
@user_required
def get_available_parking_lots():
    """Get all available parking lots for users"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        search = request.args.get('search', '').strip()
        
        # Build query for active lots with available spots
        query = ParkingLot.query.filter_by(is_active=True)
        
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                db.or_(
                    ParkingLot.prime_location_name.ilike(search_filter),
                    ParkingLot.address.ilike(search_filter),
                    ParkingLot.pin_code.ilike(search_filter)
                )
            )
        
        # Get pagination
        pagination = query.paginate(
            page=page, per_page=per_page, 
            error_out=False
        )
        
        lots_data = []
        for lot in pagination.items:
            available_spots = lot.available_spots_count
            if available_spots > 0:  # Only include lots with available spots
                lots_data.append({
                    'id': lot.id,
                    'name': lot.prime_location_name,
                    'address': lot.address,
                    'pin_code': lot.pin_code,
                    'price_per_hour': lot.price_per_hour,
                    'available_spots': available_spots,
                    'total_spots': lot.number_of_spots,
                    'occupancy_rate': round(((lot.number_of_spots - available_spots) / lot.number_of_spots) * 100, 1),
                    'description': lot.description,
                    'created_at': lot.created_at.isoformat()
                })
        
        return jsonify({
            'success': True,
            'data': {
                'lots': lots_data,
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading parking lots: {str(e)}'
        }), 500


@dashboard_bp.route('/user/parking-lots/<int:lot_id>', methods=['GET'])
@user_required  
def get_parking_lot_details(lot_id):
    """Get detailed information about a specific parking lot for users"""
    try:
        lot = ParkingLot.query.filter_by(id=lot_id, is_active=True).first()
        if not lot:
            return jsonify({
                'success': False,
                'message': 'Parking lot not found or inactive'
            }), 404
        
        # Get available spots details
        available_spots = []
        for spot in lot.parking_spots.filter_by(status='A').order_by(ParkingSpot.spot_number):
            available_spots.append({
                'id': spot.id,
                'spot_number': spot.spot_number,
                'vehicle_type': spot.vehicle_type,
                'created_at': spot.created_at.isoformat()
            })
        
        lot_data = {
            'id': lot.id,
            'name': lot.prime_location_name,
            'address': lot.address,
            'pin_code': lot.pin_code,
            'price_per_hour': lot.price_per_hour,
            'available_spots_count': len(available_spots),
            'total_spots': lot.number_of_spots,
            'occupancy_rate': round(((lot.number_of_spots - len(available_spots)) / lot.number_of_spots) * 100, 1),
            'description': lot.description,
            'available_spots': available_spots,
            'created_at': lot.created_at.isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': lot_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading parking lot details: {str(e)}'
        }), 500


# ==================== USER RESERVATION MANAGEMENT ====================

@dashboard_bp.route('/user/reservations', methods=['POST'])
@user_required
def create_reservation():
    """Auto-allocate and reserve the first available spot in a parking lot"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['lot_id', 'vehicle_number']
        for field in required_fields:
            if field not in data or not str(data[field]).strip():
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        lot_id = int(data['lot_id'])
        vehicle_number = data['vehicle_number'].strip().upper()
        vehicle_model = data.get('vehicle_model', '').strip() or None
        
        # Check if user already has an active reservation
        existing_reservation = current_user.reservations.filter_by(status='active').first()
        if existing_reservation:
            return jsonify({
                'success': False,
                'message': 'You already have an active reservation. Please complete it before making a new one.'
            }), 400
        
        # Validate parking lot
        lot = ParkingLot.query.filter_by(id=lot_id, is_active=True).first()
        if not lot:
            return jsonify({
                'success': False,
                'message': 'Parking lot not found or inactive'
            }), 404
        
        # Find first available spot (auto-allocation)
        available_spot = lot.parking_spots.filter_by(status='A').order_by(ParkingSpot.spot_number).first()
        if not available_spot:
            return jsonify({
                'success': False,
                'message': 'No available spots in this parking lot'
            }), 400
        
        # Create reservation
        reservation = Reservation(
            spot_id=available_spot.id,
            user_id=current_user.id,
            vehicle_number=vehicle_number,
            vehicle_model=vehicle_model,
            parking_timestamp=datetime.utcnow(),
            status='active'
        )
        
        # Update spot status to occupied
        available_spot.status = 'O'
        available_spot.updated_at = datetime.utcnow()
        
        # Save to database
        db.session.add(reservation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Parking spot reserved successfully!',
            'data': {
                'reservation_id': reservation.id,
                'spot_number': available_spot.spot_number,
                'lot_name': lot.prime_location_name,
                'lot_address': lot.address,
                'vehicle_number': vehicle_number,
                'parking_timestamp': reservation.parking_timestamp.isoformat(),
                'price_per_hour': lot.price_per_hour
            }
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': 'Invalid lot ID provided'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating reservation: {str(e)}'
        }), 500


@dashboard_bp.route('/user/reservations/<int:reservation_id>/occupy', methods=['POST'])
@user_required
def occupy_parking_spot(reservation_id):
    """Mark a reserved spot as occupied (user has arrived and parked)"""
    try:
        # Find user's active reservation
        reservation = current_user.reservations.filter_by(
            id=reservation_id, 
            status='active'
        ).first()
        
        if not reservation:
            return jsonify({
                'success': False,
                'message': 'Active reservation not found'
            }), 404
        
        # Update occupation timestamp (when user actually arrives and parks)
        reservation.parking_timestamp = datetime.utcnow()
        reservation.updated_at = datetime.utcnow()
        
        # Ensure spot is marked as occupied
        reservation.parking_spot.status = 'O'
        reservation.parking_spot.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        duration_minutes = (datetime.utcnow() - reservation.parking_timestamp).total_seconds() / 60
        
        return jsonify({
            'success': True,
            'message': 'Parking spot occupied successfully!',
            'data': {
                'reservation_id': reservation.id,
                'spot_number': reservation.parking_spot.spot_number,
                'lot_name': reservation.parking_spot.parking_lot.prime_location_name,
                'vehicle_number': reservation.vehicle_number,
                'parking_timestamp': reservation.parking_timestamp.isoformat(),
                'duration_minutes': int(duration_minutes),
                'estimated_cost': round(duration_minutes / 60 * reservation.parking_spot.parking_lot.price_per_hour, 2)
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error occupying parking spot: {str(e)}'
        }), 500


@dashboard_bp.route('/user/reservations/<int:reservation_id>/release', methods=['POST'])
@user_required
def release_parking_spot(reservation_id):
    """Release an occupied parking spot and calculate final cost"""
    try:
        # Find user's active reservation
        reservation = current_user.reservations.filter_by(
            id=reservation_id, 
            status='active'
        ).first()
        
        if not reservation:
            return jsonify({
                'success': False,
                'message': 'Active reservation not found'
            }), 404
        
        # Set leaving timestamp
        leaving_time = datetime.utcnow()
        reservation.leaving_timestamp = leaving_time
        reservation.status = 'completed'
        reservation.updated_at = leaving_time
        
        # Calculate final cost
        final_cost = reservation.calculate_cost()
        
        # Free up the parking spot
        reservation.parking_spot.status = 'A'
        reservation.parking_spot.updated_at = leaving_time
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Parking spot released successfully!',
            'data': {
                'reservation_id': reservation.id,
                'spot_number': reservation.parking_spot.spot_number,
                'lot_name': reservation.parking_spot.parking_lot.prime_location_name,
                'vehicle_number': reservation.vehicle_number,
                'parking_timestamp': reservation.parking_timestamp.isoformat(),
                'leaving_timestamp': reservation.leaving_timestamp.isoformat(),
                'duration_minutes': reservation.duration_minutes,
                'duration_hours': reservation.duration_hours,
                'final_cost': final_cost,
                'price_per_hour': reservation.parking_spot.parking_lot.price_per_hour
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error releasing parking spot: {str(e)}'
        }), 500


@dashboard_bp.route('/user/reservations', methods=['GET'])
@user_required
def get_user_reservations():
    """Get user's parking history with filtering and pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        status_filter = request.args.get('status', '').strip()
        
        # Build query
        query = current_user.reservations.order_by(Reservation.created_at.desc())
        
        if status_filter and status_filter in ['active', 'completed', 'cancelled']:
            query = query.filter_by(status=status_filter)
        
        # Get pagination
        pagination = query.paginate(
            page=page, per_page=per_page, 
            error_out=False
        )
        
        reservations_data = []
        for reservation in pagination.items:
            duration_minutes = 0
            estimated_cost = 0
            
            if reservation.status == 'active':
                # Calculate current duration and estimated cost
                duration_minutes = (datetime.utcnow() - reservation.parking_timestamp).total_seconds() / 60
                estimated_cost = round(duration_minutes / 60 * reservation.parking_spot.parking_lot.price_per_hour, 2)
            else:
                duration_minutes = reservation.duration_minutes
                estimated_cost = reservation.parking_cost or 0
            
            reservations_data.append({
                'id': reservation.id,
                'spot_number': reservation.parking_spot.spot_number,
                'lot_name': reservation.parking_spot.parking_lot.prime_location_name,
                'lot_address': reservation.parking_spot.parking_lot.address,
                'lot_price_per_hour': reservation.parking_spot.parking_lot.price_per_hour,
                'status': reservation.status,
                'vehicle_number': reservation.vehicle_number,
                'vehicle_model': reservation.vehicle_model,
                'parking_timestamp': reservation.parking_timestamp.isoformat(),
                'leaving_timestamp': reservation.leaving_timestamp.isoformat() if reservation.leaving_timestamp else None,
                'duration_minutes': int(duration_minutes),
                'duration_hours': reservation.duration_hours if reservation.status == 'completed' else round(duration_minutes / 60, 1),
                'cost': estimated_cost,
                'created_at': reservation.created_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'data': {
                'reservations': reservations_data,
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading reservations: {str(e)}'
        }), 500


@dashboard_bp.route('/user/reservations/<int:reservation_id>', methods=['GET'])
@user_required
def get_reservation_details(reservation_id):
    """Get detailed information about a specific reservation"""
    try:
        reservation = current_user.reservations.filter_by(id=reservation_id).first()
        
        if not reservation:
            return jsonify({
                'success': False,
                'message': 'Reservation not found'
            }), 404
        
        duration_minutes = 0
        estimated_cost = 0
        
        if reservation.status == 'active':
            # Calculate current duration and estimated cost
            duration_minutes = (datetime.utcnow() - reservation.parking_timestamp).total_seconds() / 60
            estimated_cost = round(duration_minutes / 60 * reservation.parking_spot.parking_lot.price_per_hour, 2)
        else:
            duration_minutes = reservation.duration_minutes
            estimated_cost = reservation.parking_cost or 0
        
        reservation_data = {
            'id': reservation.id,
            'spot_number': reservation.parking_spot.spot_number,
            'lot_id': reservation.parking_spot.parking_lot.id,
            'lot_name': reservation.parking_spot.parking_lot.prime_location_name,
            'lot_address': reservation.parking_spot.parking_lot.address,
            'lot_pin_code': reservation.parking_spot.parking_lot.pin_code,
            'lot_price_per_hour': reservation.parking_spot.parking_lot.price_per_hour,
            'lot_description': reservation.parking_spot.parking_lot.description,
            'status': reservation.status,
            'vehicle_number': reservation.vehicle_number,
            'vehicle_model': reservation.vehicle_model,
            'parking_timestamp': reservation.parking_timestamp.isoformat(),
            'leaving_timestamp': reservation.leaving_timestamp.isoformat() if reservation.leaving_timestamp else None,
            'duration_minutes': int(duration_minutes),
            'duration_hours': reservation.duration_hours if reservation.status == 'completed' else round(duration_minutes / 60, 1),
            'cost': estimated_cost,
            'created_at': reservation.created_at.isoformat(),
            'updated_at': reservation.updated_at.isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': reservation_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading reservation details: {str(e)}'
        }), 500 