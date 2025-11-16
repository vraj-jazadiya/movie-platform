import React, { useState, useEffect } from 'react';
import { newsAPI } from '../services/api';

const News = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    try {
      setLoading(true);
      const response = await newsAPI.getAll();
      setNews(response.data.news || []);
    } catch (error) {
      console.error('Error fetching news:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading news...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="news-page">
      <div className="container">
        <div className="page-header">
          <h1 className="page-title">Latest Entertainment News</h1>
          <p className="page-subtitle">Stay updated with the latest from the world of movies and entertainment</p>
        </div>

        {news.length > 0 ? (
          <div className="news-grid">
            {news.map((article) => (
              <div key={article._id} className="news-card">
                {article.image_url && (
                  <div className="news-image">
                    <img src={article.image_url} alt={article.title} />
                  </div>
                )}
                <div className="news-content">
                  <div className="news-category">{article.category}</div>
                  <h2 className="news-title">{article.title}</h2>
                  <p className="news-excerpt">{article.content.substring(0, 150)}...</p>
                  <div className="news-meta">
                    <span className="news-author">By {article.author}</span>
                    <span className="news-date">
                      {new Date(article.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <button className="btn btn-secondary">Read More</button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-icon">📰</div>
            <h3>No news articles yet</h3>
            <p>Check back soon for the latest entertainment news!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default News;
