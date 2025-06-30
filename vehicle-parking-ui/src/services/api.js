import axios from 'axios'

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Authentication API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
  getProfile: () => api.get('/auth/profile'),
  getStatus: () => api.get('/auth/status')
}

// Admin API
export const adminAPI = {
  // System statistics
  getStatistics: () => api.get('/admin/statistics'),
  
  // Parking lot management
  getParkingLots: (params = {}) => api.get('/admin/parking-lots', { params }),
  getParkingLot: (id) => api.get(`/admin/parking-lots/${id}`),
  createParkingLot: (data) => api.post('/admin/parking-lots', data),
  updateParkingLot: (id, data) => api.put(`/admin/parking-lots/${id}`, data),
  deleteParkingLot: (id) => api.delete(`/admin/parking-lots/${id}`),
  
  // User management
  getUsers: (params = {}) => api.get('/admin/users', { params }),
  getUser: (id) => api.get(`/admin/users/${id}`),
  toggleUserStatus: (id) => api.post(`/admin/users/${id}/toggle-status`),
  
  // Reservation management
  getReservations: (params = {}) => api.get('/admin/reservations', { params }),
  getReservation: (id) => api.get(`/admin/reservations/${id}`),
  forceReleaseReservation: (id) => api.post(`/admin/reservations/${id}/force-release`),
  
  // Analytics and reports
  getRevenueAnalytics: (params = {}) => api.get('/admin/analytics/revenue', { params }),
  getUsageAnalytics: () => api.get('/admin/analytics/usage')
}

// User API
export const userAPI = {
  // Parking lot browsing
  getParkingLots: (params = {}) => api.get('/dashboard/user/parking-lots', { params }),
  getParkingLot: (id) => api.get(`/dashboard/user/parking-lots/${id}`),
  
  // Reservation management
  createReservation: (data) => api.post('/dashboard/user/reservations', data),
  occupySpot: (reservationId) => api.post(`/dashboard/user/reservations/${reservationId}/occupy`),
  releaseSpot: (reservationId) => api.post(`/dashboard/user/reservations/${reservationId}/release`),
  
  // Parking history
  getReservations: (params = {}) => api.get('/dashboard/user/reservations', { params }),
  getReservation: (id) => api.get(`/dashboard/user/reservations/${id}`)
}

// Dashboard API
export const dashboardAPI = {
  getAdminDashboard: () => api.get('/dashboard/admin'),
  getUserDashboard: () => api.get('/dashboard/user'),
  getRedirect: () => api.get('/dashboard/redirect')
}

export default api 