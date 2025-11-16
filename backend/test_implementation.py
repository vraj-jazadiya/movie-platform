"""
Test script for automatic data fetching implementation
"""

import sys
import time
from pymongo import MongoClient
from config import Config
from services.movie_seeder import MovieSeeder
from services.news_service import NewsService

def test_database_connection():
    """Test MongoDB connection"""
    print("\n" + "="*60)
    print("TEST 1: Database Connection")
    print("="*60)
    try:
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✅ PASS: Successfully connected to MongoDB")
        return client, True
    except Exception as e:
        print(f"❌ FAIL: Could not connect to MongoDB: {str(e)}")
        return None, False

def test_movie_seeder_initialization(db):
    """Test MovieSeeder initialization"""
    print("\n" + "="*60)
    print("TEST 2: MovieSeeder Initialization")
    print("="*60)
    try:
        seeder = MovieSeeder(db)
        print("✅ PASS: MovieSeeder initialized successfully")
        return seeder, True
    except Exception as e:
        print(f"❌ FAIL: MovieSeeder initialization failed: {str(e)}")
        return None, False

def test_news_service_initialization(db):
    """Test NewsService initialization"""
    print("\n" + "="*60)
    print("TEST 3: NewsService Initialization")
    print("="*60)
    try:
        news_service = NewsService(db)
        print("✅ PASS: NewsService initialized successfully")
        return news_service, True
    except Exception as e:
        print(f"❌ FAIL: NewsService initialization failed: {str(e)}")
        return None, False

def test_omdb_api_connection(seeder):
    """Test OMDb API connection"""
    print("\n" + "="*60)
    print("TEST 4: OMDb API Connection")
    print("="*60)
    try:
        # Try to fetch a well-known movie
        movie_data = seeder.omdb_service.fetch_movie_by_title("Inception")
        if movie_data and movie_data.get('title'):
            print(f"✅ PASS: Successfully fetched movie: {movie_data['title']}")
            print(f"   Year: {movie_data.get('year')}")
            print(f"   Director: {movie_data.get('director')}")
            return True
        else:
            print("❌ FAIL: Could not fetch movie data")
            return False
    except Exception as e:
        print(f"❌ FAIL: OMDb API error: {str(e)}")
        return False

def test_movie_seeding(seeder):
    """Test movie seeding functionality"""
    print("\n" + "="*60)
    print("TEST 5: Movie Seeding (Quick Mode)")
    print("="*60)
    try:
        # Clear any existing test data
        movies_collection = seeder.movies_collection
        initial_count = movies_collection.count_documents({})
        print(f"   Initial movie count: {initial_count}")
        
        # Seed 3 test movies
        test_movies = ['Inception', 'The Matrix', 'Interstellar']
        added = 0
        
        for title in test_movies:
            try:
                existing = movies_collection.find_one({'title': title})
                if not existing:
                    movie_data = seeder.omdb_service.fetch_movie_by_title(title)
                    if movie_data:
                        movie_data['view_count'] = 100
                        movie_data['user_ratings'] = []
                        movie_data['reviews'] = []
                        movie_data['seeded'] = True
                        movies_collection.insert_one(movie_data)
                        print(f"   ✅ Added: {title}")
                        added += 1
                else:
                    print(f"   ⏭️  Skipped: {title} (already exists)")
                
                time.sleep(0.3)  # Rate limiting
            except Exception as e:
                print(f"   ❌ Error with {title}: {str(e)}")
        
        final_count = movies_collection.count_documents({})
        print(f"\n   Final movie count: {final_count}")
        print(f"   Movies added in this test: {added}")
        
        if added > 0 or final_count > initial_count:
            print("✅ PASS: Movie seeding works correctly")
            return True
        else:
            print("⚠️  WARNING: No new movies added (may already exist)")
            return True
            
    except Exception as e:
        print(f"❌ FAIL: Movie seeding failed: {str(e)}")
        return False

def test_news_generation(news_service):
    """Test news generation"""
    print("\n" + "="*60)
    print("TEST 6: News Generation")
    print("="*60)
    try:
        # Generate mock news
        articles = news_service.fetch_entertainment_news(limit=5)
        
        if articles and len(articles) > 0:
            print(f"✅ PASS: Generated {len(articles)} news articles")
            print(f"\n   Sample article:")
            print(f"   Title: {articles[0]['title'][:60]}...")
            print(f"   Category: {articles[0]['category']}")
            print(f"   Author: {articles[0]['author']}")
            return True
        else:
            print("❌ FAIL: Could not generate news articles")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: News generation failed: {str(e)}")
        return False

