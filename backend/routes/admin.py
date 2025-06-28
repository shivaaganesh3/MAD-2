"""
Admin Management API Routes
Comprehensive admin functionalities for parking lot and user management
"""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models import User, Admin, ParkingLot, ParkingSpot, Reservation, db
from datetime import datetime
from sqlalchemy import func, desc
import re

# Create admin management blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

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

def validate_parking_lot_data(data, lot_id=None):
    """Validate parking lot data"""
    errors = []
    
    # Required fields
    required_fields = ['prime_location_name', 'address', 'pin_code', 'price_per_hour', 'number_of_spots']
    for field in required_fields:
        if field not in data or not str(data[field]).strip():
            errors.append(f'{field.replace("_", " ").title()} is required')
    
    if errors:
        return errors
    
    # Validate specific fields
    prime_location_name = str(data['prime_location_name']).strip()
    if len(prime_location_name) < 3 or len(prime_location_name) > 100:
        errors.append('Location name must be between 3 and 100 characters')
    
    address = str(data['address']).strip()
    if len(address) < 10 or len(address) > 500:
        errors.append('Address must be between 10 and 500 characters')
    
    pin_code = str(data['pin_code']).strip()
    if not re.match(r'^\d{6}$', pin_code):
        errors.append('Pin code must be exactly 6 digits')
    
    try:
        price_per_hour = float(data['price_per_hour'])
        if price_per_hour <= 0 or price_per_hour > 10000:
            errors.append('Price per hour must be between 0 and 10000')
    except (ValueError, TypeError):
        errors.append('Price per hour must be a valid number')
    
    try:
        number_of_spots = int(data['number_of_spots'])
        if number_of_spots <= 0 or number_of_spots > 1000:
            errors.append('Number of spots must be between 1 and 1000')
    except (ValueError, TypeError):
        errors.append('Number of spots must be a valid integer')
    
    # Check for duplicate location name (exclude current lot if editing)
    existing_lot = ParkingLot.query.filter_by(prime_location_name=prime_location_name).first()
    if existing_lot and (lot_id is None or existing_lot.id != lot_id):
        errors.append('A parking lot with this location name already exists')
    
    return errors

def create_parking_spots_for_lot(parking_lot):
    """Create parking spots for a given parking lot"""
    try:
        # Delete existing spots if any
        ParkingSpot.query.filter_by(lot_id=parking_lot.id).delete()
        
        spots_per_row = 10  # 10 spots per row
        rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']  # Row identifiers
        
        spot_count = 0
        created_spots = []
        
        for row in rows:
            if spot_count >= parking_lot.number_of_spots:
                break
            
            for spot_num in range(1, spots_per_row + 1):
                if spot_count >= parking_lot.number_of_spots:
                    break
                
                spot_number = f"{row}{spot_num:02d}"  # e.g., A01, A02, B01, etc.
                
                parking_spot = ParkingSpot(
                    lot_id=parking_lot.id,
                    spot_number=spot_number,
                    status='A',  # Available
                    vehicle_type='4-wheeler'
                )
                
                db.session.add(parking_spot)
                created_spots.append(parking_spot)
                spot_count += 1
        
        return created_spots
    
    except Exception as e:
        raise Exception(f"Error creating parking spots: {str(e)}")

# ==================== PARKING LOT MANAGEMENT ====================

