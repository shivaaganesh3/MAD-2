<template>
  <div class="layout">
    <!-- Bootstrap Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top custom-navbar">
      <div class="container-fluid">
        <!-- Brand -->
        <a class="navbar-brand fw-bold" href="#">
          <i class="fas fa-parking me-2"></i>Vehicle Parking System
        </a>
        
        <!-- Mobile menu toggle -->
        <button 
          class="navbar-toggler border-0" 
          type="button" 
          data-bs-toggle="offcanvas" 
          data-bs-target="#sidebarOffcanvas"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <!-- User info and logout (visible on desktop) -->
        <div class="navbar-nav ms-auto d-none d-lg-flex">
          <div class="nav-item dropdown">
            <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" role="button" data-bs-toggle="dropdown">
              <i class="fas fa-user-circle me-2 fs-5"></i>
              <span class="fw-medium">{{ currentUser?.username }}</span>
              <span class="badge bg-light text-dark ms-2">{{ currentUser?.role }}</span>
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><h6 class="dropdown-header">Signed in as {{ currentUser?.username }}</h6></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#"><i class="fas fa-user me-2"></i>Profile</a></li>
              <li><a class="dropdown-item" href="#"><i class="fas fa-cog me-2"></i>Settings</a></li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <button @click="logout" class="dropdown-item text-danger">
                  <i class="fas fa-sign-out-alt me-2"></i>Logout
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>

    <div class="layout-body d-flex">
      <!-- Desktop Sidebar -->
      <aside class="sidebar d-none d-lg-block">
        <nav class="sidebar-nav p-3">
          <!-- Admin Navigation -->
          <template v-if="isAdmin">
            <h6 class="nav-title text-muted text-uppercase fw-bold mb-3">
              <i class="fas fa-crown me-2 text-warning"></i>Admin Panel
            </h6>
            <div class="nav-links">
              <router-link to="/admin/dashboard" class="nav-link d-flex align-items-center p-2 mb-1 rounded">
                <i class="fas fa-tachometer-alt me-3"></i>Dashboard
              </router-link>
              <router-link to="/admin/parking-lots" class="nav-link d-flex align-items-center p-2 mb-1 rounded">
                <i class="fas fa-building me-3"></i>Parking Lots
              </router-link>
              <router-link to="/admin/users" class="nav-link d-flex align-items-center p-2 mb-1 rounded">
                <i class="fas fa-users me-3"></i>Users
              </router-link>
              <router-link to="/admin/reservations" class="nav-link d-flex align-items-center p-2 mb-1 rounded">
                <i class="fas fa-clipboard-list me-3"></i>Reservations
              </router-link>
              <router-link to="/admin/analytics" class="nav-link d-flex align-items-center p-2 mb-1 rounded">
                <i class="fas fa-chart-line me-3"></i>Analytics
              </router-link>
              <router-link to="/admin/statistics" class="nav-link d-flex align-items-center p-2 mb-1 rounded">
                <i class="fas fa-chart-bar me-3"></i>Statistics
              </router-link>
            </div>
          </template>
          
          <!-- User Navigation -->
          <template v-if="isUser">
            <h6 class="nav-title text-muted text-uppercase fw-bold mb-3">
              <i class="fas fa-user me-2 text-primary"></i>User Panel
            </h6>
            <div class="nav-links">
              <router-link to="/user/dashboard" class="nav-link d-flex align-items-center p-2 mb-1 rounded">
                <i class="fas fa-home me-3"></i>Dashboard
              </router-link>
              <router-link to="/user/parking-lots" class="nav-link d-flex align-items-center p-2 mb-1 rounded">
                <i class="fas fa-parking me-3"></i>Find Parking
              </router-link>
              <router-link to="/user/history" class="nav-link d-flex align-items-center p-2 mb-1 rounded">
                <i class="fas fa-history me-3"></i>History
              </router-link>
            </div>
          </template>
        </nav>
      </aside>

      <!-- Mobile Offcanvas Sidebar -->
      <div class="offcanvas offcanvas-start" tabindex="-1" id="sidebarOffcanvas">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title">
            <i class="fas fa-parking me-2"></i>Navigation
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button>
        </div>
        <div class="offcanvas-body p-0">
          <nav class="sidebar-nav p-3">
            <!-- User info on mobile -->
            <div class="user-info-mobile bg-light p-3 mb-3 rounded">
              <div class="d-flex align-items-center">
                <i class="fas fa-user-circle me-2 fs-4 text-primary"></i>
                <div>
                  <div class="fw-medium">{{ currentUser?.username }}</div>
                  <small class="text-muted">{{ currentUser?.role }}</small>
                </div>
              </div>
              <button @click="logout" class="btn btn-outline-danger btn-sm mt-2 w-100">
                <i class="fas fa-sign-out-alt me-2"></i>Logout
              </button>
            </div>
            
            <!-- Admin Navigation (Mobile) -->
            <template v-if="isAdmin">
              <h6 class="nav-title text-muted text-uppercase fw-bold mb-3">
                <i class="fas fa-crown me-2 text-warning"></i>Admin Panel
              </h6>
              <div class="nav-links">
                <router-link to="/admin/dashboard" class="nav-link d-flex align-items-center p-2 mb-1 rounded" data-bs-dismiss="offcanvas">
                  <i class="fas fa-tachometer-alt me-3"></i>Dashboard
                </router-link>
                <router-link to="/admin/parking-lots" class="nav-link d-flex align-items-center p-2 mb-1 rounded" data-bs-dismiss="offcanvas">
                  <i class="fas fa-building me-3"></i>Parking Lots
                </router-link>
                <router-link to="/admin/users" class="nav-link d-flex align-items-center p-2 mb-1 rounded" data-bs-dismiss="offcanvas">
                  <i class="fas fa-users me-3"></i>Users
                </router-link>
                <router-link to="/admin/reservations" class="nav-link d-flex align-items-center p-2 mb-1 rounded" data-bs-dismiss="offcanvas">
                  <i class="fas fa-clipboard-list me-3"></i>Reservations
                </router-link>
                <router-link to="/admin/analytics" class="nav-link d-flex align-items-center p-2 mb-1 rounded" data-bs-dismiss="offcanvas">
                  <i class="fas fa-chart-line me-3"></i>Analytics
                </router-link>
                <router-link to="/admin/statistics" class="nav-link d-flex align-items-center p-2 mb-1 rounded" data-bs-dismiss="offcanvas">
                  <i class="fas fa-chart-bar me-3"></i>Statistics
                </router-link>
              </div>
            </template>
            
            <!-- User Navigation (Mobile) -->
            <template v-if="isUser">
              <h6 class="nav-title text-muted text-uppercase fw-bold mb-3">
                <i class="fas fa-user me-2 text-primary"></i>User Panel
              </h6>
              <div class="nav-links">
                <router-link to="/user/dashboard" class="nav-link d-flex align-items-center p-2 mb-1 rounded" data-bs-dismiss="offcanvas">
                  <i class="fas fa-home me-3"></i>Dashboard
                </router-link>
                <router-link to="/user/parking-lots" class="nav-link d-flex align-items-center p-2 mb-1 rounded" data-bs-dismiss="offcanvas">
                  <i class="fas fa-parking me-3"></i>Find Parking
                </router-link>
                <router-link to="/user/history" class="nav-link d-flex align-items-center p-2 mb-1 rounded" data-bs-dismiss="offcanvas">
                  <i class="fas fa-history me-3"></i>History
                </router-link>
              </div>
            </template>
          </nav>
        </div>
      </div>

      <!-- Main Content Area -->
      <main class="main-content flex-fill">
        <div class="content-wrapper">
          <!-- Loading State -->
          <div v-if="loading" class="d-flex flex-column align-items-center justify-content-center" style="min-height: 300px;">
            <div class="spinner-border text-primary mb-3" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="text-muted">Loading...</p>
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="alert alert-danger d-flex align-items-center" role="alert">
            <i class="fas fa-exclamation-triangle me-3"></i>
            <div class="flex-fill">
              <h5 class="alert-heading mb-1">Error</h5>
              <p class="mb-2">{{ error }}</p>
              <button @click="clearError" class="btn btn-outline-danger btn-sm">
                <i class="fas fa-redo me-1"></i>Try Again
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
  background-color: #f8f9fa;
}

