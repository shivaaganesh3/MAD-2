#!/usr/bin/env python3
"""
Test script for Authentication & Role-based Access
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_api():
    """Test the authentication API endpoints"""
    print("🧪 Testing Vehicle Parking System Authentication API")
    print("=" * 60)
    
    # Test 1: Check API info
    print("1. Testing API Info...")
    response = requests.get(f"{BASE_URL}/api/info")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ API Info endpoint working")
    else:
        print("❌ API Info endpoint failed")
    
    # Test 2: Check health
    print("\n2. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health check passed - {data['database']['users']} users, {data['database']['admins']} admins")
    else:
        print("❌ Health check failed")
    
    # Test 3: User Registration
    print("\n3. Testing User Registration...")
    user_data = {
        "username": "test_user",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "password123",
        "phone_number": "+91-9876543210"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"Registration Status: {response.status_code}")
    if response.status_code == 201:
        print("✅ User registration successful")
        user_session = requests.Session()
        user_session.cookies = response.cookies
    else:
        print(f"❌ User registration failed: {response.json().get('message', 'Unknown error')}")
        return
    
    # Test 4: User Dashboard Access
    print("\n4. Testing User Dashboard Access...")
    response = user_session.get(f"{BASE_URL}/api/dashboard/user")
    print(f"User Dashboard Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ User dashboard accessible - {data['data']['user_stats']['total_reservations']} reservations")
    else:
        print("❌ User dashboard access failed")
    
    # Test 5: User trying to access Admin Dashboard (should fail)
    print("\n5. Testing User Access to Admin Dashboard (should fail)...")
    response = user_session.get(f"{BASE_URL}/api/dashboard/admin")
    print(f"Admin Dashboard Status: {response.status_code}")
    if response.status_code == 403:
        print("✅ User correctly denied access to admin dashboard")
    else:
        print("❌ User access control failed")
    
    # Test 6: User Logout
    print("\n6. Testing User Logout...")
    response = user_session.post(f"{BASE_URL}/api/auth/logout")
    print(f"Logout Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ User logout successful")
    else:
        print("❌ User logout failed")
    
    # Test 7: Admin Login
    print("\n7. Testing Admin Login...")
    admin_data = {
        "username": "admin",
        "password": "admin123",
        "user_type": "admin"
    }
    
    admin_session = requests.Session()
    response = admin_session.post(f"{BASE_URL}/api/auth/login", json=admin_data)
    print(f"Admin Login Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Admin login successful")
    else:
        print(f"❌ Admin login failed: {response.json().get('message', 'Unknown error')}")
        return
    
    # Test 8: Admin Dashboard Access
    print("\n8. Testing Admin Dashboard Access...")
    response = admin_session.get(f"{BASE_URL}/api/dashboard/admin")
    print(f"Admin Dashboard Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Admin dashboard accessible - {data['data']['stats']['total_users']} total users")
    else:
        print("❌ Admin dashboard access failed")
    
    # Test 9: Admin Users List
    print("\n9. Testing Admin Users List...")
    response = admin_session.get(f"{BASE_URL}/api/dashboard/admin/users")
    print(f"Admin Users List Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Admin users list accessible - {data['data']['total_count']} users found")
    else:
        print("❌ Admin users list access failed")
    
    # Test 10: Admin trying to access User Dashboard (should fail)
    print("\n10. Testing Admin Access to User Dashboard (should fail)...")
    response = admin_session.get(f"{BASE_URL}/api/dashboard/user")
    print(f"User Dashboard Status: {response.status_code}")
    if response.status_code == 403:
        print("✅ Admin correctly denied access to user dashboard")
    else:
        print("❌ Admin access control failed") 