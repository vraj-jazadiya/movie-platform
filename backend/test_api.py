"""
Comprehensive API Testing Script
Tests all endpoints of the Movie Platform API
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Test results
test_results = {
    'passed': 0,
    'failed': 0,
    'total': 0
}

def print_test(test_name, status, message=""):
    """Print test result with color"""
    test_results['total'] += 1
    if status:
        test_results['passed'] += 1
        print(f"{GREEN}✓{RESET} {test_name}")
        if message:
            print(f"  {BLUE}→{RESET} {message}")
    else:
        test_results['failed'] += 1
        print(f"{RED}✗{RESET} {test_name}")
        if message:
            print(f"  {RED}→{RESET} {message}")

def print_section(title):
    """Print section header"""
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}{title}{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}\n")

# Store tokens and IDs for subsequent tests
tokens = {}
user_data = {}
movie_data = {}
playlist_data = {}
news_data = {}
chat_data = {}

def test_health_check():
    """Test health check endpoint"""
    print_section("1. HEALTH CHECK")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_test("Health check endpoint", response.status_code == 200, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Health check endpoint", False, str(e))

def test_admin_initialization():
    """Test admin account initialization"""
    print_section("2. ADMIN INITIALIZATION")
    try:
        response = requests.post(f"{BASE_URL}/auth/init-admin")
        success = response.status_code in [200, 201, 409]  # 409 if already exists
        print_test("Initialize admin account", success, 
                   f"Status: {response.status_code}, Message: {response.json().get('message', '')}")
    except Exception as e:
        print_test("Initialize admin account", False, str(e))

def test_user_registration():
    """Test user registration"""
    print_section("3. USER REGISTRATION")
    
    # Test valid registration
    try:
        payload = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "password": "testpass123",
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        success = response.status_code in [200, 201]
        if success:
            user_data['test_user'] = payload
        print_test("Register new user", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Register new user", False, str(e))
    
    # Test duplicate username
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        success = response.status_code == 409
        print_test("Reject duplicate username", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Reject duplicate username", False, str(e))
    
    # Test invalid email
    try:
        invalid_payload = {
            "username": "testuser2",
            "email": "invalid-email",
            "password": "testpass123",
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=invalid_payload)
        success = response.status_code == 400
        print_test("Reject invalid email", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Reject invalid email", False, str(e))

def test_user_login():
    """Test user login"""
    print_section("4. USER LOGIN")
    
    # Test admin login
    try:
        payload = {
            "username": "admin",
            "password": "admin"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        success = response.status_code == 200
        if success:
            data = response.json()
            tokens['admin'] = data.get('access_token')
            user_data['admin'] = data.get('user')
        print_test("Admin login", success, 
                   f"Status: {response.status_code}, Token received: {bool(tokens.get('admin'))}")
    except Exception as e:
        print_test("Admin login", False, str(e))
    
    # Test regular user login
    if 'test_user' in user_data:
        try:
            payload = {
                "username": user_data['test_user']['username'],
                "password": user_data['test_user']['password']
            }
            response = requests.post(f"{BASE_URL}/auth/login", json=payload)
            success = response.status_code == 200
            if success:
                data = response.json()
                tokens['user'] = data.get('access_token')
            print_test("User login", success, 
                       f"Status: {response.status_code}, Token received: {bool(tokens.get('user'))}")
        except Exception as e:
            print_test("User login", False, str(e))
    
    # Test invalid credentials
    try:
        payload = {
            "username": "admin",
            "password": "wrongpassword"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        success = response.status_code == 401
        print_test("Reject invalid credentials", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Reject invalid credentials", False, str(e))

def test_get_current_user():
    """Test get current user endpoint"""
    print_section("5. GET CURRENT USER")
    
    if 'admin' in tokens:
        try:
            headers = {"Authorization": f"Bearer {tokens['admin']}"}
            response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
            success = response.status_code == 200
            if success:
                data = response.json()
                print_test("Get current user (admin)", success, 
                           f"Username: {data.get('username')}, Role: {data.get('role')}")
        except Exception as e:
            print_test("Get current user (admin)", False, str(e))
    
    # Test without token
    try:
        response = requests.get(f"{BASE_URL}/auth/me")
        success = response.status_code == 401
        print_test("Reject request without token", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Reject request without token", False, str(e))

def test_movie_search():
    """Test movie search endpoints"""
    print_section("6. MOVIE SEARCH")
    
    # Test search by title
    try:
        response = requests.get(f"{BASE_URL}/movies/search", params={"q": "inception"})
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("Search movies by title", success, 
                       f"Found {len(data.get('movies', []))} movies")
    except Exception as e:
        print_test("Search movies by title", False, str(e))
    
    # Test search with year
    try:
        response = requests.get(f"{BASE_URL}/movies/search", params={"q": "avengers", "year": "2012"})
        success = response.status_code == 200
        print_test("Search movies with year filter", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Search movies with year filter", False, str(e))
    
    # Test empty search
    try:
        response = requests.get(f"{BASE_URL}/movies/search", params={"q": ""})
        success = response.status_code == 400
        print_test("Reject empty search query", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Reject empty search query", False, str(e))

def test_movie_fetch():
    """Test fetch movie by IMDb ID"""
    print_section("7. FETCH MOVIE BY IMDB ID")
    
    # Test valid IMDb ID
    try:
        imdb_id = "tt1375666"  # Inception
        response = requests.get(f"{BASE_URL}/movies/fetch/{imdb_id}")
        success = response.status_code == 200
        if success:
            data = response.json()
            movie_data['inception'] = data
            print_test("Fetch movie by IMDb ID", success, 
                       f"Title: {data.get('title')}, Year: {data.get('year')}")
    except Exception as e:
        print_test("Fetch movie by IMDb ID", False, str(e))
    
    # Test invalid IMDb ID
    try:
        response = requests.get(f"{BASE_URL}/movies/fetch/invalid123")
        success = response.status_code == 404
        print_test("Reject invalid IMDb ID", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Reject invalid IMDb ID", False, str(e))

def test_movie_operations():
    """Test movie operations"""
    print_section("8. MOVIE OPERATIONS")
    
    # Test get trending movies
    try:
        response = requests.get(f"{BASE_URL}/movies/trending", params={"limit": 5})
        success = response.status_code == 200
        print_test("Get trending movies", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Get trending movies", False, str(e))
    
    # Test get top rated movies
    try:
        response = requests.get(f"{BASE_URL}/movies/top-rated", params={"limit": 5})
        success = response.status_code == 200
        print_test("Get top rated movies", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Get top rated movies", False, str(e))
    
    # Test get production houses
    try:
        response = requests.get(f"{BASE_URL}/movies/production-houses")
        success = response.status_code == 200
        if success:
            data = response.json()
            print_test("Get production houses list", success, 
                       f"Found {len(data.get('production_houses', []))} studios")
    except Exception as e:
        print_test("Get production houses list", False, str(e))

def test_profile_operations():
    """Test profile operations"""
    print_section("9. PROFILE OPERATIONS")
    
    if 'user' not in tokens:
        print_test("Profile operations", False, "No user token available")
        return
    
    headers = {"Authorization": f"Bearer {tokens['user']}"}
    
    # Test get profile
    try:
        response = requests.get(f"{BASE_URL}/profile/", headers=headers)
        success = response.status_code == 200
        print_test("Get user profile", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Get user profile", False, str(e))
    
    # Test update profile
    try:
        payload = {
            "name": "Updated Test User",
            "bio": "This is my updated bio"
        }
        response = requests.put(f"{BASE_URL}/profile/update", json=payload, headers=headers)
        success = response.status_code == 200
        print_test("Update user profile", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Update user profile", False, str(e))
    
    # Test add to favorites
    if 'inception' in movie_data:
        try:
            movie_id = movie_data['inception'].get('_id', 'test_movie_id')
            response = requests.post(f"{BASE_URL}/profile/favorites/{movie_id}", headers=headers)
            success = response.status_code in [200, 201]
            print_test("Add movie to favorites", success, 
                       f"Status: {response.status_code}")
        except Exception as e:
            print_test("Add movie to favorites", False, str(e))

def test_playlist_operations():
    """Test playlist operations"""
    print_section("10. PLAYLIST OPERATIONS")
    
    if 'user' not in tokens:
        print_test("Playlist operations", False, "No user token available")
        return
    
    headers = {"Authorization": f"Bearer {tokens['user']}"}
    
    # Test create playlist
    try:
        payload = {
            "name": "My Test Playlist",
            "description": "A playlist for testing",
            "is_public": True
        }
        response = requests.post(f"{BASE_URL}/playlists/", json=payload, headers=headers)
        success = response.status_code in [200, 201]
        if success:
            data = response.json()
            playlist_data['test_playlist'] = data
        print_test("Create playlist", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Create playlist", False, str(e))
    
    # Test add movie to playlist
    if 'test_playlist' in playlist_data and 'inception' in movie_data:
        try:
            playlist_id = playlist_data['test_playlist'].get('_id')
            movie_payload = {
                "imdb_id": "tt1375666",
                "title": "Inception",
                "year": "2010",
                "poster": "https://example.com/poster.jpg"
            }
            response = requests.post(f"{BASE_URL}/playlists/{playlist_id}/movies", 
                                    json=movie_payload, headers=headers)
            success = response.status_code in [200, 201]
            print_test("Add movie to playlist", success, 
                       f"Status: {response.status_code}")
        except Exception as e:
            print_test("Add movie to playlist", False, str(e))
    
    # Test get playlist
    if 'test_playlist' in playlist_data:
        try:
            playlist_id = playlist_data['test_playlist'].get('_id')
            response = requests.get(f"{BASE_URL}/playlists/{playlist_id}", headers=headers)
            success = response.status_code == 200
            print_test("Get playlist by ID", success, 
                       f"Status: {response.status_code}")
        except Exception as e:
            print_test("Get playlist by ID", False, str(e))

def test_news_operations():
    """Test news operations"""
    print_section("11. NEWS OPERATIONS")
    
    # Test get all news (public)
    try:
        response = requests.get(f"{BASE_URL}/news/")
        success = response.status_code == 200
        print_test("Get all news (public)", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Get all news (public)", False, str(e))
    
    # Test get latest news
    try:
        response = requests.get(f"{BASE_URL}/news/latest", params={"limit": 5})
        success = response.status_code == 200
        print_test("Get latest news", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Get latest news", False, str(e))
    
    # Test create news (admin only)
    if 'admin' in tokens:
        try:
            headers = {"Authorization": f"Bearer {tokens['admin']}"}
            payload = {
                "title": "Test News Article",
                "content": "This is a test news article content",
                "category": "movies",
                "image_url": "https://example.com/news.jpg"
            }
            response = requests.post(f"{BASE_URL}/news/", json=payload, headers=headers)
            success = response.status_code in [200, 201]
            if success:
                data = response.json()
                news_data['test_article'] = data
            print_test("Create news article (admin)", success, 
                       f"Status: {response.status_code}")
        except Exception as e:
            print_test("Create news article (admin)", False, str(e))
    
    # Test create news (non-admin) - should fail
    if 'user' in tokens:
        try:
            headers = {"Authorization": f"Bearer {tokens['user']}"}
            payload = {
                "title": "Unauthorized News",
                "content": "This should fail",
                "category": "movies"
            }
            response = requests.post(f"{BASE_URL}/news/", json=payload, headers=headers)
            success = response.status_code == 403
            print_test("Reject news creation by non-admin", success, 
                       f"Status: {response.status_code}")
        except Exception as e:
            print_test("Reject news creation by non-admin", False, str(e))

def test_chat_operations():
    """Test chat operations"""
    print_section("12. CHAT OPERATIONS")
    
    if 'user' not in tokens:
        print_test("Chat operations", False, "No user token available")
        return
    
    headers = {"Authorization": f"Bearer {tokens['user']}"}
    
    # Test get or create chat
    try:
        response = requests.get(f"{BASE_URL}/chat/my-chat", headers=headers)
        success = response.status_code == 200
        if success:
            data = response.json()
            chat_data['user_chat'] = data
        print_test("Get or create user chat", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Get or create user chat", False, str(e))
    
    # Test send message
    if 'user_chat' in chat_data:
        try:
            chat_id = chat_data['user_chat'].get('_id')
            payload = {"message": "Hello, this is a test message"}
            response = requests.post(f"{BASE_URL}/chat/{chat_id}/message", 
                                    json=payload, headers=headers)
            success = response.status_code in [200, 201]
            print_test("Send chat message", success, 
                       f"Status: {response.status_code}")
        except Exception as e:
            print_test("Send chat message", False, str(e))

def test_contact_operations():
    """Test contact form operations"""
    print_section("13. CONTACT FORM")
    
    # Test submit contact form
    try:
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test Subject",
            "message": "This is a test contact message"
        }
        response = requests.post(f"{BASE_URL}/contact/", json=payload)
        success = response.status_code in [200, 201]
        print_test("Submit contact form", success, 
                   f"Status: {response.status_code}")
    except Exception as e:
        print_test("Submit contact form", False, str(e))
    
    # Test get all contacts (admin only)
    if 'admin' in tokens:
        try:
            headers = {"Authorization": f"Bearer {tokens['admin']}"}
            response = requests.get(f"{BASE_URL}/contact/all", headers=headers)
            success = response.status_code == 200
            print_test("Get all contacts (admin)", success, 
                       f"Status: {response.status_code}")
        except Exception as e:
            print_test("Get all contacts (admin)", False, str(e))

def print_summary():
    """Print test summary"""
    print_section("TEST SUMMARY")
    total = test_results['total']
    passed = test_results['passed']
    failed = test_results['failed']
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"Total Tests: {total}")
    print(f"{GREEN}Passed: {passed}{RESET}")
    print(f"{RED}Failed: {failed}{RESET}")
    print(f"Success Rate: {percentage:.1f}%\n")
    
    if failed == 0:
        print(f"{GREEN}{'='*60}")
        print("🎉 ALL TESTS PASSED! 🎉")
        print(f"{'='*60}{RESET}\n")
    else:
        print(f"{YELLOW}{'='*60}")
        print(f"⚠️  {failed} TEST(S) FAILED")
        print(f"{'='*60}{RESET}\n")

def main():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}")
    print("MOVIE PLATFORM API - COMPREHENSIVE TEST SUITE")
    print(f"{'='*60}{RESET}\n")
    print(f"Testing API at: {BASE_URL}\n")
    
    try:
        test_health_check()
        test_admin_initialization()
        test_user_registration()
        test_user_login()
        test_get_current_user()
        test_movie_search()
        test_movie_fetch()
        test_movie_operations()
        test_profile_operations()
        test_playlist_operations()
        test_news_operations()
        test_chat_operations()
        test_contact_operations()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{RESET}\n")
    except Exception as e:
        print(f"\n{RED}Unexpected error: {e}{RESET}\n")
    finally:
        print_summary()

if __name__ == "__main__":
    main()
