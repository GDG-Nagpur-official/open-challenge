import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (username, email, password) => api.post('/auth/register', { username, email, password }),
  getCurrentUser: () => api.get('/auth/me'),
};

export const apisAPI = {
  // Added trailing slashes to all paths
  getAll: (page = 1, limit = 10) => api.get(`/apis/?page=${page}&limit=${limit}`),
  getOne: (id) => api.get(`/apis/${id}/`),
  create: (data) => api.post('/apis/', data),
  update: (id, data) => api.put(`/apis/${id}/`, data),
  delete: (id) => api.delete(`/apis/${id}/`),
};

export const keysAPI = {
  // Added trailing slashes to all paths
  getAll: () => api.get('/keys/'),
  create: (data) => api.post('/keys/', data),
  delete: (id) => api.delete(`/keys/${id}/`),
  toggle: (id) => api.patch(`/keys/${id}/toggle/`),
};

export const logsAPI = {
  // Added trailing slashes
  getAll: (page = 1, limit = 20) => api.get(`/logs/?page=${page}&limit=${limit}`),
  getStats: () => api.get('/logs/stats'),
};

export default api;