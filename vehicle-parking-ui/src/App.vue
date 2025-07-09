<template>
  <div id="app">
    <!-- Global Loading Overlay -->
    <div v-if="globalLoading" class="global-loading">
      <div class="loading-spinner"></div>
      <p>Loading...</p>
    </div>
    
    <!-- Global Error Handler -->
    <div v-if="globalError" class="global-error">
      <div class="error-content">
        <h3>⚠️ Application Error</h3>
        <p>{{ globalError }}</p>
        <button @click="clearGlobalError" class="error-button">
          Dismiss
        </button>
      </div>
    </div>
    
    <!-- Global Notification System -->
    <div v-if="notification" :class="['notification', `notification-${notification.type}`]">
      <div class="notification-content">
        <span class="notification-icon">
          {{ getNotificationIcon(notification.type) }}
        </span>
        <span class="notification-message">{{ notification.message }}</span>
        <button @click="clearNotification" class="notification-close">
          ×
        </button>
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
    
    // Global event listeners
    const handleGlobalError = (error) => {
      console.error('Global error:', error)
      globalError.value = error.message || 'An unexpected error occurred'
    }
    
    const handleGlobalLoading = (loading) => {
      globalLoading.value = loading
    }
    
    const showNotification = (message, type = 'info') => {
      notification.value = { message, type }
      // Auto-hide notification after 5 seconds
      setTimeout(() => {
        clearNotification()
      }, 5000)
    }
    
    const clearGlobalError = () => {
      globalError.value = null
    }
    
    const clearNotification = () => {
      notification.value = null
    }
    
    const getNotificationIcon = (type) => {
      const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
      }
      return icons[type] || 'ℹ️'
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
      getNotificationIcon
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
  background-color: #f5f5f5;
  color: #333;
  line-height: 1.6;
}

#app {
  min-height: 100vh;
  position: relative;
}

/* Global Loading Overlay */
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Global Error Handler */
.global-error {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  z-index: 9998;
  max-width: 400px;
  width: 90%;
  border-left: 4px solid #e74c3c;
}

.error-content h3 {
  color: #e74c3c;
  margin: 0 0 1rem 0;
}

.error-content p {
  margin: 0 0 1.5rem 0;
  color: #666;
}

.error-button {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s ease;
}

.error-button:hover {
  background: #c0392b;
}

/* Global Notification System */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 9997;
  min-width: 300px;
  max-width: 500px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification-content {
  display: flex;
  align-items: center;
  padding: 1rem;
  gap: 0.75rem;
}

.notification-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.notification-message {
  flex: 1;
  font-size: 0.9rem;
  line-height: 1.4;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background 0.2s ease;
}

.notification-close:hover {
  background: #f0f0f0;
}

/* Notification Types */
.notification-success {
  border-left: 4px solid #27ae60;
}

.notification-error {
  border-left: 4px solid #e74c3c;
}

.notification-warning {
  border-left: 4px solid #f39c12;
}

.notification-info {
  border-left: 4px solid #3498db;
}

/* Global Utility Classes */
.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  text-decoration: none;
  text-align: center;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  background: #667eea;
  color: white;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #6c757d;
}

.btn-secondary:hover {
  background: #5a6268;
  box-shadow: 0 4px 12px rgba(108, 117, 125, 0.4);
}

.btn-danger {
  background: #e74c3c;
}

.btn-danger:hover {
  background: #c0392b;
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.4);
}

.btn-success {
  background: #27ae60;
}

.btn-success:hover {
  background: #229954;
  box-shadow: 0 4px 12px rgba(39, 174, 96, 0.4);
}

/* Form Elements */
.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border-color 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input.error {
  border-color: #e74c3c;
}

.form-error {
  color: #e74c3c;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

/* Card Components */
.card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.card-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e1e5e9;
  background: #f8f9fa;
}

.card-body {
  padding: 1.5rem;
}

.card-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e1e5e9;
  background: #f8f9fa;
}

/* Responsive Utilities */
@media (max-width: 768px) {
  .notification {
    top: 10px;
    right: 10px;
    left: 10px;
    min-width: auto;
  }
  
  .global-error {
    margin: 1rem;
    width: calc(100% - 2rem);
  }
}

/* Accessibility Improvements */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Focus styles for keyboard navigation */
button:focus,
input:focus,
select:focus,
textarea:focus,
a:focus {
  outline: 2px solid #667eea;
  outline-offset: 2px;
}
</style>
