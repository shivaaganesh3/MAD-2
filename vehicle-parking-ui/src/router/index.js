import { createRouter, createWebHistory } from 'vue-router'
import AdminDashboard from '../components/admin/AdminDashboard.vue'
import ParkingLotManager from '../components/admin/ParkingLotManager.vue'
import UserManager from '../components/admin/UserManager.vue'
import SystemStats from '../components/admin/SystemStats.vue'
import Login from '../components/auth/Login.vue'
import Register from '../components/auth/Register.vue'

const routes = [
  {
    path: '/',
    redirect: '/admin/dashboard'
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
    path: '/admin/statistics',
    name: 'SystemStats',
    component: SystemStats,
    meta: { requiresAuth: true, requiresAdmin: true }
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
          next('/login')
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