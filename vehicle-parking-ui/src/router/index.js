import { createRouter, createWebHistory } from 'vue-router'
import AdminDashboard from '../components/admin/AdminDashboard.vue'
import ParkingLotManager from '../components/admin/ParkingLotManager.vue'
import UserManager from '../components/admin/UserManager.vue'
import SystemStats from '../components/admin/SystemStats.vue'
import ReservationManager from '../components/admin/ReservationManager.vue'
import Analytics from '../components/admin/Analytics.vue'
import Login from '../components/auth/Login.vue'
import Register from '../components/auth/Register.vue'
import UserDashboard from '../components/user/UserDashboard.vue'
import ParkingLots from '../components/user/ParkingLots.vue'
import ParkingHistory from '../components/user/ParkingHistory.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  
  // Admin Routes
  {
    path: '/admin',
    redirect: '/admin/dashboard'
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/parking-lots',
    name: 'ParkingLotManager',
    component: ParkingLotManager,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'UserManager',
    component: UserManager,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/reservations',
    name: 'ReservationManager',
    component: ReservationManager,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/analytics',
    name: 'Analytics',
    component: Analytics,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/statistics',
    name: 'SystemStats',
    component: SystemStats,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  
  // User Routes
  {
    path: '/user',
    redirect: '/user/dashboard'
  },
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, requiresUser: true }
  },
  {
    path: '/user/parking-lots',
    name: 'ParkingLots',
    component: ParkingLots,
    meta: { requiresAuth: true, requiresUser: true }
  },
  {
    path: '/user/history',
    name: 'ParkingHistory',
    component: ParkingHistory,
    meta: { requiresAuth: true, requiresUser: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authentication
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    try {
      // Check authentication status
      const response = await fetch('/api/auth/status', {
        method: 'GET',
        credentials: 'include'
      })
      
      const authData = await response.json()
      
      if (!authData.authenticated) {
        next('/login')
        return
      }
      
      // Check admin requirement
      if (to.matched.some(record => record.meta.requiresAdmin)) {
        if (authData.user.role !== 'admin') {
          alert('Admin access required')
          next('/user/dashboard')
          return
        }
      }
      
      // Check user requirement
      if (to.matched.some(record => record.meta.requiresUser)) {
        if (authData.user.role !== 'user') {
          alert('User access required')
          next('/admin/dashboard')
          return
        }
      }
      
      next()
    } catch (error) {
      console.error('Auth check failed:', error)
      next('/login')
    }
  } else {
    next()
  }
})

export default router 