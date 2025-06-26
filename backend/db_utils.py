"""
Database Utility Functions for Vehicle Parking System
Provides helper functions for database operations
"""

from app import app, db
from models import User, Admin, ParkingLot, ParkingSpot, Reservation
from datetime import datetime

def reset_database():
    """Drop all tables and recreate them"""
    with app.app_context():
        print("⚠️  Resetting database - all data will be lost!")
        db.drop_all()
        db.create_all()
        print("✅ Database reset completed!")

def backup_database():
    """Create a simple backup of critical data"""
    with app.app_context():
        backup_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'users': [],
            'parking_lots': [],
            'reservations': []
        }
        
        # Backup users
        for user in User.query.all():
            backup_data['users'].append({
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'phone_number': user.phone_number,
                'address': user.address
            })
        
        # Backup parking lots
        for lot in ParkingLot.query.all():
            backup_data['parking_lots'].append({
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'price_per_hour': lot.price_per_hour,
                'number_of_spots': lot.number_of_spots,
                'description': lot.description
            })
        
        print(f"✅ Backup data prepared with {len(backup_data['users'])} users and {len(backup_data['parking_lots'])} lots")
        return backup_data

def check_database_health():
    """Check database integrity and relationships"""
    with app.app_context():
        print("🔍 Checking database health...")
        
        issues = []
        
        # Check for orphaned parking spots
        orphaned_spots = ParkingSpot.query.filter(~ParkingSpot.lot_id.in_(
            db.session.query(ParkingLot.id)
        )).count()
        
        if orphaned_spots > 0:
            issues.append(f"Found {orphaned_spots} orphaned parking spots")
        
        # Check for orphaned reservations
        orphaned_reservations = Reservation.query.filter(
            ~Reservation.spot_id.in_(db.session.query(ParkingSpot.id))
        ).count()
        
        if orphaned_reservations > 0:
            issues.append(f"Found {orphaned_reservations} orphaned reservations")
        
        # Check for inconsistent spot statuses
        active_reservations = Reservation.query.filter_by(status='active').all()
        for reservation in active_reservations:
            if reservation.parking_spot.status != 'O':
                issues.append(f"Spot {reservation.parking_spot.id} has active reservation but status is not 'O'")
        
        if issues:
            print("⚠️  Database issues found:")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print("✅ Database health check passed!")
        
        return len(issues) == 0

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'reset':
            reset_database()
        elif command == 'backup':
            backup_data = backup_database()
            import json
            with open('db_backup.json', 'w') as f:
                json.dump(backup_data, f, indent=2)
            print("✅ Backup saved to db_backup.json")
        elif command == 'health':
            check_database_health()
        else:
            print("Available commands: reset, backup, health")
    else:
        print("Usage: python db_utils.py [reset|backup|health]") 