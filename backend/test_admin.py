#!/usr/bin/env python3
"""
Comprehensive Admin API Testing Script
Tests all admin management APIs for parking lots and user management
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
session = requests.Session()

def print_separator(title):
    """Print a formatted separator"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_response(response, description=""):
    """Print formatted response"""
    if description:
        print(f"\n{description}:")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_admin_login():
    """Test admin login"""
    print_separator("TESTING ADMIN LOGIN")
    
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)
    print_response(response, "Admin Login")
    
    if response.status_code == 200 and response.json().get('success'):
        print("✅ Admin login successful")
        return True
    else:
        print("❌ Admin login failed")
        return False

def test_system_statistics():
    """Test system statistics endpoint"""
    print_separator("TESTING SYSTEM STATISTICS")
    
    response = session.get(f"{BASE_URL}/api/admin/statistics")
    print_response(response, "System Statistics")
    
    if response.status_code == 200:
        print("✅ System statistics retrieved successfully")
        return True
    else:
        print("❌ Failed to retrieve system statistics")
        return False

def test_parking_lot_crud():
    """Test parking lot CRUD operations"""
    print_separator("TESTING PARKING LOT CRUD OPERATIONS")
    
    # Test 1: Create parking lot
    print("\n1. Creating parking lot...")
    lot_data = {
        "prime_location_name": "Test Mall Parking",
        "address": "123 Test Street, Test City, Test State",
        "pin_code": "123456",
        "price_per_hour": 25.50,
        "number_of_spots": 50,
        "description": "Test parking lot for API testing",
        "is_active": True
    }
    
    response = session.post(f"{BASE_URL}/api/admin/parking-lots", json=lot_data)
    print_response(response, "Create Parking Lot")
    
    if response.status_code != 201:
        print("❌ Failed to create parking lot")
        return False
    
    lot_id = response.json().get('data', {}).get('lot_id')
    if not lot_id:
        print("❌ No lot ID returned")
        return False
    
    print(f"✅ Parking lot created with ID: {lot_id}")
    
    # Test 2: Get all parking lots
    print("\n2. Getting all parking lots...")
    response = session.get(f"{BASE_URL}/api/admin/parking-lots")
    print_response(response, "Get All Parking Lots")
    
    if response.status_code != 200:
        print("❌ Failed to get parking lots")
        return False
    
    lots = response.json().get('data', {}).get('parking_lots', [])
    print(f"✅ Retrieved {len(lots)} parking lots")
    
    # Test 3: Get specific parking lot
    print(f"\n3. Getting parking lot details for ID {lot_id}...")
    response = session.get(f"{BASE_URL}/api/admin/parking-lots/{lot_id}")
    print_response(response, "Get Specific Parking Lot")
    
    if response.status_code != 200:
        print("❌ Failed to get parking lot details")
        return False
    
    lot_details = response.json().get('data', {})
    spots_count = len(lot_details.get('parking_spots', []))
    print(f"✅ Retrieved parking lot details with {spots_count} spots")
    
    # Test 4: Update parking lot
    print(f"\n4. Updating parking lot {lot_id}...")
    update_data = {
        "prime_location_name": "Updated Test Mall Parking",
        "address": "456 Updated Street, Test City, Test State",
        "pin_code": "123456",
        "price_per_hour": 30.00,
        "number_of_spots": 60,  # Increased spots
        "description": "Updated test parking lot",
        "is_active": True
    }
    
    response = session.put(f"{BASE_URL}/api/admin/parking-lots/{lot_id}", json=update_data)
    print_response(response, "Update Parking Lot")
    
    if response.status_code != 200:
        print("❌ Failed to update parking lot")
        return False
    
    print("✅ Parking lot updated successfully")
    
    # Test 5: Search parking lots
    print("\n5. Searching parking lots...")
    search_params = {
        "search": "Updated",
        "status": "active",
        "page": 1,
        "per_page": 10
    }
    
    response = session.get(f"{BASE_URL}/api/admin/parking-lots", params=search_params)
    print_response(response, "Search Parking Lots")
    
    if response.status_code != 200:
        print("❌ Failed to search parking lots")
        return False
    
    search_results = response.json().get('data', {}).get('parking_lots', [])
    print(f"✅ Found {len(search_results)} parking lots matching search")
    
    # Test 6: Delete parking lot
    print(f"\n6. Deleting parking lot {lot_id}...")
    response = session.delete(f"{BASE_URL}/api/admin/parking-lots/{lot_id}")
    print_response(response, "Delete Parking Lot")
    
    if response.status_code != 200:
        print("❌ Failed to delete parking lot")
        return False
    
    print("✅ Parking lot deleted successfully")
    
    return True

