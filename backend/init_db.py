#!/usr/bin/env python3
"""
Database Initialization Script for Vehicle Parking System
This script creates the database schema and populates initial data programmatically
"""

import os
import sys
from datetime import datetime

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db
from models import User, Admin, ParkingLot, ParkingSpot, Reservation

def create_database():
    """Create all database tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")

def create_admin():
    """Create the predefined admin user"""
    with app.app_context():
        # Check if admin already exists
        existing_admin = Admin.query.filter_by(username='admin').first()
        if existing_admin:
            print("ℹ️  Admin already exists, skipping creation")
            return existing_admin
        
        # Create new admin
        admin = Admin(
            username='admin',
            email='admin@parkingsystem.com'
        )
        admin.set_password('admin123')  # Default password - change in production
        
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin user created successfully!")
        print(f"   Username: admin")
        print(f"   Password: admin123")
        print(f"   Email: admin@parkingsystem.com")
        return admin

def create_sample_parking_lots():
    """Create sample parking lots with their spots"""
    with app.app_context():
        # Check if parking lots already exist
        if ParkingLot.query.count() > 0:
            print("ℹ️  Parking lots already exist, skipping creation")
            return
        
        print("Creating sample parking lots...")
        
        # Sample parking lots data
        lots_data = [
            {
                'prime_location_name': 'Downtown Mall',
                'address': '123 Main Street, Downtown Area',
                'pin_code': '560001',
                'price_per_hour': 50.0,
                'number_of_spots': 20,
                'description': 'Prime location near shopping mall and business district'
            },
            {
                'prime_location_name': 'Airport Terminal',
                'address': 'Kempegowda International Airport, Terminal 1',
                'pin_code': '560300',
                'price_per_hour': 100.0,
                'number_of_spots': 50,
                'description': 'Convenient parking for airport travelers'
            },
            {
                'prime_location_name': 'Tech Park Central',
                'address': 'Electronic City Phase 1, Bangalore',
                'pin_code': '560100',
                'price_per_hour': 30.0,
                'number_of_spots': 30,
                'description': 'Parking facility for tech park employees and visitors'
            }
        ]
        
        for lot_data in lots_data:
            # Create parking lot
            parking_lot = ParkingLot(**lot_data)
            db.session.add(parking_lot)
            db.session.flush()  # Get the ID without committing
            
            # Create parking spots for this lot
            create_parking_spots_for_lot(parking_lot)
            
            print(f"✅ Created parking lot: {parking_lot.prime_location_name} with {parking_lot.number_of_spots} spots")
        
        db.session.commit()
        print("✅ All sample parking lots created successfully!")

def create_parking_spots_for_lot(parking_lot):
    """Create parking spots for a given parking lot"""
    spots_per_row = 10  # Assuming 10 spots per row
    rows = ['A', 'B', 'C', 'D', 'E', 'F']  # Row identifiers
    
    spot_count = 0
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
            spot_count += 1

def create_sample_users():
    """Create sample users for testing"""
    with app.app_context():
        # Check if users already exist
        if User.query.count() > 0:
            print("ℹ️  Sample users already exist, skipping creation")
            return
        
        print("Creating sample users...")
        
        sample_users = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'full_name': 'John Doe',
                'phone_number': '+91-9876543210',
                'address': '123 Sample Street, Bangalore',
                'password': 'password123'
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'full_name': 'Jane Smith',
                'phone_number': '+91-9876543211',
                'address': '456 Test Avenue, Bangalore',
                'password': 'password123'
            }
        ]
        
        for user_data in sample_users:
            password = user_data.pop('password')
            user = User(**user_data)
            user.set_password(password)
            db.session.add(user)
            print(f"✅ Created user: {user.username}")
        
        db.session.commit()
        print("✅ Sample users created successfully!")

def display_database_summary():
    """Display a summary of the created database"""
    with app.app_context():
        print("\n" + "="*50)
        print("DATABASE SUMMARY")
        print("="*50)
        
        # Admin count
        admin_count = Admin.query.count()
        print(f"👤 Admins: {admin_count}")
        
        # User count
        user_count = User.query.count()
        print(f"👥 Users: {user_count}")
        
        # Parking lots summary
        lot_count = ParkingLot.query.count()
        print(f"🏢 Parking Lots: {lot_count}")
        
        for lot in ParkingLot.query.all():
            available_spots = lot.available_spots_count
            total_spots = lot.number_of_spots
            print(f"   📍 {lot.prime_location_name}: {available_spots}/{total_spots} available")
        
        # Total spots
        total_spots = ParkingSpot.query.count()
        available_spots = ParkingSpot.query.filter_by(status='A').count()
        occupied_spots = ParkingSpot.query.filter_by(status='O').count()
        print(f"🅿️  Total Parking Spots: {total_spots}")
        print(f"   ✅ Available: {available_spots}")
        print(f"   🔴 Occupied: {occupied_spots}")
        
        # Reservations
        reservation_count = Reservation.query.count()
        active_reservations = Reservation.query.filter_by(status='active').count()
        print(f"📝 Reservations: {reservation_count}")
        print(f"   🟢 Active: {active_reservations}")
        
        print("="*50)

def main():
    """Main function to initialize the entire database"""
    print("🚀 Initializing Vehicle Parking System Database...")
    print("="*60)
    
    try:
        # Step 1: Create database tables
        create_database()
        
        # Step 2: Create admin user
        create_admin()
        
        # Step 3: Create sample parking lots and spots
        create_sample_parking_lots()
        
        # Step 4: Create sample users
        create_sample_users()
        
        # Step 5: Display summary
        display_database_summary()
        
        print("\n🎉 Database initialization completed successfully!")
        print("\nNext Steps:")
        print("1. Run the Flask application: python app.py")
        print("2. Admin login: username='admin', password='admin123'")
        print("3. User login: username='john_doe', password='password123'")
        
    except Exception as e:
        print(f"❌ Error during database initialization: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    main() 