@admin_bp.route('/parking-lots', methods=['GET'])
@admin_required
def get_parking_lots():
    """Get all parking lots with detailed information"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '').strip()
        status_filter = request.args.get('status', 'all')  # all, active, inactive
        
        # Build query
        query = ParkingLot.query
        
        # Apply search filter
        if search:
            query = query.filter(
                (ParkingLot.prime_location_name.contains(search)) |
                (ParkingLot.address.contains(search)) |
                (ParkingLot.pin_code.contains(search))
            )
        
        # Apply status filter
        if status_filter == 'active':
            query = query.filter_by(is_active=True)
        elif status_filter == 'inactive':
            query = query.filter_by(is_active=False)
        
        # Order by creation date (newest first)
        query = query.order_by(desc(ParkingLot.created_at))
        
        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        lots_data = []
        for lot in pagination.items:
            # Get revenue data
            total_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
                Reservation.spot_id.in_([spot.id for spot in lot.parking_spots]),
                Reservation.status == 'completed',
                Reservation.parking_cost.isnot(None)
            ).scalar() or 0
            
            # Get active reservations
            active_reservations = db.session.query(Reservation).filter(
                Reservation.spot_id.in_([spot.id for spot in lot.parking_spots]),
                Reservation.status == 'active'
            ).count()
            
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
                'updated_at': lot.updated_at.isoformat(),
                'available_spots': lot.available_spots_count,
                'occupied_spots': lot.occupied_spots_count,
                'occupancy_rate': round((lot.occupied_spots_count / lot.number_of_spots) * 100, 1) if lot.number_of_spots > 0 else 0,
                'total_revenue': round(total_revenue, 2),
                'active_reservations': active_reservations
            }
            lots_data.append(lot_data)
        
        return jsonify({
            'success': True,
            'data': {
                'parking_lots': lots_data,
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
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

@admin_bp.route('/parking-lots/<int:lot_id>', methods=['GET'])
@admin_required
def get_parking_lot(lot_id):
    """Get detailed information about a specific parking lot"""
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        
        # Get parking spots with details
        spots_data = []
        for spot in lot.parking_spots.order_by(ParkingSpot.spot_number):
            spot_data = {
                'id': spot.id,
                'spot_number': spot.spot_number,
                'status': spot.status,
                'vehicle_type': spot.vehicle_type,
                'created_at': spot.created_at.isoformat(),
                'current_reservation': None
            }
            
            # Add current reservation details if occupied
            if spot.status == 'O':
                reservation = spot.current_reservation
                if reservation:
                    duration_minutes = (datetime.utcnow() - reservation.parking_timestamp).total_seconds() / 60
                    spot_data['current_reservation'] = {
                        'id': reservation.id,
                        'user_name': reservation.user.full_name,
                        'user_username': reservation.user.username,
                        'vehicle_number': reservation.vehicle_number,
                        'vehicle_model': reservation.vehicle_model,
                        'parking_timestamp': reservation.parking_timestamp.isoformat(),
                        'duration_minutes': int(duration_minutes),
                        'estimated_cost': round(duration_minutes / 60 * lot.price_per_hour, 2)
                    }
            
            spots_data.append(spot_data)
        
        # Get revenue statistics
        total_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            Reservation.spot_id.in_([spot.id for spot in lot.parking_spots]),
            Reservation.status == 'completed',
            Reservation.parking_cost.isnot(None)
        ).scalar() or 0
        
        total_reservations = db.session.query(Reservation).filter(
            Reservation.spot_id.in_([spot.id for spot in lot.parking_spots])
        ).count()
        
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
            'updated_at': lot.updated_at.isoformat(),
            'available_spots': lot.available_spots_count,
            'occupied_spots': lot.occupied_spots_count,
            'occupancy_rate': round((lot.occupied_spots_count / lot.number_of_spots) * 100, 1) if lot.number_of_spots > 0 else 0,
            'total_revenue': round(total_revenue, 2),
            'total_reservations': total_reservations,
            'parking_spots': spots_data
        }
        
        return jsonify({
            'success': True,
            'data': lot_data
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading parking lot: {str(e)}'
        }), 500

@admin_bp.route('/parking-lots', methods=['POST'])
@admin_required
def create_parking_lot():
    """Create a new parking lot with automatic spot generation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400
        
        # Validate data
        errors = validate_parking_lot_data(data)
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        # Create parking lot
        parking_lot = ParkingLot(
            prime_location_name=data['prime_location_name'].strip(),
            address=data['address'].strip(),
            pin_code=data['pin_code'].strip(),
            price_per_hour=float(data['price_per_hour']),
            number_of_spots=int(data['number_of_spots']),
            description=data.get('description', '').strip() or None,
            is_active=data.get('is_active', True)
        )
        
        db.session.add(parking_lot)
        db.session.flush()  # Get the ID without committing
        
        # Create parking spots automatically
        created_spots = create_parking_spots_for_lot(parking_lot)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Parking lot "{parking_lot.prime_location_name}" created successfully with {len(created_spots)} spots',
            'data': {
                'lot_id': parking_lot.id,
                'spots_created': len(created_spots)
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating parking lot: {str(e)}'
        }), 500

