import requests
from datetime import datetime
from config import Config

class NewsService:
    """Service for fetching entertainment news from external APIs"""
    
    def __init__(self, db):
        self.db = db
        self.news_collection = db[Config.DATABASE_NAME]['news']
        
        # Using NewsAPI.org (free tier: 100 requests/day)
        # You can get a free API key from https://newsapi.org/
        self.newsapi_key = '854b2e8293b54de1a12a4531162bcf15'
        self.newsapi_url = 'https://newsapi.org/v2/everything'
        
        # Fallback: Use mock news if API key not available
        self.use_mock = False  # Set to False when you have a real API key
    
    def fetch_entertainment_news(self, limit=20):
        """Fetch latest entertainment news"""
        if self.use_mock:
            return self._fetch_mock_news(limit)
        
        try:
            # Fetch from NewsAPI
            params = {
                'apiKey': self.newsapi_key,
                'q': 'movie OR cinema OR entertainment OR hollywood',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': limit
            }
            
            response = requests.get(self.newsapi_url, params=params, timeout=10)
            data = response.json()
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                return self._format_news_articles(articles)
            
            return []
            
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return self._fetch_mock_news(limit)
    
    def _format_news_articles(self, articles):
        """Format news articles from API response"""
        formatted = []
        
        for article in articles:
            formatted.append({
                'title': article.get('title', ''),
                'content': article.get('description', '') or article.get('content', ''),
                'author': article.get('author', 'Entertainment Desk'),
                'category': self._categorize_article(article.get('title', '')),
                'image_url': article.get('urlToImage', ''),
                'source_url': article.get('url', ''),
                'published_at': article.get('publishedAt', datetime.utcnow().isoformat()),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            })
        
        return formatted
    
    def _categorize_article(self, title):
        """Categorize article based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['movie', 'film', 'cinema', 'box office']):
            return 'Movies'
        elif any(word in title_lower for word in ['tv', 'series', 'show', 'episode']):
            return 'TV Series'
        elif any(word in title_lower for word in ['anime', 'manga', 'animation']):
            return 'Anime'
        elif any(word in title_lower for word in ['game', 'gaming', 'playstation', 'xbox']):
            return 'Gaming'
        else:
            return 'Entertainment'
    
    def _fetch_mock_news(self, limit=20):
        """Fetch mock news articles (fallback)"""
        mock_articles = [
            {
                'title': 'Marvel Studios Announces Phase 6 Lineup',
                'content': 'Marvel Studios has officially announced the complete lineup for Phase 6 of the MCU, featuring exciting new characters and storylines that will shape the future of the franchise.',
                'author': 'Entertainment Weekly',
                'category': 'Movies',
                'image_url': 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Christopher Nolan\'s Next Film Gets Release Date',
                'content': 'Warner Bros. has announced the release date for Christopher Nolan\'s highly anticipated next project, which promises to be another mind-bending cinematic experience.',
                'author': 'Variety',
                'category': 'Movies',
                'image_url': 'https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Studio Ghibli Announces New Animated Feature',
                'content': 'The legendary Studio Ghibli has revealed plans for a new animated feature film, marking their return to original storytelling after several years.',
                'author': 'Anime News Network',
                'category': 'Anime',
                'image_url': 'https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Box Office: Latest Blockbuster Breaks Records',
                'content': 'The latest superhero blockbuster has shattered box office records worldwide, becoming the highest-grossing film of the year in just two weeks.',
                'author': 'Box Office Mojo',
                'category': 'Movies',
                'image_url': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Streaming Wars: New Platform Launches',
                'content': 'A new streaming platform has entered the competitive market, promising exclusive content and competitive pricing to attract subscribers.',
                'author': 'The Hollywood Reporter',
                'category': 'TV Series',
                'image_url': 'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Oscar Nominations Announced',
                'content': 'The Academy has announced this year\'s Oscar nominations, with several surprise inclusions and notable snubs sparking conversation across the industry.',
                'author': 'Deadline',
                'category': 'Movies',
                'image_url': 'https://images.unsplash.com/photo-1485846234645-a62644f84728?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Popular Anime Series Gets Live-Action Adaptation',
                'content': 'A beloved anime series is being adapted into a live-action format, with production set to begin next year and a star-studded cast already confirmed.',
                'author': 'IGN',
                'category': 'Anime',
                'image_url': 'https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Director Wins Lifetime Achievement Award',
                'content': 'Legendary filmmaker receives prestigious lifetime achievement award, celebrating decades of groundbreaking work in cinema.',
                'author': 'IndieWire',
                'category': 'Movies',
                'image_url': 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Gaming Industry Sees Record Growth',
                'content': 'The gaming industry has reported record-breaking growth this year, with several blockbuster releases driving unprecedented engagement.',
                'author': 'GameSpot',
                'category': 'Gaming',
                'image_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Film Festival Announces Lineup',
                'content': 'Major international film festival reveals its official selection, featuring diverse voices and innovative storytelling from around the world.',
                'author': 'Screen Daily',
                'category': 'Movies',
                'image_url': 'https://images.unsplash.com/photo-1574267432644-f610f5b17752?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Sequel to Hit Movie Confirmed',
                'content': 'Studio confirms sequel to last year\'s surprise hit, with original cast and director returning for the highly anticipated follow-up.',
                'author': 'Collider',
                'category': 'Movies',
                'image_url': 'https://images.unsplash.com/photo-1594908900066-3f47337549d8?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            },
            {
                'title': 'Streaming Service Announces Original Series',
                'content': 'Major streaming platform unveils slate of original series, featuring high-profile creators and ambitious storytelling.',
                'author': 'TV Line',
                'category': 'TV Series',
                'image_url': 'https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=800',
                'source_url': '#',
                'published_at': datetime.utcnow().isoformat(),
                'created_at': datetime.utcnow(),
                'auto_fetched': True
            }
        ]
        
        return mock_articles[:limit]
    
    def seed_news(self):
        """Seed news articles into database"""
        print("📰 Fetching and seeding news articles...")
        
        try:
            # Fetch news articles
            articles = self.fetch_entertainment_news(limit=15)
            
            if not articles:
                print("❌ No articles fetched")
                return 0
            
            added = 0
            for article in articles:
                # Check if article already exists
                existing = self.news_collection.find_one({'title': article['title']})
                if not existing:
                    self.news_collection.insert_one(article)
                    print(f"   ✅ Added: {article['title'][:50]}...")
                    added += 1
            
            print(f"✅ Seeded {added} news articles")
            return added
            
        except Exception as e:
            print(f"❌ Error seeding news: {str(e)}")
            return 0
    
    def refresh_news(self):
        """Refresh news by removing old articles and fetching new ones"""
        print("🔄 Refreshing news articles...")
        
        try:
            # Remove auto-fetched articles older than 7 days
            from datetime import timedelta
            week_ago = datetime.utcnow() - timedelta(days=7)
            
            result = self.news_collection.delete_many({
                'auto_fetched': True,
                'created_at': {'$lt': week_ago}
            })
            
            print(f"   🗑️  Removed {result.deleted_count} old articles")
            
            # Fetch new articles
            added = self.seed_news()
            
            return {
                'removed': result.deleted_count,
                'added': added
            }
            
        except Exception as e:
            print(f"❌ Error refreshing news: {str(e)}")
            return {'removed': 0, 'added': 0}
    
    def get_news_status(self):
        """Get current news status"""
        total_news = self.news_collection.count_documents({})
        auto_fetched = self.news_collection.count_documents({'auto_fetched': True})
        
        return {
            'total_articles': total_news,
            'auto_fetched': auto_fetched,
            'manual': total_news - auto_fetched
        }
