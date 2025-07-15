<template>
  <div id="app">
    <!-- Global Loading Overlay -->
    <div v-if="globalLoading" class="position-fixed top-0 start-0 w-100 h-100 d-flex flex-column align-items-center justify-content-center" style="background: rgba(255, 255, 255, 0.9); z-index: 9999; backdrop-filter: blur(5px);">
      <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-muted fw-medium">Loading...</p>
    </div>
    
    <!-- Global Error Handler -->
    <div v-if="globalError" class="position-fixed top-50 start-50 translate-middle" style="z-index: 9998;">
      <div class="card border-danger shadow-lg" style="max-width: 400px; width: 90vw;">
        <div class="card-header bg-danger text-white d-flex align-items-center">
          <i class="fas fa-exclamation-triangle me-2"></i>
          <h5 class="mb-0">Application Error</h5>
        </div>
        <div class="card-body">
          <p class="mb-3">{{ globalError }}</p>
          <button @click="clearGlobalError" class="btn btn-danger w-100">
            <i class="fas fa-times me-2"></i>Dismiss
          </button>
        </div>
      </div>
    </div>
    
    <!-- Global Notification System (Toast) -->
    <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 9997;">
      <div 
        v-if="notification" 
        :class="['toast', 'show', `border-${getNotificationColor(notification.type)}`]"
        role="alert" 
        aria-live="assertive" 
        aria-atomic="true"
      >
        <div :class="['toast-header', `bg-${getNotificationColor(notification.type)}-subtle`]">
          <i :class="getNotificationIcon(notification.type)" class="me-2"></i>
          <strong class="me-auto">{{ getNotificationTitle(notification.type) }}</strong>
          <small class="text-muted">now</small>
          <button @click="clearNotification" type="button" class="btn-close" aria-label="Close"></button>
        </div>
        <div class="toast-body">
          {{ notification.message }}
        </div>
      </div>
    </div>
    
    <!-- Main Router View -->
    <router-view />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { authHelpers } from './services/api.js'

export default {
  name: 'App',
  setup() {
    const globalLoading = ref(false)
    const globalError = ref(null)
    const notification = ref(null)
    const notificationTimeout = ref(null)
    
    // Global event listeners
    const handleGlobalError = (error) => {
      console.error('Global error:', error)
      globalError.value = error.message || 'An unexpected error occurred'
    }
    
    const handleGlobalLoading = (loading) => {
      globalLoading.value = loading
    }
    
    const showNotification = (message, type = 'info') => {
      // Clear existing notification timeout
      if (notificationTimeout.value) {
        clearTimeout(notificationTimeout.value)
      }
      
      notification.value = { message, type }
      
      // Auto-hide notification after 5 seconds
      notificationTimeout.value = setTimeout(() => {
        clearNotification()
      }, 5000)
    }
    
    const clearGlobalError = () => {
      globalError.value = null
    }
    
    const clearNotification = () => {
      if (notificationTimeout.value) {
        clearTimeout(notificationTimeout.value)
        notificationTimeout.value = null
      }
      notification.value = null
    }
    
    const getNotificationIcon = (type) => {
      const icons = {
        success: 'fas fa-check-circle text-success',
        error: 'fas fa-exclamation-circle text-danger',
        warning: 'fas fa-exclamation-triangle text-warning',
        info: 'fas fa-info-circle text-info'
      }
      return icons[type] || 'fas fa-info-circle text-info'
    }
    
    const getNotificationColor = (type) => {
      const colors = {
        success: 'success',
        error: 'danger',
        warning: 'warning',
        info: 'info'
      }
      return colors[type] || 'info'
    }
    
    const getNotificationTitle = (type) => {
      const titles = {
        success: 'Success',
        error: 'Error',
        warning: 'Warning',
        info: 'Information'
      }
      return titles[type] || 'Notification'
    }
    
    // Token expiration handler
    const handleTokenExpiration = () => {
      showNotification('Your session has expired. Please login again.', 'warning')
      setTimeout(() => {
        authHelpers.logout()
        window.location.href = '/auth/login'
      }, 2000)
    }
    
    // Initialize app
    onMounted(() => {
      // Set up global event listeners
      window.addEventListener('error', handleGlobalError)
      window.addEventListener('unhandledrejection', (event) => {
        handleGlobalError(event.reason)
      })
      
      // Check authentication status on app start
      if (authHelpers.isAuthenticated()) {
        const tokenStatus = authHelpers.getTokenStatus()
        if (tokenStatus?.isExpired) {
          handleTokenExpiration()
        } else if (tokenStatus?.willExpireSoon) {
          showNotification(
            `Your session will expire in ${tokenStatus.timeUntilExpiryMinutes} minutes.`,
            'warning'
          )
        }
      }
      
      // Set up periodic token check
      const tokenCheckInterval = setInterval(() => {
        if (authHelpers.isAuthenticated()) {
          const tokenStatus = authHelpers.getTokenStatus()
          if (tokenStatus?.isExpired) {
            clearInterval(tokenCheckInterval)
            handleTokenExpiration()
          }
        }
      }, 60000) // Check every minute
      
      // Store interval for cleanup
      window.tokenCheckInterval = tokenCheckInterval
      
      console.log('🚀 Vehicle Parking System initialized')
    })
    
    onUnmounted(() => {
      // Clean up event listeners
      window.removeEventListener('error', handleGlobalError)
      window.removeEventListener('unhandledrejection', handleGlobalError)
      
      // Clear token check interval
      if (window.tokenCheckInterval) {
        clearInterval(window.tokenCheckInterval)
      }
      
      // Clear notification timeout
      if (notificationTimeout.value) {
        clearTimeout(notificationTimeout.value)
      }
    })
    
    // Provide global methods to child components
    window.app = {
      showNotification,
      setGlobalLoading: handleGlobalLoading,
      setGlobalError: handleGlobalError
    }
    
    return {
      globalLoading,
      globalError,
      notification,
      clearGlobalError,
      clearNotification,
      getNotificationIcon,
      getNotificationColor,
      getNotificationTitle
    }
  }
}
</script>