@admin_bp.route('/parking-lots/<int:lot_id>', methods=['PUT'])
@admin_required
def update_parking_lot(lot_id):
    """Update an existing parking lot and regenerate spots if needed"""
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400
        
        # Validate data
        errors = validate_parking_lot_data(data, lot_id)
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }), 400
        
        # Check if number of spots is changing and if there are active reservations
        old_spot_count = lot.number_of_spots
        new_spot_count = int(data['number_of_spots'])
        
        if old_spot_count != new_spot_count:
            active_reservations = db.session.query(Reservation).filter(
                Reservation.spot_id.in_([spot.id for spot in lot.parking_spots]),
                Reservation.status == 'active'
            ).count()
            
            if active_reservations > 0 and new_spot_count < old_spot_count:
                return jsonify({
                    'success': False,
                    'message': f'Cannot reduce spots while {active_reservations} reservations are active. Please wait for them to complete.'
                }), 400
        
        # Update parking lot
        lot.prime_location_name = data['prime_location_name'].strip()
        lot.address = data['address'].strip()
        lot.pin_code = data['pin_code'].strip()
        lot.price_per_hour = float(data['price_per_hour'])
        lot.number_of_spots = new_spot_count
        lot.description = data.get('description', '').strip() or None
        lot.is_active = data.get('is_active', lot.is_active)
        lot.updated_at = datetime.utcnow()
        
        # Regenerate spots if count changed
        spots_message = ""
        if old_spot_count != new_spot_count:
            created_spots = create_parking_spots_for_lot(lot)
            spots_message = f" Parking spots regenerated: {len(created_spots)} spots."
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Parking lot "{lot.prime_location_name}" updated successfully.{spots_message}',
            'data': {
                'lot_id': lot.id,
                'spots_count': lot.number_of_spots
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating parking lot: {str(e)}'
        }), 500

@admin_bp.route('/parking-lots/<int:lot_id>', methods=['DELETE'])
@admin_required
def delete_parking_lot(lot_id):
    """Delete a parking lot (only if all spots are empty)"""
    try:
        lot = ParkingLot.query.get_or_404(lot_id)
        
        # Check if there are any active reservations
        active_reservations = db.session.query(Reservation).filter(
            Reservation.spot_id.in_([spot.id for spot in lot.parking_spots]),
            Reservation.status == 'active'
        ).count()
        
        if active_reservations > 0:
            return jsonify({
                'success': False,
                'message': f'Cannot delete parking lot. There are {active_reservations} active reservations. Please wait for them to complete.'
            }), 400
        
        # Check if there are any occupied spots
        occupied_spots = lot.occupied_spots_count
        if occupied_spots > 0:
            return jsonify({
                'success': False,
                'message': f'Cannot delete parking lot. There are {occupied_spots} occupied spots.'
            }), 400
        
        lot_name = lot.prime_location_name
        
        # Delete the parking lot (spots will be deleted via cascade)
        db.session.delete(lot)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Parking lot "{lot_name}" deleted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting parking lot: {str(e)}'
        }), 500

