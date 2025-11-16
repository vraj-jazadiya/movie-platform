import React from 'react';

const MovieCard = ({ movie, onAddToPlaylist, onAddToFavorites }) => {
  const posterUrl = movie.poster && movie.poster !== 'N/A' 
    ? movie.poster 
    : 'https://via.placeholder.com/300x450?text=No+Poster';

  return (
    <div className="movie-card">
      <div className="movie-poster">
        <img src={posterUrl} alt={movie.title} />
        <div className="movie-overlay">
          <div className="movie-actions">
            {onAddToFavorites && (
              <button 
                className="btn btn-icon" 
                onClick={() => onAddToFavorites(movie)}
                title="Add to Favorites"
              >
                ❤️
              </button>
            )}
            {onAddToPlaylist && (
              <button 
                className="btn btn-icon" 
                onClick={() => onAddToPlaylist(movie)}
                title="Add to Playlist"
              >
                ➕
              </button>
            )}
          </div>
        </div>
      </div>
      <div className="movie-info">
        <h3 className="movie-title">{movie.title}</h3>
        <div className="movie-meta">
          <span className="movie-year">{movie.year}</span>
          {movie.imdb_rating && (
            <span className="movie-rating">
              ⭐ {movie.imdb_rating}
            </span>
          )}
        </div>
        {movie.genre && (
          <p className="movie-genre">{movie.genre}</p>
        )}
      </div>
    </div>
  );
};

export default MovieCard;
