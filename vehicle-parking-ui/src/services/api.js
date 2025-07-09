import axios from 'axios'

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Enhanced Token management utilities
const TokenManager = {
  getToken() {
    return localStorage.getItem('auth_token')
  },
  
  setToken(token) {
    localStorage.setItem('auth_token', token)
    // Store token creation time for debugging
    localStorage.setItem('auth_token_created', Date.now().toString())
    console.log('🔐 Token stored successfully')
  },
  
  removeToken() {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_token_created')
    console.log('🗑️ Token removed')
  },
  
  isTokenExpired(token) {
    if (!token) return true
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Date.now() / 1000
      const timeUntilExpiry = payload.exp - currentTime
      
      // Log token status for debugging
      console.log('⏰ Token expiry check:', {
        expiresAt: new Date(payload.exp * 1000).toLocaleString(),
        currentTime: new Date().toLocaleString(),
        timeUntilExpiryMinutes: Math.round(timeUntilExpiry / 60),
        isExpired: payload.exp < currentTime
      })
      
      return payload.exp < currentTime
    } catch (error) {
      console.error('❌ Token parsing error:', error)
      return true
    }
  },
  
  getTokenInfo() {
    const token = this.getToken()
    if (!token) return null
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Date.now() / 1000
      const timeUntilExpiry = payload.exp - currentTime
      
      return {
        user: payload.username,
        role: payload.role,
        expiresAt: new Date(payload.exp * 1000),
        timeUntilExpiryMinutes: Math.round(timeUntilExpiry / 60),
        isExpired: payload.exp < currentTime,
        willExpireSoon: timeUntilExpiry < 300 // Less than 5 minutes
      }
    } catch (error) {
      return null
    }
  },
  
  shouldRefreshToken() {
    const tokenInfo = this.getTokenInfo()
    return tokenInfo && !tokenInfo.isExpired && tokenInfo.willExpireSoon
  }
}

// Request interceptor to add JWT token and handle auto-refresh
api.interceptors.request.use(
  async (config) => {
    const token = TokenManager.getToken()
    
    if (token) {
      if (TokenManager.isTokenExpired(token)) {
        console.log('🔄 Token expired, redirecting to login')
        TokenManager.removeToken()
        window.location.href = '/login'
        return Promise.reject(new Error('Token expired'))
      }
      
      // Auto-refresh if token will expire soon (except for auth endpoints)
      if (TokenManager.shouldRefreshToken() && !config.url.includes('/auth/')) {
        try {
          console.log('🔄 Refreshing token automatically...')
          const refreshResponse = await axios.post(
            'http://localhost:5000/api/auth/refresh',
            {},
            { headers: { Authorization: `Bearer ${token}` } }
          )
          
          if (refreshResponse.data.success) {
            TokenManager.setToken(refreshResponse.data.token)
            config.headers.Authorization = `Bearer ${refreshResponse.data.token}`
            console.log('✅ Token refreshed successfully')
          }
        } catch (refreshError) {
          console.error('❌ Token refresh failed:', refreshError)
          TokenManager.removeToken()
          window.location.href = '/login'
          return Promise.reject(new Error('Token refresh failed'))
        }
      } else {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling and token management
api.interceptors.response.use(
  (response) => {
    // Store token if provided in response
    if (response.data.token) {
      TokenManager.setToken(response.data.token)
    }
    return response
  },
  (error) => {
    console.error('🚨 API Error:', {
      status: error.response?.status,
      url: error.config?.url,
      message: error.response?.data?.message
    })
    
    if (error.response?.status === 401) {
      // Unauthorized - remove invalid token and redirect to login
      console.log('🔓 Unauthorized, clearing token and redirecting')
      TokenManager.removeToken()
      
      // Don't redirect if already on login page
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// Authentication API
export const authAPI = {
  login: (credentials) => {
    // Add user_type to credentials if not present
    const loginData = {
      user_type: 'user',
      ...credentials
    }
    console.log('🔐 Attempting user login...')
    return api.post('/auth/login', loginData)
  },
  
  adminLogin: (credentials) => {
    // Specifically for admin login
    const loginData = {
      user_type: 'admin',
      ...credentials
    }
    console.log('👑 Attempting admin login...')
    return api.post('/auth/login', loginData)
  },
  
  register: (userData) => api.post('/auth/register', userData),
  
  logout: () => {
    console.log('👋 Logging out...')
    const promise = api.post('/auth/logout')
    // Remove token regardless of API response
    promise.finally(() => {
      TokenManager.removeToken()
    })
    return promise
  },
  
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (userData) => api.put('/auth/profile', userData),
  verifyToken: () => api.get('/auth/verify'),
  refreshToken: () => api.post('/auth/refresh')
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

// Enhanced Auth helper functions
export const authHelpers = {
  isAuthenticated() {
    const token = TokenManager.getToken()
    const isValid = token && !TokenManager.isTokenExpired(token)
    console.log('🔍 Auth check:', { hasToken: !!token, isValid })
    return isValid
  },
  
  getCurrentUser() {
    const token = TokenManager.getToken()
    if (!token || TokenManager.isTokenExpired(token)) {
      return null
    }
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return {
        id: payload.user_id,
        username: payload.username,
        role: payload.role,
        email: payload.email,
        full_name: payload.full_name,
        expires_at: payload.exp
      }
    } catch (error) {
      console.error('❌ Error parsing user from token:', error)
      return null
    }
  },
  
  getUserRole() {
    const user = this.getCurrentUser()
    return user ? user.role : null
  },
  
  isAdmin() {
    return this.getUserRole() === 'admin'
  },
  
  isUser() {
    return this.getUserRole() === 'user'
  },
  
  getTokenStatus() {
    return TokenManager.getTokenInfo()
  },
  
  logout() {
    console.log('👋 Manual logout triggered')
    TokenManager.removeToken()
    window.location.href = '/login'
  },
  
  // Debug function to check token status
  debugTokenStatus() {
    const tokenInfo = TokenManager.getTokenInfo()
    console.log('🔍 Token Debug Info:', tokenInfo)
    return tokenInfo
  }
}

// Add a periodic token status check
if (typeof window !== 'undefined') {
  setInterval(() => {
    const tokenInfo = TokenManager.getTokenInfo()
    if (tokenInfo && tokenInfo.willExpireSoon && !tokenInfo.isExpired) {
      console.log('⚠️ Token will expire soon:', tokenInfo.timeUntilExpiryMinutes, 'minutes')
    }
  }, 60000) // Check every minute
}

export { TokenManager }
export default api 