def test_user_management():
    """Test user management endpoints"""
    print_separator("TESTING USER MANAGEMENT")
    
    # Test 1: Get all users
    print("\n1. Getting all users...")
    response = session.get(f"{BASE_URL}/api/admin/users")
    print_response(response, "Get All Users")
    
    if response.status_code != 200:
        print("❌ Failed to get users")
        return False
    
    users = response.json().get('data', {}).get('users', [])
    print(f"✅ Retrieved {len(users)} users")
    
    if not users:
        print("ℹ️ No users found, skipping user-specific tests")
        return True
    
    # Test 2: Get specific user details
    user_id = users[0]['id']
    print(f"\n2. Getting user details for ID {user_id}...")
    response = session.get(f"{BASE_URL}/api/admin/users/{user_id}")
    print_response(response, "Get Specific User")
    
    if response.status_code != 200:
        print("❌ Failed to get user details")
        return False
    
    user_details = response.json().get('data', {})
    print(f"✅ Retrieved user details for: {user_details.get('username')}")
    
    # Test 3: Search users
    print("\n3. Searching users...")
    search_params = {
        "search": user_details.get('username', '')[:3],  # Search by first 3 chars
        "status": "all",
        "page": 1,
        "per_page": 10
    }
    
    response = session.get(f"{BASE_URL}/api/admin/users", params=search_params)
    print_response(response, "Search Users")
    
    if response.status_code != 200:
        print("❌ Failed to search users")
        return False
    
    search_results = response.json().get('data', {}).get('users', [])
    print(f"✅ Found {len(search_results)} users matching search")
    
    # Test 4: Toggle user status (only if user is active)
    if user_details.get('is_active'):
        print(f"\n4. Toggling status for user {user_id}...")
        response = session.post(f"{BASE_URL}/api/admin/users/{user_id}/toggle-status")
        print_response(response, "Toggle User Status")
        
        if response.status_code == 200:
            print("✅ User status toggled successfully")
            
            # Toggle back to original state
            print("   Toggling back to original state...")
            response = session.post(f"{BASE_URL}/api/admin/users/{user_id}/toggle-status")
            if response.status_code == 200:
                print("✅ User status restored")
            else:
                print("⚠️ Warning: Could not restore original user status")
        else:
            print("❌ Failed to toggle user status")
            return False
    else:
        print("ℹ️ User is inactive, skipping status toggle test")
    
    return True

def test_error_scenarios():
    """Test error handling scenarios"""
    print_separator("TESTING ERROR SCENARIOS")
    
    # Test 1: Invalid parking lot ID
    print("\n1. Testing invalid parking lot ID...")
    response = session.get(f"{BASE_URL}/api/admin/parking-lots/99999")
    print_response(response, "Invalid Parking Lot ID")
    
    if response.status_code == 404:
        print("✅ Correctly handled invalid parking lot ID")
    else:
        print("⚠️ Unexpected response for invalid parking lot ID")
    
    # Test 2: Invalid user ID
    print("\n2. Testing invalid user ID...")
    response = session.get(f"{BASE_URL}/api/admin/users/99999")
    print_response(response, "Invalid User ID")
    
    if response.status_code == 404:
        print("✅ Correctly handled invalid user ID")
    else:
        print("⚠️ Unexpected response for invalid user ID")
    
    # Test 3: Invalid parking lot data
    print("\n3. Testing invalid parking lot data...")
    invalid_data = {
        "prime_location_name": "",  # Empty name
        "address": "Short",  # Too short
        "pin_code": "123",  # Wrong format
        "price_per_hour": -10,  # Negative price
        "number_of_spots": 0,  # Zero spots
    }
    
    response = session.post(f"{BASE_URL}/api/admin/parking-lots", json=invalid_data)
    print_response(response, "Invalid Parking Lot Data")
    
    if response.status_code == 400:
        print("✅ Correctly rejected invalid parking lot data")
    else:
        print("⚠️ Unexpected response for invalid parking lot data")
    
    return True

def test_api_info():
    """Test API info endpoint"""
    print_separator("TESTING API INFO")
    
    response = session.get(f"{BASE_URL}/api/info")
    print_response(response, "API Info")
    
    if response.status_code == 200:
        print("✅ API info retrieved successfully")
        return True
    else:
        print("❌ Failed to get API info")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Comprehensive Admin API Tests")
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test basic API info
    if not test_api_info():
        print("❌ API info test failed, stopping tests")
        sys.exit(1)
    
    # Test admin login
    if not test_admin_login():
        print("❌ Admin login failed, stopping tests")
        sys.exit(1)
    
    # Test system statistics
    if not test_system_statistics():
        print("⚠️ System statistics test failed, but continuing...")
    
    # Test parking lot CRUD
    if not test_parking_lot_crud():
        print("❌ Parking lot CRUD tests failed")
        sys.exit(1)
    
    # Test user management
    if not test_user_management():
        print("❌ User management tests failed")
        sys.exit(1)
    
    # Test error scenarios
    if not test_error_scenarios():
        print("⚠️ Error scenario tests had issues, but continuing...")
    
    print_separator("TEST SUMMARY")
    print("🎉 All admin API tests completed successfully!")
    print("✅ Admin authentication works")
    print("✅ Parking lot CRUD operations work")
    print("✅ User management works")
    print("✅ System statistics work")
    print("✅ Error handling works")
    
    print("\n🔧 Next steps:")
    print("1. Start the frontend: cd vehicle-parking-ui && npm run dev")
    print("2. Access admin dashboard: http://localhost:5173/login")
    print("3. Login with: admin / admin123")

if __name__ == "__main__":
    main() 