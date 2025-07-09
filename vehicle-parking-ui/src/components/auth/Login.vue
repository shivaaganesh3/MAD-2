<template>
  <div class="login-form">
    <!-- Header -->
    <div class="form-header">
      <h2>Welcome Back</h2>
      <p>Sign in to your account</p>
    </div>

    <!-- Login Form -->
    <form @submit.prevent="handleLogin" class="auth-form">
      <!-- Error Alert -->
      <div v-if="error" class="error-alert">
        <div class="error-content">
          <svg class="error-icon" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
          </svg>
          <p>{{ error }}</p>
        </div>
      </div>

      <!-- Form Fields -->
      <div class="form-group">
        <label for="username" class="form-label">
          Username
        </label>
        <input
          id="username"
          v-model="form.username"
          type="text"
          required
          :disabled="loading"
          class="form-input"
          :class="{ 'error': validationErrors.username }"
          placeholder="Enter your username"
          @input="clearFieldError('username')"
        />
        <div v-if="validationErrors.username" class="form-error">
          {{ validationErrors.username }}
        </div>
      </div>

      <div class="form-group">
        <label for="password" class="form-label">
          Password
        </label>
        <div class="password-input-container">
          <input
            id="password"
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            required
            :disabled="loading"
            class="form-input"
            :class="{ 'error': validationErrors.password }"
            placeholder="Enter your password"
            @input="clearFieldError('password')"
          />
          <button
            type="button"
            @click="togglePasswordVisibility"
            class="password-toggle"
            :disabled="loading"
          >
            <svg v-if="showPassword" class="password-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
            </svg>
            <svg v-else class="password-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
            </svg>
          </button>
        </div>
        <div v-if="validationErrors.password" class="form-error">
          {{ validationErrors.password }}
        </div>
      </div>

      <!-- Login Button -->
      <button
        type="submit"
        :disabled="loading || !isFormValid"
        class="login-button"
        :class="{ 'loading': loading }"
      >
        <span v-if="loading" class="loading-spinner"></span>
        {{ loading ? 'Signing in...' : 'Sign in' }}
      </button>

      <!-- Register Link -->
      <div class="auth-link">
        <span>Don't have an account?</span>
        <router-link to="/auth/register" class="link">
          Sign up here
        </router-link>
      </div>
    </form>

    <!-- Demo Credentials -->
    <div class="demo-credentials">
      <div class="demo-header">
        <svg class="demo-icon" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
        </svg>
        <h3>Demo Credentials</h3>
      </div>
      <div class="demo-content">
        <div class="demo-account" @click="fillDemoCredentials('admin')">
          <strong>Admin:</strong> admin / admin123
        </div>
        <div class="demo-account" @click="fillDemoCredentials('user')">
          <strong>User:</strong> john_doe / password123
        </div>
        <p class="demo-hint">Click to auto-fill</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI, authHelpers } from '../../services/api.js'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    
    const form = ref({
      username: '',
      password: ''
    })
    
    const loading = ref(false)
    const error = ref('')
    const showPassword = ref(false)
    const validationErrors = ref({})
    
    // Computed properties
    const isFormValid = computed(() => {
      return form.value.username.trim() && 
             form.value.password.length >= 3 &&
             Object.keys(validationErrors.value).length === 0
    })
    
    // Methods
    const validateForm = () => {
      const errors = {}
      
      if (!form.value.username.trim()) {
        errors.username = 'Username is required'
      } else if (form.value.username.length < 2) {
        errors.username = 'Username must be at least 2 characters'
      }
      
      if (!form.value.password) {
        errors.password = 'Password is required'
      } else if (form.value.password.length < 3) {
        errors.password = 'Password must be at least 3 characters'
      }
      
      validationErrors.value = errors
      return Object.keys(errors).length === 0
    }
    
    const clearFieldError = (field) => {
      if (validationErrors.value[field]) {
        delete validationErrors.value[field]
        validationErrors.value = { ...validationErrors.value }
      }
      if (error.value) {
        error.value = ''
      }
    }
    
    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }
    
    const fillDemoCredentials = (type) => {
      if (type === 'admin') {
        form.value.username = 'admin'
        form.value.password = 'admin123'
      } else {
        form.value.username = 'john_doe'
        form.value.password = 'password123'
      }
      // Clear any existing errors
      validationErrors.value = {}
      error.value = ''
    }
    
    const handleLogin = async () => {
      try {
        // Validate form first
        if (!validateForm()) {
          return
        }
        
        loading.value = true
        error.value = ''
        
        console.log('🔐 Attempting login for:', form.value.username)
        
        // Show global loading
        if (window.app?.setGlobalLoading) {
          window.app.setGlobalLoading(true)
        }
        
        // Try smart authentication (user first, then admin)
        let response
        let loginType = 'user'
        
        try {
          response = await authAPI.login(form.value)
          console.log('✅ User login successful')
        } catch (userLoginError) {
          if (userLoginError.response?.status === 401) {
            try {
              console.log('🔄 Trying admin login...')
              response = await authAPI.adminLogin(form.value)
              loginType = 'admin'
              console.log('✅ Admin login successful')
            } catch (adminLoginError) {
              console.error('❌ Both login attempts failed')
              throw userLoginError // Use the original user login error
            }
          } else {
            throw userLoginError
          }
        }
        
        if (response.data.success) {
          const user = response.data.user
          console.log('🎉 Login successful:', { username: user.username, role: user.role })
          
          // Show success notification
          if (window.app?.showNotification) {
            window.app.showNotification(
              `Welcome back, ${user.username}! Logged in as ${user.role}.`,
              'success'
            )
          }
          
          // Navigate based on role
          const redirectPath = user.role === 'admin' ? '/admin/dashboard' : '/user/dashboard'
          
          // Small delay to show success message
          setTimeout(() => {
            router.push(redirectPath)
          }, 500)
          
        } else {
          throw new Error(response.data.message || 'Login failed')
        }
        
      } catch (err) {
        console.error('❌ Login error:', err)
        
        const errorMessage = err.response?.data?.message || 
                           err.message || 
                           'Login failed. Please check your credentials and try again.'
        
        error.value = errorMessage
        
        // Show global notification
        if (window.app?.showNotification) {
          window.app.showNotification(errorMessage, 'error')
        }
        
        // Clear password on error
        form.value.password = ''
        
      } finally {
        loading.value = false
        
        // Hide global loading
        if (window.app?.setGlobalLoading) {
          window.app.setGlobalLoading(false)
        }
      }
    }
    
    // Lifecycle
    onMounted(() => {
      // Check if already authenticated
      if (authHelpers.isAuthenticated()) {
        const user = authHelpers.getCurrentUser()
        if (user) {
          console.log('👤 Already authenticated, redirecting...')
          const redirectPath = user.role === 'admin' ? '/admin/dashboard' : '/user/dashboard'
          router.push(redirectPath)
        }
      }
      
      // Focus username field
      setTimeout(() => {
        const usernameInput = document.getElementById('username')
        if (usernameInput) {
          usernameInput.focus()
        }
      }, 100)
    })
    
    return {
      form,
      loading,
      error,
      showPassword,
      validationErrors,
      isFormValid,
      handleLogin,
      togglePasswordVisibility,
      fillDemoCredentials,
      clearFieldError
    }
  }
}
</script>