# ==================== USER MANAGEMENT ====================

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users with their parking details"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        status_filter = request.args.get('status', 'all')  # all, active, inactive
        
        # Build query
        query = User.query
        
        # Apply search filter
        if search:
            query = query.filter(
                (User.username.contains(search)) |
                (User.full_name.contains(search)) |
                (User.email.contains(search)) |
                (User.phone_number.contains(search))
            )
        
        # Apply status filter
        if status_filter == 'active':
            query = query.filter_by(is_active=True)
        elif status_filter == 'inactive':
            query = query.filter_by(is_active=False)
        
        # Order by creation date (newest first)
        query = query.order_by(desc(User.created_at))
        
        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        users_data = []
        for user in pagination.items:
            # Get user statistics
            total_reservations = user.reservations.count()
            active_reservations = user.reservations.filter_by(status='active').count()
            completed_reservations = user.reservations.filter_by(status='completed').count()
            
            # Get total spent
            total_spent = db.session.query(func.sum(Reservation.parking_cost)).filter(
                Reservation.user_id == user.id,
                Reservation.status == 'completed',
                Reservation.parking_cost.isnot(None)
            ).scalar() or 0
            
            # Get current active reservation
            current_reservation = None
            active_res = user.reservations.filter_by(status='active').first()
            if active_res:
                duration_minutes = (datetime.utcnow() - active_res.parking_timestamp).total_seconds() / 60
                current_reservation = {
                    'spot_number': active_res.parking_spot.spot_number,
                    'lot_name': active_res.parking_spot.parking_lot.prime_location_name,
                    'vehicle_number': active_res.vehicle_number,
                    'duration_minutes': int(duration_minutes),
                    'parking_timestamp': active_res.parking_timestamp.isoformat()
                }
            
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'address': user.address,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat(),
                'statistics': {
                    'total_reservations': total_reservations,
                    'active_reservations': active_reservations,
                    'completed_reservations': completed_reservations,
                    'total_spent': round(total_spent, 2)
                },
                'current_reservation': current_reservation
            }
            users_data.append(user_data)
        
        return jsonify({
            'success': True,
            'data': {
                'users': users_data,
                'pagination': {
                    'page': pagination.page,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'pages': pagination.pages,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading users: {str(e)}'
        }), 500

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user_details(user_id):
    """Get detailed information about a specific user"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Get user statistics
        total_reservations = user.reservations.count()
        active_reservations = user.reservations.filter_by(status='active').count()
        completed_reservations = user.reservations.filter_by(status='completed').count()
        cancelled_reservations = user.reservations.filter_by(status='cancelled').count()
        
        # Get total spent and average session duration
        completed_res = user.reservations.filter_by(status='completed').all()
        total_spent = sum([r.parking_cost for r in completed_res if r.parking_cost]) or 0
        avg_duration = sum([r.duration_minutes for r in completed_res]) / len(completed_res) if completed_res else 0
        
        # Get current active reservation
        current_reservation = None
        active_res = user.reservations.filter_by(status='active').first()
        if active_res:
            duration_minutes = (datetime.utcnow() - active_res.parking_timestamp).total_seconds() / 60
            current_reservation = {
                'id': active_res.id,
                'spot_number': active_res.parking_spot.spot_number,
                'lot_name': active_res.parking_spot.parking_lot.prime_location_name,
                'lot_address': active_res.parking_spot.parking_lot.address,
                'vehicle_number': active_res.vehicle_number,
                'vehicle_model': active_res.vehicle_model,
                'parking_timestamp': active_res.parking_timestamp.isoformat(),
                'duration_minutes': int(duration_minutes),
                'estimated_cost': round(duration_minutes / 60 * active_res.parking_spot.parking_lot.price_per_hour, 2)
            }
        
        # Get recent reservations
        recent_reservations = []
        for reservation in user.reservations.order_by(desc(Reservation.created_at)).limit(20):
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
        
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.full_name,
            'phone_number': user.phone_number,
            'address': user.address,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'statistics': {
                'total_reservations': total_reservations,
                'active_reservations': active_reservations,
                'completed_reservations': completed_reservations,
                'cancelled_reservations': cancelled_reservations,
                'total_spent': round(total_spent, 2),
                'average_duration_minutes': round(avg_duration, 1)
            },
            'current_reservation': current_reservation,
            'recent_reservations': recent_reservations
        }
        
        return jsonify({
            'success': True,
            'data': user_data
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading user details: {str(e)}'
        }), 500

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """Toggle user active/inactive status"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Check if user has active reservations
        if user.is_active:  # About to deactivate
            active_reservations = user.reservations.filter_by(status='active').count()
            if active_reservations > 0:
                return jsonify({
                    'success': False,
                    'message': f'Cannot deactivate user. They have {active_reservations} active reservations.'
                }), 400
        
        # Toggle status
        user.is_active = not user.is_active
        db.session.commit()
        
        status_text = "activated" if user.is_active else "deactivated"
        
        return jsonify({
            'success': True,
            'message': f'User "{user.username}" has been {status_text}',
            'data': {
                'user_id': user.id,
                'is_active': user.is_active
            }
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating user status: {str(e)}'
        }), 500

# ==================== SYSTEM STATISTICS ====================

@admin_bp.route('/statistics', methods=['GET'])
@admin_required
def get_system_statistics():
    """Get comprehensive system statistics for admin dashboard"""
    try:
        # Basic counts
        stats = {
            'users': {
                'total': User.query.count(),
                'active': User.query.filter_by(is_active=True).count(),
                'inactive': User.query.filter_by(is_active=False).count()
            },
            'parking_lots': {
                'total': ParkingLot.query.count(),
                'active': ParkingLot.query.filter_by(is_active=True).count(),
                'inactive': ParkingLot.query.filter_by(is_active=False).count()
            },
            'parking_spots': {
                'total': ParkingSpot.query.count(),
                'available': ParkingSpot.query.filter_by(status='A').count(),
                'occupied': ParkingSpot.query.filter_by(status='O').count()
            },
            'reservations': {
                'total': Reservation.query.count(),
                'active': Reservation.query.filter_by(status='active').count(),
                'completed': Reservation.query.filter_by(status='completed').count(),
                'cancelled': Reservation.query.filter_by(status='cancelled').count()
            }
        }
        
        # Calculate occupancy rate
        if stats['parking_spots']['total'] > 0:
            stats['parking_spots']['occupancy_rate'] = round(
                (stats['parking_spots']['occupied'] / stats['parking_spots']['total']) * 100, 1
            )
        else:
            stats['parking_spots']['occupancy_rate'] = 0
        
        # Revenue statistics
        total_revenue = db.session.query(func.sum(Reservation.parking_cost)).filter(
            Reservation.status == 'completed',
            Reservation.parking_cost.isnot(None)
        ).scalar() or 0
        
        stats['revenue'] = {
            'total': round(total_revenue, 2)
        }
        
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading statistics: {str(e)}'
        }), 500 