import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
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
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/api/auth/refresh`, {}, {
          headers: {
            Authorization: `Bearer ${refreshToken}`,
          },
        });

        const { access_token } = response.data;
        localStorage.setItem('access_token', access_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  getCurrentUser: () => api.get('/api/auth/me'),
};

export const apisAPI = {
  getAll: (page = 1, limit = 10) => api.get(`/api/apis?page=${page}&limit=${limit}`),
  getOne: (id) => api.get(`/api/apis/${id}`),
  create: (data) => api.post('/api/apis', data),
  update: (id, data) => api.put(`/api/apis/${id}`, data),
  delete: (id) => api.delete(`/api/apis/${id}`),
};

export const keysAPI = {
  getAll: () => api.get('/api/keys'),
  create: (data) => api.post('/api/keys', data),
  delete: (id) => api.delete(`/api/keys/${id}`),
  toggle: (id) => api.patch(`/api/keys/${id}/toggle`),
};

export const logsAPI = {
  getAll: (page = 1, limit = 20, apiId = null) => {
    let url = `/api/logs?page=${page}&limit=${limit}`;
    if (apiId) url += `&api_id=${apiId}`;
    return api.get(url);
  },
  getStats: () => api.get('/api/logs/stats'),
};

export default api;
