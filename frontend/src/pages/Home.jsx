import React, { useState, useEffect } from 'react';
import { moviesAPI } from '../services/api';
import MovieCard from '../components/MovieCard';

const Home = () => {
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [topRatedMovies, setTopRatedMovies] = useState([]);
  const [productionHouses, setProductionHouses] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);

  useEffect(() => {
    fetchHomeData();
  }, []);

  const fetchHomeData = async () => {
    try {
      setLoading(true);
      const [trending, topRated, houses] = await Promise.all([
        moviesAPI.getTrending(10),
        moviesAPI.getTopRated(10),
        moviesAPI.getProductionHouses()
      ]);
      
      setTrendingMovies(trending.data.movies || []);
      setTopRatedMovies(topRated.data.movies || []);
      setProductionHouses(houses.data.production_houses || []);
    } catch (error) {
      console.error('Error fetching home data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    try {
      setSearching(true);
      const response = await moviesAPI.search(searchQuery);
      setSearchResults(response.data.movies || []);
    } catch (error) {
      console.error('Error searching movies:', error);
    } finally {
      setSearching(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading amazing movies...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="container">
          <div className="hero-content">
            <h1 className="hero-title">
              Discover Your Next
              <span className="gradient-text"> Favorite Movie</span>
            </h1>
            <p className="hero-subtitle">
              Explore thousands of movies from 37+ production houses worldwide
            </p>
            
            {/* Search Bar */}
            <form onSubmit={handleSearch} className="search-form">
              <input
                type="text"
                placeholder="Search for movies, series, anime..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
              />
              <button type="submit" className="btn btn-primary" disabled={searching}>
                {searching ? 'Searching...' : '🔍 Search'}
              </button>
            </form>
          </div>
        </div>
      </section>

      <div className="container">
        {/* Search Results */}
        {searchResults.length > 0 && (
          <section className="movie-section">
            <div className="section-header">
              <h2 className="section-title">Search Results</h2>
              <button 
                className="btn btn-secondary"
                onClick={() => {
                  setSearchResults([]);
                  setSearchQuery('');
                }}
              >
                Clear
              </button>
            </div>
            <div className="movie-grid">
              {searchResults.map((movie, index) => (
                <MovieCard key={index} movie={movie} />
              ))}
            </div>
          </section>
        )}

        {/* Trending Movies */}
        {trendingMovies.length > 0 && (
          <section className="movie-section">
            <div className="section-header">
              <h2 className="section-title">🔥 Trending Now</h2>
            </div>
            <div className="movie-grid">
              {trendingMovies.map((movie, index) => (
                <MovieCard key={index} movie={movie} />
              ))}
            </div>
          </section>
        )}

        {/* Top Rated Movies */}
        {topRatedMovies.length > 0 && (
          <section className="movie-section">
            <div className="section-header">
              <h2 className="section-title">⭐ Top Rated</h2>
            </div>
            <div className="movie-grid">
              {topRatedMovies.map((movie, index) => (
                <MovieCard key={index} movie={movie} />
              ))}
            </div>
          </section>
        )}

        {/* Production Houses */}
        <section className="movie-section">
          <div className="section-header">
            <h2 className="section-title">🎬 Browse by Studio</h2>
          </div>
          <div className="production-houses-grid">
            {productionHouses.map((house, index) => (
              <div key={index} className="production-house-card">
                <div className="production-house-icon">🎥</div>
                <h3 className="production-house-name">{house}</h3>
                <button className="btn btn-sm btn-primary">
                  Explore Movies
                </button>
              </div>
            ))}
          </div>
        </section>

        {/* Features Section */}
        <section className="features-section">
          <h2 className="section-title text-center">Why Choose MoviePlatform?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🎬</div>
              <h3>37+ Studios</h3>
              <p>Access movies from major studios and anime producers worldwide</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📝</div>
              <h3>Custom Playlists</h3>
              <p>Create and organize your favorite movies in personalized playlists</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⭐</div>
              <h3>Rate & Review</h3>
              <p>Share your opinions and discover what others think</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📰</div>
              <h3>Latest News</h3>
              <p>Stay updated with entertainment news and releases</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Home;
