import axios, { InternalAxiosRequestConfig } from 'axios';

// 配置 axios 实例
const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
  },
  withCredentials: true
});

// 添加请求拦截器
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 确保每个请求都带有正确的头部
    if (config.headers) {
      config.headers['Content-Type'] = 'application/json';
      config.headers['Accept'] = 'application/json';
      config.headers['X-Requested-With'] = 'XMLHttpRequest';
    }
    
    console.log('Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      headers: config.headers,
      data: config.data
    });
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// 添加响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('Response:', response.status, response.config.url);
    console.log('Response data:', response.data);
    return response;
  },
  (error) => {
    console.error('Response error:', error.response || error);
    return Promise.reject(error);
  }
);

export interface LoginData {
    username: string;
    password: string;
}

export interface RegisterData extends LoginData {
    email: string;
}

export interface AuthResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export interface UserData {
    id: number;
    username: string;
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    created_at: string;
    updated_at: string | null;
}

const authService = {
    async login(data: LoginData): Promise<AuthResponse> {
        const response = await api.post('/auth/login', data);
        if (response.data.access_token) {
            this.setAuthToken(response.data.access_token);
        }
        return response.data;
    },

    async register(data: RegisterData): Promise<UserData> {
        const response = await api.post('/auth/register', data);
        return response.data;
    },

    async getCurrentUser(): Promise<UserData> {
        const response = await api.get('/auth/me');
        return response.data;
    },

    async refreshToken(): Promise<AuthResponse> {
        const response = await api.post('/auth/refresh');
        if (response.data.access_token) {
            this.setAuthToken(response.data.access_token);
        }
        return response.data;
    },

    setAuthToken(token: string) {
        if (token) {
            localStorage.setItem('token', token);
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        } else {
            localStorage.removeItem('token');
            delete api.defaults.headers.common['Authorization'];
        }
    },

    logout() {
        this.setAuthToken('');
    }
};

export default authService; 