.custom-navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  z-index: 1030;
}

.navbar-brand {
  font-size: 1.5rem;
}

.layout-body {
  margin-top: 56px; /* Bootstrap navbar height */
  min-height: calc(100vh - 56px);
}

.sidebar {
  width: 260px;
  background: white;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  border-right: 1px solid #e9ecef;
  overflow-y: auto;
}

/* Content wrapper with optimized spacing - see responsive rules below */

/* Legacy nav-link styles for navigation */
.nav-title {
  font-size: 0.75rem;
  letter-spacing: 0.5px;
}

.nav-link {
  color: #6c757d;
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-link:hover {
  background-color: #f8f9fa;
  color: #667eea;
  text-decoration: none;
}

.nav-link.router-link-active {
  background: linear-gradient(90deg, #f8f9ff 0%, #e8edff 100%);
  color: #667eea;
  font-weight: 600;
  border-left: 3px solid #667eea;
  margin-left: -1rem;
  padding-left: 1rem !important;
}

.main-content {
  background: #f8f9fa;
  min-height: calc(100vh - 56px);
}

/* Bootstrap dropdown customization */
.dropdown-menu {
  border: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  border-radius: 8px;
}

.dropdown-item {
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item.text-danger:hover {
  background-color: #f8d7da;
}

/* Offcanvas customization */
.offcanvas {
  width: 260px !important;
}

.user-info-mobile {
  border: 1px solid #e9ecef;
}

/* Enhanced mobile responsiveness */
@media (max-width: 991.98px) {
  .main-content {
    margin-left: 0;
  }
}

/* Responsive content wrapper spacing */
@media (min-width: 992px) {
  .content-wrapper {
    padding: 1.5rem 2rem 2rem 1.5rem;
  }
}

@media (max-width: 991.98px) {
  .content-wrapper {
    padding: 1rem 1.5rem 1.5rem 1.5rem;
  }
}

@media (max-width: 576px) {
  .content-wrapper {
    padding: 1rem 1rem 1.5rem 1rem;
  }
}

/* Loading spinner customization */
.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* Enhanced focus states for accessibility */
.nav-link:focus,
.btn:focus,
.dropdown-toggle:focus {
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}
</style> 