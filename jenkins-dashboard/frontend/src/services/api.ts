import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // Proxied by Vite/Nginx
  headers: {
    'Content-Type': 'application/json',
  },
});

// Example function
export const getHealth = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};

// Add more functions to fetch data for builds, analytics etc.

export default apiClient;
