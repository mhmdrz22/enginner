import axios from './axios';

export const authAPI = {
  register: (data) => axios.post('/accounts/register/', data),
  login: (data) => axios.post('/accounts/login/', data),
  getProfile: () => axios.get('/accounts/profile/'),
  updateProfile: (data) => axios.patch('/accounts/profile/', data),
};
