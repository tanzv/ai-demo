import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

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
        const response = await axios.post(`${API_URL}/auth/login`, data, {
            withCredentials: true
        });
        return response.data;
    },

    async register(data: RegisterData): Promise<UserData> {
        const response = await axios.post(`${API_URL}/auth/register`, data);
        return response.data;
    },

    async getCurrentUser(): Promise<UserData> {
        const response = await axios.get(`${API_URL}/auth/me`, {
            withCredentials: true
        });
        return response.data;
    },

    async refreshToken(): Promise<AuthResponse> {
        const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
            withCredentials: true
        });
        return response.data;
    },

    setAuthToken(token: string) {
        if (token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        } else {
            delete axios.defaults.headers.common['Authorization'];
        }
    },

    logout() {
        this.setAuthToken('');
        localStorage.removeItem('token');
    }
};

export default authService; 