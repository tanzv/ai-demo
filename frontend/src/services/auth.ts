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
        const response = await axios.post(`${API_URL}/auth/login`, data);
        if (response.data.access_token) {
            this.setAuthToken(response.data.access_token);
        }
        return response.data;
    },

    async register(data: RegisterData): Promise<UserData> {
        const response = await axios.post(`${API_URL}/auth/register`, data);
        return response.data;
    },

    async getCurrentUser(): Promise<UserData> {
        const response = await axios.get(`${API_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        return response.data;
    },

    async refreshToken(): Promise<AuthResponse> {
        const response = await axios.post(`${API_URL}/auth/refresh`, {}, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });
        if (response.data.access_token) {
            this.setAuthToken(response.data.access_token);
        }
        return response.data;
    },

    setAuthToken(token: string) {
        if (token) {
            localStorage.setItem('token', token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        } else {
            localStorage.removeItem('token');
            delete axios.defaults.headers.common['Authorization'];
        }
    },

    logout() {
        this.setAuthToken('');
    }
};

export default authService; 