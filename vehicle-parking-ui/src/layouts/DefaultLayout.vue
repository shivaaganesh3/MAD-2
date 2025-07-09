<template>
  <div class="layout">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-brand">
          <h2>🅿️ Vehicle Parking System</h2>
        </div>
        
        <div class="navbar-menu">
          <!-- User Menu -->
          <div class="user-menu">
            <span class="user-info">
              {{ currentUser?.username }} ({{ currentUser?.role }})
            </span>
            <button @click="logout" class="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <div class="layout-body">
      <!-- Sidebar Navigation -->
      <aside class="sidebar">
        <nav class="sidebar-nav">
          <!-- Admin Navigation -->
          <template v-if="isAdmin">
            <h3 class="nav-title">Admin Panel</h3>
            <router-link to="/admin/dashboard" class="nav-link">
              📊 Dashboard
            </router-link>
            <router-link to="/admin/parking-lots" class="nav-link">
              🏢 Parking Lots
            </router-link>
            <router-link to="/admin/users" class="nav-link">
              👥 Users
            </router-link>
            <router-link to="/admin/reservations" class="nav-link">
              📋 Reservations
            </router-link>
            <router-link to="/admin/analytics" class="nav-link">
              📈 Analytics
            </router-link>
            <router-link to="/admin/statistics" class="nav-link">
              📊 Statistics
            </router-link>
          </template>
          
          <!-- User Navigation -->
          <template v-if="isUser">
            <h3 class="nav-title">User Panel</h3>
            <router-link to="/user/dashboard" class="nav-link">
              🏠 Dashboard
            </router-link>
            <router-link to="/user/parking-lots" class="nav-link">
              🅿️ Find Parking
            </router-link>
            <router-link to="/user/history" class="nav-link">
              📜 History
            </router-link>
          </template>
        </nav>
      </aside>

      <!-- Main Content Area -->
      <main class="main-content">
        <div class="content-wrapper">
          <!-- Loading State -->
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Loading...</p>
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="error-state">
            <div class="error-message">
              <h3>❌ Error</h3>
              <p>{{ error }}</p>
              <button @click="clearError" class="btn btn-primary">
                Try Again
              </button>
            </div>
          </div>
          
          <!-- Main Router View -->
          <router-view v-else @loading="setLoading" @error="setError" />
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authHelpers } from '../services/api.js'

export default {
  name: 'DefaultLayout',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const error = ref(null)
    
    // Computed properties
    const currentUser = computed(() => authHelpers.getCurrentUser())
    const isAdmin = computed(() => authHelpers.isAdmin())
    const isUser = computed(() => authHelpers.isUser())
    
    // Methods
    const logout = async () => {
      try {
        loading.value = true
        await authHelpers.logout()
        router.push('/auth/login')
      } catch (err) {
        console.error('Logout error:', err)
        // Force logout even if API fails
        authHelpers.logout()
        router.push('/auth/login')
      } finally {
        loading.value = false
      }
    }
    
    const setLoading = (state) => {
      loading.value = state
    }
    
    const setError = (errorMessage) => {
      error.value = errorMessage
    }
    
    const clearError = () => {
      error.value = null
    }
    
    // Lifecycle
    onMounted(() => {
      // Check authentication on mount
      if (!authHelpers.isAuthenticated()) {
        router.push('/auth/login')
      }
    })
    
    return {
      loading,
      error,
      currentUser,
      isAdmin,
      isUser,
      logout,
      setLoading,
      setError,
      clearError
    }
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.5rem;
  max-width: 100%;
}

.navbar-brand h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  font-size: 0.9rem;
  font-weight: 500;
}

.logout-btn {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.3);
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255,255,255,0.3);
  transform: translateY(-1px);
}

.layout-body {
  display: flex;
  margin-top: 70px; /* Account for fixed navbar */
  min-height: calc(100vh - 70px);
}

.sidebar {
  width: 250px;
  background: white;
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
  position: fixed;
  left: 0;
  top: 70px;
  bottom: 0;
  overflow-y: auto;
}

.sidebar-nav {
  padding: 1.5rem 0;
}

.nav-title {
  padding: 0 1.5rem;
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-link {
  display: block;
  padding: 0.75rem 1.5rem;
  color: #555;
  text-decoration: none;
  border-left: 3px solid transparent;
  transition: all 0.3s ease;
}

.nav-link:hover {
  background: #f8f9ff;
  color: #667eea;
  border-left-color: #667eea;
}

.nav-link.router-link-active {
  background: linear-gradient(90deg, #f8f9ff 0%, #e8edff 100%);
  color: #667eea;
  border-left-color: #667eea;
  font-weight: 600;
}

.main-content {
  flex: 1;
  margin-left: 250px;
  background: #f5f5f5;
}

.content-wrapper {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-left: 4px solid #e74c3c;
}

.error-message h3 {
  margin: 0 0 1rem 0;
  color: #e74c3c;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #5a6fd8;
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .navbar-brand h2 {
    font-size: 1.2rem;
  }
  
  .user-info {
    display: none;
  }
}
</style> 