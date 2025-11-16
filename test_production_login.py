"""
Test production login functionality
"""
import requests
import json

def test_production_login():
    """Test admin login on production"""
    
    print("="*60)
    print("Testing Production Login")
    print("="*60)
    
    # Production API URL
    api_url = "https://movie-platform-api.onrender.com/api/auth/login"
    
    # Admin credentials
    credentials = {
        "username": "admin",
        "password": "admin"
    }
    
    print(f"\n🔗 API URL: {api_url}")
    print(f"👤 Username: {credentials['username']}")
    print(f"🔑 Password: {credentials['password']}")
    print("\n" + "="*60)
    print("Sending login request...")
    print("="*60)
    
    try:
        # Send login request
        response = requests.post(
            api_url,
            json=credentials,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\n📊 Status Code: {response.status_code}")
        print(f"📝 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ LOGIN SUCCESSFUL!")
            print("="*60)
            print(f"Full Response: {json.dumps(data, indent=2)}")
            print("="*60)
            
            access_token = data.get('access_token')
            refresh_token = data.get('refresh_token')
            
            if access_token:
                print(f"✅ Access Token: {access_token[:50]}...")
            else:
                print("❌ Access Token: NOT FOUND")
                
            if refresh_token:
                print(f"✅ Refresh Token: {refresh_token[:50]}...")
            else:
                print("❌ Refresh Token: NOT FOUND")
                
            print(f"User: {data.get('user', {}).get('username')} (Role: {data.get('user', {}).get('role')})")
            print("="*60)
            
            # Test if we can access admin endpoint
            print("\n🔍 Testing admin access...")
            token = data.get('access_token')
            
            status_response = requests.get(
                "https://movie-platform-api.onrender.com/api/admin/data-status",
                headers={"Authorization": f"Bearer {token}"},
                timeout=30
            )
            
            if status_response.status_code == 200:
                print("✅ Admin access confirmed!")
                print(f"Data Status: {status_response.json()}")
            else:
                print(f"⚠️  Admin access issue: {status_response.status_code}")
                print(f"Response: {status_response.text}")
            
            return True
            
        elif response.status_code == 404:
            print("\n❌ LOGIN FAILED - Endpoint not found")
            print("="*60)
            print("Issue: The login endpoint doesn't exist")
            print("Possible causes:")
            print("1. Admin user not initialized")
            print("2. Backend not deployed properly")
            print("3. Route not registered")
            print("\nResponse:", response.text)
            return False
            
        elif response.status_code == 401:
            print("\n❌ LOGIN FAILED - Invalid credentials")
            print("="*60)
            print("Issue: Username or password incorrect")
            print("Possible causes:")
            print("1. Admin user not created")
            print("2. Wrong credentials")
            print("\nResponse:", response.text)
            return False
            
        else:
            print(f"\n❌ LOGIN FAILED - Status {response.status_code}")
            print("="*60)
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n❌ REQUEST TIMEOUT")
        print("="*60)
        print("The server took too long to respond")
        print("Possible causes:")
        print("1. Render free tier is sleeping (first request takes ~30s)")
        print("2. Network issues")
        print("\nTry again in a moment...")
        return False
        
    except requests.exceptions.ConnectionError:
        print("\n❌ CONNECTION ERROR")
        print("="*60)
        print("Could not connect to the server")
        print("Possible causes:")
        print("1. Backend not running")
        print("2. Wrong URL")
        print("3. Network issues")
        return False
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")
        return False

def test_init_admin():
    """Test admin initialization endpoint"""
    print("\n" + "="*60)
    print("Testing Admin Initialization")
    print("="*60)
    
    api_url = "https://movie-platform-api.onrender.com/api/auth/init-admin"
    
    try:
        response = requests.post(api_url, timeout=30)
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Admin initialized successfully!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n🧪 PRODUCTION LOGIN TEST")
    print("="*60)
    
    # First, try to initialize admin
    print("\nStep 1: Initialize admin account...")
    test_init_admin()
    
    # Then test login
    print("\n\nStep 2: Test login...")
    success = test_production_login()
    
    print("\n" + "="*60)
    if success:
        print("✅ ALL TESTS PASSED - Login is working!")
    else:
        print("❌ TESTS FAILED - Login needs fixing")
    print("="*60)
