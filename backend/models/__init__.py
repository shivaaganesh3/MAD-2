
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class User(db.Model):
    """
    User model for registered users who can book parking spots
    Inherits from UserMixin for Flask-Login compatibility
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    reservations = db.relationship('Reservation', back_populates='user', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    # Flask-Login required properties
    def get_id(self):
        """Return the user ID as a string"""
        return str(self.id)
    
    @property
    def is_authenticated(self):
        """Return True if user is authenticated"""
        return True
    
    @property
    def is_anonymous(self):
        """Return False as this is not an anonymous user"""
        return False
    
    def get_role(self):
        """Return user role for RBAC"""
        return 'user'
    
    def to_dict(self):
        """Convert user to dictionary for JSON response"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
            'role': self.get_role()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Admin(db.Model):
    """
    Admin model - predefined superuser with root access
    Only one admin should exist in the system
    Inherits from UserMixin for Flask-Login compatibility
    """
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, default='admin')
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    # Flask-Login required properties
    def get_id(self):
        """Return the admin ID as a string with admin prefix"""
        return f"admin_{self.id}"
    
    @property
    def is_authenticated(self):
        """Return True if admin is authenticated"""
        return True
    
    @property
    def is_anonymous(self):
        """Return False as this is not an anonymous user"""
        return False
    
    def get_role(self):
        """Return admin role for RBAC"""
        return 'admin'
    
    def to_dict(self):
        """Convert admin to dictionary for JSON response"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'role': self.get_role()
        }
    
    def __repr__(self):
        return f'<Admin {self.username}>'


class ParkingLot(db.Model):
    """
    Parking Lot model representing physical parking areas
    """
    __tablename__ = 'parking_lots'
    
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)  # Price per hour for parking
    number_of_spots = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parking_spots = db.relationship('ParkingSpot', back_populates='parking_lot', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def available_spots_count(self):
        """Get count of available parking spots"""
        return self.parking_spots.filter_by(status='A').count()
    
    @property
    def occupied_spots_count(self):
        """Get count of occupied parking spots"""
        return self.parking_spots.filter_by(status='O').count()
    
    def __repr__(self):
        return f'<ParkingLot {self.prime_location_name}>'


class ParkingSpot(db.Model):
    """
    Parking Spot model representing individual parking spaces within a lot
    """
    __tablename__ = 'parking_spots'
    
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    spot_number = db.Column(db.String(10), nullable=False)  # e.g., "A1", "B12"
    status = db.Column(db.String(1), nullable=False, default='A')  # 'A' = Available, 'O' = Occupied
    vehicle_type = db.Column(db.String(20), default='4-wheeler')  # Fixed for 4-wheelers
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parking_lot = db.relationship('ParkingLot', back_populates='parking_spots')
    reservations = db.relationship('Reservation', back_populates='parking_spot', lazy='dynamic')
    
    # Composite unique constraint for lot_id and spot_number
    __table_args__ = (db.UniqueConstraint('lot_id', 'spot_number', name='_lot_spot_uc'),)
    
    @property
    def current_reservation(self):
        """Get current active reservation for this spot"""
        return self.reservations.filter_by(status='active').first()
    
    def __repr__(self):
        return f'<ParkingSpot {self.spot_number} in Lot {self.lot_id}>'


class Reservation(db.Model):
    """
    Reservation model tracking parking bookings and their details
    """
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Timestamps
    parking_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime, nullable=True)
    
    # Cost and Status
    parking_cost = db.Column(db.Float, nullable=True)  # Calculated when leaving
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'cancelled'
    
    # Vehicle details
    vehicle_number = db.Column(db.String(20), nullable=False)
    vehicle_model = db.Column(db.String(50), nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    parking_spot = db.relationship('ParkingSpot', back_populates='reservations')
    user = db.relationship('User', back_populates='reservations')
    
    @property
    def duration_minutes(self):
        """Calculate parking duration in minutes"""
        if self.leaving_timestamp:
            duration = self.leaving_timestamp - self.parking_timestamp
            return int(duration.total_seconds() / 60)
        return 0
    
    @property
    def duration_hours(self):
        """Calculate parking duration in hours (rounded up)"""
        if self.leaving_timestamp:
            duration = self.leaving_timestamp - self.parking_timestamp
            hours = duration.total_seconds() / 3600
            return max(1, int(hours) + (1 if hours % 1 > 0 else 0))  # Round up, minimum 1 hour
        return 0
    
    @property
    def current_duration_minutes(self):
        """Calculate current duration in minutes for active reservations"""
        if self.status == 'active':
            duration = datetime.utcnow() - self.parking_timestamp
            return int(duration.total_seconds() / 60)
        return self.duration_minutes
    
    @property
    def current_duration_hours(self):
        """Calculate current duration in hours for active reservations"""
        if self.status == 'active':
            duration = datetime.utcnow() - self.parking_timestamp
            hours = duration.total_seconds() / 3600
            return round(hours, 2)
        return self.duration_hours if self.leaving_timestamp else 0
    
    @property
    def estimated_cost(self):
        """Calculate estimated cost for active reservations"""
        if self.status == 'active' and self.parking_spot:
            hours = self.current_duration_hours
            return round(hours * self.parking_spot.parking_lot.price_per_hour, 2)
        return self.parking_cost or 0
    
    def calculate_cost(self):
        """Calculate parking cost based on duration and lot price"""
        if self.leaving_timestamp and self.parking_spot:
            hours = self.duration_hours
            cost = hours * self.parking_spot.parking_lot.price_per_hour
            self.parking_cost = round(cost, 2)
            return self.parking_cost
        return 0
    
    def get_cost_breakdown(self):
        """Get detailed cost breakdown for this reservation"""
        if not self.parking_spot:
            return None
        
        breakdown = {
            'hourly_rate': self.parking_spot.parking_lot.price_per_hour,
            'billing_method': 'hourly',
            'currency': 'INR'
        }
        
        if self.status == 'active':
            # Active reservation - estimated cost
            current_minutes = self.current_duration_minutes
            current_hours = self.current_duration_hours
            estimated_cost = self.estimated_cost
            
            breakdown.update({
                'duration_minutes': current_minutes,
                'duration_hours': current_hours,
                'estimated_cost': estimated_cost,
                'billing_hours': round(current_hours, 2),
                'is_final': False,
                'cost_calculation': f"{current_hours:.2f} hours × ₹{self.parking_spot.parking_lot.price_per_hour}/hour = ₹{estimated_cost}"
            })
        
        elif self.status == 'completed' and self.leaving_timestamp:
            # Completed reservation - final cost
            breakdown.update({
                'duration_minutes': self.duration_minutes,
                'duration_hours': self.duration_hours,
                'actual_hours': round((self.leaving_timestamp - self.parking_timestamp).total_seconds() / 3600, 2),
                'billing_hours': self.duration_hours,  # Rounded up for billing
                'final_cost': self.parking_cost,
                'is_final': True,
                'cost_calculation': f"{self.duration_hours} billing hours × ₹{self.parking_spot.parking_lot.price_per_hour}/hour = ₹{self.parking_cost}"
            })
        
        else:
            # Cancelled or incomplete reservation
            breakdown.update({
                'duration_minutes': 0,
                'duration_hours': 0,
                'final_cost': 0,
                'is_final': True,
                'cost_calculation': 'No cost - reservation was cancelled'
            })
        
        return breakdown
    
    def get_revenue_stats(self):
        """Get revenue statistics for this reservation"""
        if not self.parking_spot:
            return None
        
        return {
            'lot_name': self.parking_spot.parking_lot.prime_location_name,
            'lot_id': self.parking_spot.parking_lot.id,
            'spot_number': self.parking_spot.spot_number,
            'user_name': self.user.full_name,
            'user_id': self.user.id,
            'cost': self.parking_cost or 0,
            'duration_hours': self.duration_hours if self.status == 'completed' else 0,
            'hourly_rate': self.parking_spot.parking_lot.price_per_hour,
            'status': self.status,
            'date': self.parking_timestamp.date().isoformat() if self.parking_timestamp else None
        }
    
    def __repr__(self):
        return f'<Reservation {self.id} - User {self.user_id} - Spot {self.spot_id}>' 