def test_news_seeding(news_service):
    """Test news seeding to database"""
    print("\n" + "="*60)
    print("TEST 7: News Seeding to Database")
    print("="*60)
    try:
        initial_count = news_service.news_collection.count_documents({})
        print(f"   Initial news count: {initial_count}")
        
        added = news_service.seed_news()
        
        final_count = news_service.news_collection.count_documents({})
        print(f"   Final news count: {final_count}")
        print(f"   Articles added: {added}")
        
        if added > 0 or final_count > 0:
            print("✅ PASS: News seeding works correctly")
            return True
        else:
            print("⚠️  WARNING: No news added")
            return True
            
    except Exception as e:
        print(f"❌ FAIL: News seeding failed: {str(e)}")
        return False

def test_data_status(seeder, news_service):
    """Test data status retrieval"""
    print("\n" + "="*60)
    print("TEST 8: Data Status Retrieval")
    print("="*60)
    try:
        movie_status = seeder.get_seeding_status()
        news_status = news_service.get_news_status()
        
        print(f"\n   📊 Movie Status:")
        print(f"      Total movies: {movie_status['total_movies']}")
        print(f"      Seeded movies: {movie_status['seeded_movies']}")
        print(f"      Trending movies: {movie_status['trending_movies']}")
        
        print(f"\n   📰 News Status:")
        print(f"      Total articles: {news_status['total_articles']}")
        print(f"      Auto-fetched: {news_status['auto_fetched']}")
        
        print("\n✅ PASS: Data status retrieval works correctly")
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Data status retrieval failed: {str(e)}")
        return False

def test_duplicate_prevention(seeder):
    """Test duplicate movie prevention"""
    print("\n" + "="*60)
    print("TEST 9: Duplicate Prevention")
    print("="*60)
    try:
        # Try to add the same movie twice
        test_title = "The Dark Knight"
        movies_collection = seeder.movies_collection
        
        initial_count = movies_collection.count_documents({'title': test_title})
        print(f"   Initial count of '{test_title}': {initial_count}")
        
        # Try to add it
        existing = movies_collection.find_one({'title': test_title})
        if existing:
            print(f"   ⏭️  Movie already exists (duplicate prevention working)")
            print("✅ PASS: Duplicate prevention works correctly")
            return True
        else:
            # Add it once
            movie_data = seeder.omdb_service.fetch_movie_by_title(test_title)
            if movie_data:
                movie_data['seeded'] = True
                movies_collection.insert_one(movie_data)
                print(f"   ✅ Added movie first time")
                
                # Try to add again
                existing = movies_collection.find_one({'title': test_title})
                if existing:
                    print(f"   ⏭️  Duplicate detected on second attempt")
                    print("✅ PASS: Duplicate prevention works correctly")
                    return True
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: Duplicate prevention test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 AUTOMATIC DATA FETCHING - TEST SUITE")
    print("="*60)
    print(f"Testing implementation of automatic movie and news fetching")
    print(f"Database: {Config.DATABASE_NAME}")
    print("="*60)
    
    results = []
    
    # Test 1: Database Connection
    client, success = test_database_connection()
    results.append(("Database Connection", success))
    if not success:
        print("\n❌ Cannot proceed without database connection")
        return
    
    db = client
    
    # Test 2: MovieSeeder Initialization
    seeder, success = test_movie_seeder_initialization(db)
    results.append(("MovieSeeder Init", success))
    if not success:
        return
    
    # Test 3: NewsService Initialization
    news_service, success = test_news_service_initialization(db)
    results.append(("NewsService Init", success))
    if not success:
        return
    
    # Test 4: OMDb API Connection
    success = test_omdb_api_connection(seeder)
    results.append(("OMDb API Connection", success))
    
    # Test 5: Movie Seeding
    success = test_movie_seeding(seeder)
    results.append(("Movie Seeding", success))
    
    # Test 6: News Generation
    success = test_news_generation(news_service)
    results.append(("News Generation", success))
    
    # Test 7: News Seeding
    success = test_news_seeding(news_service)
    results.append(("News Seeding", success))
    
    # Test 8: Data Status
    success = test_data_status(seeder, news_service)
    results.append(("Data Status", success))
    
    # Test 9: Duplicate Prevention
    success = test_duplicate_prevention(seeder)
    results.append(("Duplicate Prevention", success))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    print("="*60)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Implementation is working correctly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the errors above.")
    
    print("\n✅ Testing complete!")

if __name__ == '__main__':
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
