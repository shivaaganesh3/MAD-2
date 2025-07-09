import { createRouter, createWebHistory } from 'vue-router'
import { authHelpers } from '../services/api.js'

// Admin Components
import AdminDashboard from '../components/admin/AdminDashboard.vue'
import ParkingLotManager from '../components/admin/ParkingLotManager.vue'
import UserManager from '../components/admin/UserManager.vue'
import SystemStats from '../components/admin/SystemStats.vue'
import ReservationManager from '../components/admin/ReservationManager.vue'
import Analytics from '../components/admin/Analytics.vue'

// Auth Components
import Login from '../components/auth/Login.vue'
import Register from '../components/auth/Register.vue'

// User Components
import UserDashboard from '../components/user/UserDashboard.vue'
import ParkingLots from '../components/user/ParkingLots.vue'
import ParkingHistory from '../components/user/ParkingHistory.vue'

// Layout Components (we'll create these)
import DefaultLayout from '../layouts/DefaultLayout.vue'
import AuthLayout from '../layouts/AuthLayout.vue'

const routes = [
  {
    path: '/',
    redirect: () => {
      if (authHelpers.isAuthenticated()) {
        if (authHelpers.isAdmin()) {
          return '/admin/dashboard'
        } else {
          return '/user/dashboard'
        }
      }
      return '/login'
    }
  },
  
  // Auth Routes (No Layout)
  {
    path: '/auth',
    component: AuthLayout,
    children: [
      {
        path: 'login',
        name: 'Login',
        component: Login,
        meta: { guest: true, title: 'Login - Vehicle Parking System' }
      },
      {
        path: 'register',
        name: 'Register',
        component: Register,
        meta: { guest: true, title: 'Register - Vehicle Parking System' }
      }
    ]
  },
  
  // Legacy route redirects
  {
    path: '/login',
    redirect: '/auth/login'
  },
  {
    path: '/register',
    redirect: '/auth/register'
  },
  
  // Admin Routes
  {
    path: '/admin',
    component: DefaultLayout,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        redirect: 'dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: { title: 'Admin Dashboard - Vehicle Parking System' }
      },
      {
        path: 'parking-lots',
        name: 'ParkingLotManager',
        component: ParkingLotManager,
        meta: { title: 'Parking Lot Management - Admin' }
      },
      {
        path: 'users',
        name: 'UserManager',
        component: UserManager,
        meta: { title: 'User Management - Admin' }
      },
      {
        path: 'reservations',
        name: 'ReservationManager',
        component: ReservationManager,
        meta: { title: 'Reservation Management - Admin' }
      },
      {
        path: 'analytics',
        name: 'Analytics',
        component: Analytics,
        meta: { title: 'Analytics - Admin' }
      },
      {
        path: 'statistics',
        name: 'SystemStats',
        component: SystemStats,
        meta: { title: 'System Statistics - Admin' }
      }
    ]
  },
  
  // User Routes
  {
    path: '/user',
    component: DefaultLayout,
    meta: { requiresAuth: true, requiresUser: true },
    children: [
      {
        path: '',
        redirect: 'dashboard'
      },
      {
        path: 'dashboard',
        name: 'UserDashboard',
        component: UserDashboard,
        meta: { title: 'Dashboard - Vehicle Parking System' }
      },
      {
        path: 'parking-lots',
        name: 'ParkingLots',
        component: ParkingLots,
        meta: { title: 'Available Parking Lots' }
      },
      {
        path: 'history',
        name: 'ParkingHistory',
        component: ParkingHistory,
        meta: { title: 'Parking History' }
      }
    ]
  },
  
  // Catch all 404 route
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Enhanced Navigation Guards with JWT Authentication
router.beforeEach(async (to, from, next) => {
  // Set page title
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  console.log('🛂 Route Guard:', { to: to.path, from: from.path })
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authHelpers.isAuthenticated()) {
      console.log('🚫 Not authenticated, redirecting to login')
      next('/auth/login')
      return
    }
    
    // Verify token is still valid by checking with server
    try {
      const tokenStatus = authHelpers.getTokenStatus()
      if (!tokenStatus || tokenStatus.isExpired) {
        console.log('🔄 Token expired, redirecting to login')
        authHelpers.logout()
        next('/auth/login')
        return
      }
      
      // Check admin requirement
      if (to.matched.some(record => record.meta.requiresAdmin)) {
        if (!authHelpers.isAdmin()) {
          console.log('👑 Admin access required, redirecting user')
          next('/user/dashboard')
          return
        }
      }
      
      // Check user requirement
      if (to.matched.some(record => record.meta.requiresUser)) {
        if (!authHelpers.isUser()) {
          console.log('👤 User access required, redirecting admin')
          next('/admin/dashboard')
          return
        }
      }
      
      console.log('✅ Authentication check passed')
      next()
    } catch (error) {
      console.error('❌ Auth verification failed:', error)
      authHelpers.logout()
      next('/auth/login')
    }
  } 
  // Check if route is for guests only (login/register)
  else if (to.matched.some(record => record.meta.guest)) {
    if (authHelpers.isAuthenticated()) {
      console.log('🔄 Already authenticated, redirecting to dashboard')
      if (authHelpers.isAdmin()) {
        next('/admin/dashboard')
      } else {
        next('/user/dashboard')
      }
      return
    }
    next()
  } 
  // Public routes
  else {
    next()
  }
})

// Global error handler for route navigation
router.onError((error) => {
  console.error('🚨 Router error:', error)
  // You could show a global error message here
})

export default router 