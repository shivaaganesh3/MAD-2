# Vehicle Parking System V2 - MAD-2 Project


---


## 🔧 **Setup and Installation**

### **Prerequisites**
- Python 3.8+
- Node.js 16+
- npm/yarn

### **Backend Setup**
```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python init_db.py

# Start Flask server
python app.py
```

### **Frontend Setup**
```bash
# Navigate to frontend
cd vehicle-parking-ui

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 🧪 **Testing**

### **Backend API Testing**
```bash
# Run comprehensive admin API tests
cd backend
python test_admin.py
```

**Test Coverage:**
- ✅ Admin authentication
- ✅ Parking lot CRUD operations
- ✅ User management APIs
- ✅ System statistics
- ✅ Error handling scenarios
- ✅ Data validation

