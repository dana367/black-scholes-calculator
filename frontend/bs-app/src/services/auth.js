import api from '../api';

export const authService = {
  async login(credentials) {
    try {
      const formData = new URLSearchParams();
      formData.append('username', credentials.username);
      formData.append('password', credentials.password);

      const response = await api.post('/auth/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
       
        const userResponse = await this.getCurrentUser();
        return {
          ...response.data,
          user: userResponse.data.User 
        };
      }
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  async register(credentials) {
    try {
      const response = await api.post('/auth', {
        username: credentials.username,
        password: credentials.password
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  logout() {
    localStorage.removeItem('token');
  },

  getCurrentUser() {
    const token = localStorage.getItem('token');
    return token ? api.get('/') : null;
  }
};
