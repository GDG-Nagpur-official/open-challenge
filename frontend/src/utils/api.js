import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Single-flight refresh to prevent multiple 401s from triggering a refresh storm.
let refreshPromise = null;

const clearAuthAndRedirectToLogin = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  // Replace (not push) so back button doesn't return to protected pages.
  window.location.replace('/login');
};

const refreshAccessToken = async () => {
  if (refreshPromise) return refreshPromise;

  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) {
    return Promise.reject(new Error('No refresh token available'));
  }

  refreshPromise = axios
    .post(
      `${API_URL}/api/auth/refresh`,
      {},
      {
        headers: {
          Authorization: `Bearer ${refreshToken}`,
        },
      }
    )
    .then((response) => {
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      return access_token;
    })
    .catch((err) => {
      clearAuthAndRedirectToLogin();
      throw err;
    })
    .finally(() => {
      refreshPromise = null;
    });

  return refreshPromise;
};

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

    // If there's no config, we can't safely retry.
    if (!originalRequest) return Promise.reject(error);

    const status = error.response?.status;
    const url = originalRequest.url || '';

    // Never try to refresh for auth routes. Prevents accidental loops.
    const isAuthRoute = url.includes('/api/auth/login') ||
      url.includes('/api/auth/register') ||
      url.includes('/api/auth/refresh');

    if (status === 401 && !originalRequest._retry && !isAuthRoute) {
      originalRequest._retry = true;

      try {
        const accessToken = await refreshAccessToken();

        originalRequest.headers = originalRequest.headers || {};
        originalRequest.headers.Authorization = `Bearer ${accessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // refreshAccessToken already cleared auth + redirected.
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