<style>
/* CSS Reset and Global Styles */
*, *::before, *::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f8f9fa;
  color: #333;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
  position: relative;
}

/* Enhanced Bootstrap Toast Styling */
.toast {
  min-width: 350px;
  border-width: 2px;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.toast-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

.toast-body {
  padding: 0.75rem;
  font-weight: 500;
}

/* Enhanced button styling */
.btn {
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.btn-primary:hover,
.btn-primary:focus {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(102, 126, 234, 0.4);
}

/* Enhanced form controls */
.form-control,
.form-select {
  border-radius: 0.5rem;
  border: 2px solid #e9ecef;
  transition: all 0.3s ease;
}

.form-control:focus,
.form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Enhanced cards */
.card {
  border-radius: 1rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: 1px solid rgba(0, 0, 0, 0.125);
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.card-header {
  border-radius: 1rem 1rem 0 0 !important;
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
  font-weight: 600;
}

/* Enhanced badges */
.badge {
  font-weight: 500;
  padding: 0.5em 0.75em;
  border-radius: 0.5rem;
}

/* Enhanced alerts */
.alert {
  border-radius: 0.75rem;
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

/* Responsive utilities */
@media (max-width: 576px) {
  .toast {
    min-width: 280px;
    margin: 0 0.5rem;
  }
  
  .position-fixed.top-50.start-50.translate-middle {
    width: 95vw !important;
    max-width: none !important;
  }
}

/* Enhanced loading states */
.spinner-border {
  animation-duration: 0.75s;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Focus indicators for accessibility */
.btn:focus,
.form-control:focus,
.form-select:focus,
.nav-link:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}

/* Enhanced text selection */
::selection {
  background-color: rgba(102, 126, 234, 0.3);
  color: inherit;
}

/* Reduced motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  body {
    background-color: #1a1a1a;
    color: #e9ecef;
  }
}

/* Print styles */
@media print {
  .toast-container,
  .position-fixed,
  .btn,
  .navbar {
    display: none !important;
  }
}
</style>
