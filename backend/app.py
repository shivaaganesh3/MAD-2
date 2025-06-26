from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "parking_system.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models after db initialization
from models import User, Admin, ParkingLot, ParkingSpot, Reservation

# Basic route for testing
@app.route('/')
def index():
    return {
        'message': 'Vehicle Parking System API',
        'version': '1.0',
        'status': 'active'
    }

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        user_count = User.query.count()
        return {
            'status': 'healthy',
            'database': 'connected',
            'users': user_count
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
