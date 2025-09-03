# Vehicle Parking System V2 - MAD-2 Project



## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **Redis** (for background tasks)
- **Git**

### Backend Setup
```bash
# Navigate to backend directory
cd MAD-2/backend

# Install Python dependencies
pip install -r requirements.txt

# Initialize database with sample data
python init_db.py

# Start Flask development server
python app.py
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd MAD-2/vehicle-parking-ui

# Install Node.js dependencies
npm install

# Start development server
npm run dev
```

### Background Tasks (Optional)
```bash
# Start Redis server
redis-server

# Start Celery worker (in backend directory)
celery -A celery_app worker --loglevel=info

# Start Celery beat scheduler (in separate terminal)
celery -A celery_app beat --loglevel=info
```

## 🔑 Default Credentials

### Admin Access
- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@parkingsystem.com`

### Test User
Create new users through the registration page or use the sample data generated during database initialization.

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/login` - User/Admin login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - Logout
- `GET /api/auth/profile` - Get user profile
- `GET /api/auth/status` - Check authentication status

### User Dashboard
- `GET /api/dashboard/user` - User dashboard data
- `GET /api/dashboard/redirect` - Role-based redirect

### Admin Management
- `GET /api/admin/parking-lots` - List parking lots
- `POST /api/admin/parking-lots` - Create parking lot
- `PUT /api/admin/parking-lots/{id}` - Update parking lot
- `DELETE /api/admin/parking-lots/{id}` - Delete parking lot
- `GET /api/admin/users` - List all users
- `POST /api/admin/users/{id}/toggle-status` - Toggle user status
- `GET /api/admin/statistics` - System statistics

## 📊 Database Models

### User
- Personal information and authentication
- Relationship to reservations

### Admin
- System administrator with full access
- Single admin account per system

### ParkingLot
- Physical parking locations
- Pricing and capacity information

### ParkingSpot
- Individual parking spaces within lots
- Real-time availability status

### Reservation
- Parking session tracking
- Cost calculation and billing

## 🔄 Background Tasks

### Scheduled Jobs
- **Daily Reminders** - 9:59 PM daily
- **Monthly Reports** - 15th of each month at 9:59 PM
- **CSV Export** - On-demand data export

### Email Notifications
- Daily engagement reminders
- Monthly activity reports
- Export completion notifications

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM and database management
- **PyJWT** - JSON Web Token authentication
- **Celery** - Background task processing
- **Redis** - Message broker and cache
- **SMTP** - Email notifications

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vue Router** - Client-side routing
- **Axios** - HTTP client
- **Bootstrap** - CSS framework
- **Vite** - Build tool and dev server

