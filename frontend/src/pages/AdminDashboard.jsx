import React, { useState, useEffect } from 'react';
import { newsAPI, contactAPI, chatAPI, adminAPI } from '../services/api';

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    news: 0,
    contacts: 0,
    chats: 0,
    movies: 0
  });
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [seeding, setSeeding] = useState(false);
  const [seedingMessage, setSeedingMessage] = useState('');

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      setLoading(true);
      const [newsRes, contactsRes, chatsRes, dataStatus] = await Promise.all([
        newsAPI.getAll(),
        contactAPI.getAll(),
        chatAPI.getAll(),
        adminAPI.getDataStatus().catch(() => ({ data: { movies: { total_movies: 0 } } }))
      ]);

      setStats({
        news: newsRes.data.news?.length || 0,
        contacts: contactsRes.data.contacts?.length || 0,
        chats: chatsRes.data.chats?.length || 0,
        movies: dataStatus.data.movies?.total_movies || 0
      });
      setContacts(contactsRes.data.contacts || []);
    } catch (error) {
      console.error('Error fetching admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSeedAll = async () => {
    if (!confirm('This will populate the database with movies and news. Continue?')) return;
    
    try {
      setSeeding(true);
      setSeedingMessage('🎬 Seeding movies and news... This may take a minute...');
      
      const response = await adminAPI.seedAll('quick');
      
      setSeedingMessage(`✅ Success! Added ${response.data.movies.total_added} movies and ${response.data.news.articles_added} news articles`);
      
      // Refresh data
      setTimeout(() => {
        fetchAdminData();
        setSeedingMessage('');
        setSeeding(false);
      }, 3000);
      
    } catch (error) {
      setSeedingMessage('❌ Error seeding data: ' + error.message);
      setSeeding(false);
    }
  };

  const handleSeedMovies = async () => {
    if (!confirm('Seed movies into the database?')) return;
    
    try {
      setSeeding(true);
      setSeedingMessage('🎬 Seeding movies...');
      
      const response = await adminAPI.seedMovies('quick');
      
      setSeedingMessage(`✅ Added ${response.data.total_added} movies!`);
      
      setTimeout(() => {
        fetchAdminData();
        setSeedingMessage('');
        setSeeding(false);
      }, 2000);
      
    } catch (error) {
      setSeedingMessage('❌ Error: ' + error.message);
      setSeeding(false);
    }
  };

  const handleSeedNews = async () => {
    try {
      setSeeding(true);
      setSeedingMessage('📰 Fetching news...');
      
      const response = await adminAPI.seedNews();
      
      setSeedingMessage(`✅ Added ${response.data.articles_added} news articles!`);
      
      setTimeout(() => {
        fetchAdminData();
        setSeedingMessage('');
        setSeeding(false);
      }, 2000);
      
    } catch (error) {
      setSeedingMessage('❌ Error: ' + error.message);
      setSeeding(false);
    }
  };

  const handleRefreshNews = async () => {
    try {
      setSeeding(true);
      setSeedingMessage('🔄 Refreshing news...');
      
      const response = await adminAPI.refreshNews();
      
      setSeedingMessage(`✅ Removed ${response.data.removed} old articles, added ${response.data.added} new ones!`);
      
      setTimeout(() => {
        fetchAdminData();
        setSeedingMessage('');
        setSeeding(false);
      }, 2000);
      
    } catch (error) {
      setSeedingMessage('❌ Error: ' + error.message);
      setSeeding(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-page">
      <div className="container">
        <div className="page-header">
          <h1 className="page-title">👑 Admin Dashboard</h1>
          <p className="page-subtitle">Manage your movie platform</p>
        </div>

        <div className="admin-stats">
          <div className="stat-card">
            <div className="stat-icon">🎬</div>
            <div className="stat-info">
              <div className="stat-value">{stats.movies}</div>
              <div className="stat-label">Movies</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📰</div>
            <div className="stat-info">
              <div className="stat-value">{stats.news}</div>
              <div className="stat-label">News Articles</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">📧</div>
            <div className="stat-info">
              <div className="stat-value">{stats.contacts}</div>
              <div className="stat-label">Contact Messages</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">💬</div>
            <div className="stat-info">
              <div className="stat-value">{stats.chats}</div>
              <div className="stat-label">Active Chats</div>
            </div>
          </div>
        </div>

        {seedingMessage && (
          <div className="card" style={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            padding: '20px',
            textAlign: 'center',
            marginBottom: '20px'
          }}>
            <h3>{seedingMessage}</h3>
          </div>
        )}

        <div className="admin-section">
          <h2 className="section-title">🚀 Data Management</h2>
          <div className="action-buttons">
            <button 
              className="btn btn-primary" 
              onClick={handleSeedAll}
              disabled={seeding}
            >
              {seeding ? '⏳ Processing...' : '🎬 Seed All Data (Quick)'}
            </button>
            <button 
              className="btn btn-primary" 
              onClick={handleSeedMovies}
              disabled={seeding}
            >
              🎥 Seed Movies Only
            </button>
            <button 
              className="btn btn-primary" 
              onClick={handleSeedNews}
              disabled={seeding}
            >
              📰 Seed News
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={handleRefreshNews}
              disabled={seeding}
            >
              🔄 Refresh News
            </button>
          </div>
          <p style={{ marginTop: '15px', color: '#888', fontSize: '14px' }}>
            💡 Tip: Use "Seed All Data" to quickly populate your database with movies and news articles
          </p>
        </div>

        <div className="admin-section">
          <h2 className="section-title">Recent Contact Messages</h2>
          {contacts.length > 0 ? (
            <div className="contacts-list">
              {contacts.slice(0, 5).map((contact) => (
                <div key={contact._id} className="contact-item card">
                  <div className="contact-header">
                    <h3>{contact.name}</h3>
                    <span className="contact-date">
                      {new Date(contact.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="contact-email">{contact.email}</p>
                  <p className="contact-subject"><strong>{contact.subject}</strong></p>
                  <p className="contact-message">{contact.message}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No contact messages yet</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
