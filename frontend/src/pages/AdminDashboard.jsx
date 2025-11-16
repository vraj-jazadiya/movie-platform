import React, { useState, useEffect } from 'react';
import { newsAPI, contactAPI, chatAPI } from '../services/api';

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    news: 0,
    contacts: 0,
    chats: 0
  });
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      setLoading(true);
      const [newsRes, contactsRes, chatsRes] = await Promise.all([
        newsAPI.getAll(),
        contactAPI.getAll(),
        chatAPI.getAll()
      ]);

      setStats({
        news: newsRes.data.news?.length || 0,
        contacts: contactsRes.data.contacts?.length || 0,
        chats: chatsRes.data.chats?.length || 0
      });
      setContacts(contactsRes.data.contacts || []);
    } catch (error) {
      console.error('Error fetching admin data:', error);
    } finally {
      setLoading(false);
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

        <div className="admin-section">
          <h2 className="section-title">Quick Actions</h2>
          <div className="action-buttons">
            <button className="btn btn-primary">Create News Article</button>
            <button className="btn btn-primary">Manage Users</button>
            <button className="btn btn-primary">View All Chats</button>
            <button className="btn btn-primary">Manage Movies</button>
          </div>
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
