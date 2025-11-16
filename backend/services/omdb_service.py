import requests
from config import Config

class OMDbService:
    """Service for interacting with OMDb API"""
    
    def __init__(self):
        self.api_key = Config.OMDB_API_KEY
        self.base_url = Config.OMDB_API_URL
    
    def fetch_movie_by_imdb_id(self, imdb_id):
        """Fetch movie details by IMDb ID"""
        try:
            params = {
                'apikey': self.api_key,
                'i': imdb_id,
                'plot': 'full'
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if data.get('Response') == 'True':
                return self._format_movie_data(data)
            
            return None
        except Exception as e:
            print(f"Error fetching movie: {str(e)}")
            return None
    
    def search_movies(self, title, year=None, page=1):
        """Search movies by title"""
        try:
            params = {
                'apikey': self.api_key,
                's': title,
                'page': page
            }
            
            if year:
                params['y'] = year
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if data.get('Response') == 'True':
                return {
                    'results': data.get('Search', []),
                    'total_results': data.get('totalResults', 0)
                }
            
            return {'results': [], 'total_results': 0}
        except Exception as e:
            print(f"Error searching movies: {str(e)}")
            return {'results': [], 'total_results': 0}
    
    def fetch_movie_by_title(self, title, year=None):
        """Fetch movie details by title"""
        try:
            params = {
                'apikey': self.api_key,
                't': title,
                'plot': 'full'
            }
            
            if year:
                params['y'] = year
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if data.get('Response') == 'True':
                return self._format_movie_data(data)
            
            return None
        except Exception as e:
            print(f"Error fetching movie: {str(e)}")
            return None
    
    def _format_movie_data(self, data):
        """Format OMDb API response to our movie model"""
        return {
            'imdb_id': data.get('imdbID'),
            'title': data.get('Title'),
            'year': data.get('Year'),
            'rated': data.get('Rated'),
            'released': data.get('Released'),
            'runtime': data.get('Runtime'),
            'genre': data.get('Genre'),
            'director': data.get('Director'),
            'writer': data.get('Writer'),
            'actors': data.get('Actors'),
            'plot': data.get('Plot'),
            'language': data.get('Language'),
            'country': data.get('Country'),
            'awards': data.get('Awards'),
            'poster': data.get('Poster'),
            'ratings': self._format_ratings(data.get('Ratings', [])),
            'metascore': data.get('Metascore'),
            'imdb_rating': data.get('imdbRating'),
            'imdb_votes': data.get('imdbVotes'),
            'type': data.get('Type'),
            'dvd': data.get('DVD'),
            'box_office': data.get('BoxOffice'),
            'production': data.get('Production'),
            'website': data.get('Website'),
            'production_house': self._extract_production_house(data)
        }
    
    def _format_ratings(self, ratings):
        """Format ratings from OMDb"""
        formatted = []
        for rating in ratings:
            formatted.append({
                'source': rating.get('Source'),
                'value': rating.get('Value')
            })
        return formatted
    
    def _extract_production_house(self, data):
        """Extract production house from movie data"""
        production = data.get('Production', '')
        
        # Check against our list of production houses
        for house in Config.PRODUCTION_HOUSES:
            if house.lower() in production.lower():
                return house
        
        return production if production != 'N/A' else ''
    
    def fetch_movies_by_production_house(self, production_house, page=1):
        """Fetch movies by production house (limited by OMDb API)"""
        # Note: OMDb doesn't directly support production house search
        # This is a workaround using search
        try:
            params = {
                'apikey': self.api_key,
                's': production_house,
                'page': page
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if data.get('Response') == 'True':
                movies = []
                for movie in data.get('Search', []):
                    # Fetch full details for each movie
                    full_data = self.fetch_movie_by_imdb_id(movie.get('imdbID'))
                    if full_data and production_house.lower() in full_data.get('production_house', '').lower():
                        movies.append(full_data)
                
                return movies
            
            return []
        except Exception as e:
            print(f"Error fetching movies by production house: {str(e)}")
            return []
