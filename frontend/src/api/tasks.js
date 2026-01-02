import axios from './axios';

export const tasksAPI = {
  getTasks: (params) => axios.get('/tasks/', { params }),
  getTask: (id) => axios.get(`/tasks/${id}/`),
  createTask: (data) => axios.post('/tasks/', data),
  updateTask: (id, data) => axios.patch(`/tasks/${id}/`, data),
  deleteTask: (id) => axios.delete(`/tasks/${id}/`),
};