<style scoped>
.login-form {
  padding: 2rem;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;
}

.form-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  margin: 0 0 0.5rem 0;
}

.form-header p {
  color: #666;
  font-size: 0.95rem;
  margin: 0;
}

.auth-form {
  max-width: 100%;
}

.error-alert {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
}

.error-content {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.error-icon {
  width: 20px;
  height: 20px;
  color: #ef4444;
  flex-shrink: 0;
  margin-top: 2px;
}

.error-content p {
  color: #dc2626;
  font-size: 0.9rem;
  margin: 0;
  line-height: 1.4;
}

.password-input-container {
  position: relative;
}

.password-toggle {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #374151;
}

.password-toggle:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.password-icon {
  width: 20px;
  height: 20px;
}

.login-button {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.875rem 1.5rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.login-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.auth-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #666;
}

.auth-link .link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  margin-left: 0.25rem;
  transition: color 0.2s ease;
}

.auth-link .link:hover {
  color: #5a6fd8;
  text-decoration: underline;
}

.demo-credentials {
  margin-top: 1.5rem;
  background: #fffbeb;
  border: 1px solid #fed7aa;
  border-radius: 8px;
  padding: 1rem;
}

.demo-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.demo-icon {
  width: 18px;
  height: 18px;
  color: #d97706;
}

.demo-header h3 {
  font-size: 0.9rem;
  font-weight: 600;
  color: #92400e;
  margin: 0;
}

.demo-content {
  font-size: 0.85rem;
  color: #b45309;
}

.demo-account {
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.25rem;
  transition: background 0.2s ease;
}

.demo-account:hover {
  background: rgba(217, 119, 6, 0.1);
}

.demo-hint {
  font-size: 0.75rem;
  color: #a16207;
  margin: 0.5rem 0 0 0;
  font-style: italic;
}

/* Form validation improvements */
.form-input.error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

.form-error {
  color: #ef4444;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

/* Responsive design */
@media (max-width: 480px) {
  .login-form {
    padding: 1.5rem;
  }
  
  .form-header h2 {
    font-size: 1.5rem;
  }
}

/* Animation for error clearing */
.error-alert {
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 