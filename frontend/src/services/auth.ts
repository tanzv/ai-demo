import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const login = async (data: { username: string; password: string }): Promise<LoginResponse> => {
  const formData = new FormData();
  formData.append('username', data.username);
  formData.append('password', data.password);
  
  const response = await axios.post(`${API_URL}/auth/login/access-token`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const getCurrentUser = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No token found');
  }

  const response = await axios.get(`${API_URL}/users/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return response.data;
}; 