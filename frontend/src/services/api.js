import axios from 'axios';

// Use environment variable for production, fallback to production URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://movie-platform-api.onrender.com';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {}, {
          headers: { Authorization: `Bearer ${refreshToken}` },
        });
        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
  initAdmin: () => api.post('/auth/init-admin'),
};

export const moviesAPI = {
  search: (query, year, page = 1) => api.get('/movies/search', { params: { q: query, year, page } }),
  fetchByImdbId: (imdbId) => api.get(`/movies/fetch/${imdbId}`),
  getById: (movieId) => api.get(`/movies/${movieId}`),
  getByProductionHouse: (house, skip = 0, limit = 20) => api.get(`/movies/production-house/${house}`, { params: { skip, limit } }),
  getTrending: (limit = 10) => api.get('/movies/trending', { params: { limit } }),
  getTopRated: (limit = 10) => api.get('/movies/top-rated', { params: { limit } }),
  filter: (filters) => api.post('/movies/filter', filters),
  getProductionHouses: () => api.get('/movies/production-houses'),
};

export const profileAPI = {
  getProfile: () => api.get('/profile/'),
  updateProfile: (data) => api.put('/profile/update', data),
  addToFavorites: (movieId) => api.post(`/profile/favorites/${movieId}`),
  removeFromFavorites: (movieId) => api.delete(`/profile/favorites/${movieId}`),
};

export const playlistsAPI = {
  create: (data) => api.post('/playlists/', data),
  getById: (id) => api.get(`/playlists/${id}`),
  update: (id, data) => api.put(`/playlists/${id}`, data),
  delete: (id) => api.delete(`/playlists/${id}`),
  addMovie: (id, movie) => api.post(`/playlists/${id}/movies`, movie),
  removeMovie: (id, movieId) => api.delete(`/playlists/${id}/movies/${movieId}`),
};

export const newsAPI = {
  getAll: (skip = 0, limit = 20) => api.get('/news/', { params: { skip, limit } }),
  getById: (id) => api.get(`/news/${id}`),
  getLatest: (limit = 5) => api.get('/news/latest', { params: { limit } }),
  create: (data) => api.post('/news/', data),
  update: (id, data) => api.put(`/news/${id}`, data),
  delete: (id) => api.delete(`/news/${id}`),
};

export const chatAPI = {
  getMyChat: () => api.get('/chat/my-chat'),
  sendMessage: (chatId, message) => api.post(`/chat/${chatId}/message`, { message }),
  getAll: () => api.get('/chat/all'),
};

export const contactAPI = {
  submit: (data) => api.post('/contact/', data),
  getAll: () => api.get('/contact/all'),
};

export const adminAPI = {
  seedMovies: (type = 'quick') => api.post('/admin/seed-movies', { type }),
  seedNews: () => api.post('/admin/seed-news'),
  refreshNews: () => api.post('/admin/refresh-news'),
  seedAll: (type = 'quick') => api.post('/admin/seed-all', { type }),
  getDataStatus: () => api.get('/admin/data-status'),
  clearMovies: () => api.delete('/admin/clear-movies'),
  clearNews: () => api.delete('/admin/clear-news'),
};

export default api;
