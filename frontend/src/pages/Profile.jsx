import React, { useState, useEffect, useContext } from 'react';
import { profileAPI, playlistsAPI } from '../services/api';
import { AuthContext } from '../App';

const Profile = () => {
  const { user } = useContext(AuthContext);
  const [profile, setProfile] = useState(null);
  const [playlists, setPlaylists] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    bio: ''
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await profileAPI.getProfile();
      setProfile(response.data);
      setPlaylists(response.data.playlists || []);
      setFormData({
        name: response.data.name || '',
        bio: response.data.bio || ''
      });
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await profileAPI.updateProfile(formData);
      setProfile({ ...profile, ...formData });
      setEditing(false);
    } catch (error) {
      console.error('Error updating profile:', error);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="container">
        <div className="profile-header">
          <div className="profile-avatar">
            <div className="avatar-circle">
              {profile?.name?.charAt(0) || user?.username?.charAt(0) || '?'}
            </div>
          </div>
          <div className="profile-info">
            <h1 className="profile-name">{profile?.name || user?.username}</h1>
            <p className="profile-username">@{user?.username}</p>
            <p className="profile-role">{user?.role === 'admin' ? '👑 Admin' : '🎬 Movie Enthusiast'}</p>
          </div>
          <button 
            className="btn btn-primary"
            onClick={() => setEditing(!editing)}
          >
            {editing ? 'Cancel' : 'Edit Profile'}
          </button>
        </div>

        {editing && (
          <div className="card">
            <h2 className="card-title">Edit Profile</h2>
            <form onSubmit={handleUpdate} className="profile-form">
              <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  placeholder="Your name"
                />
              </div>
              <div className="form-group">
                <label htmlFor="bio">Bio</label>
                <textarea
                  id="bio"
                  name="bio"
                  value={formData.bio}
                  onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                  placeholder="Tell us about yourself..."
                  rows="4"
                />
              </div>
              <button type="submit" className="btn btn-primary">
                Save Changes
              </button>
            </form>
          </div>
        )}

        {profile?.bio && !editing && (
          <div className="card">
            <h2 className="card-title">About</h2>
            <p>{profile.bio}</p>
          </div>
        )}

        <div className="profile-stats">
          <div className="stat-card">
            <div className="stat-value">{playlists.length}</div>
            <div className="stat-label">Playlists</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{profile?.favorites?.length || 0}</div>
            <div className="stat-label">Favorites</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{profile?.watchlist?.length || 0}</div>
            <div className="stat-label">Watchlist</div>
          </div>
        </div>

        <div className="profile-section">
          <div className="section-header">
            <h2 className="section-title">My Playlists</h2>
            <button className="btn btn-primary">Create Playlist</button>
          </div>
          
          {playlists.length > 0 ? (
            <div className="playlists-grid">
              {playlists.map((playlist, index) => (
                <div key={index} className="playlist-card">
                  <h3 className="playlist-name">{playlist.name}</h3>
                  <p className="playlist-description">{playlist.description}</p>
                  <div className="playlist-meta">
                    <span>{playlist.movies?.length || 0} movies</span>
                    <span>{playlist.is_public ? '🌐 Public' : '🔒 Private'}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <p>No playlists yet. Create your first playlist!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;
