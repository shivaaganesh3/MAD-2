<template>
  <div class="login-form">
    <!-- Header -->
    <div class="text-center mb-4">
      <h2 class="fw-bold text-dark mb-2">Welcome Back</h2>
      <p class="text-muted">Sign in to your account</p>
    </div>

    <!-- Login Form -->
    <form @submit.prevent="handleLogin">
      <!-- Error Alert -->
      <div v-if="error" class="alert alert-danger d-flex align-items-center mb-4" role="alert">
        <i class="fas fa-exclamation-circle me-2"></i>
        <div>{{ error }}</div>
      </div>

      <div class="row g-3">
        <!-- Form Fields -->
        <div class="col-12">
          <label for="username" class="form-label fw-medium">
            <i class="fas fa-user me-1"></i>Username
          </label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            :disabled="loading"
            class="form-control form-control-lg"
            :class="{ 'is-invalid': validationErrors.username }"
            placeholder="Enter your username"
            @input="clearFieldError('username')"
          />
          <div v-if="validationErrors.username" class="invalid-feedback">
            {{ validationErrors.username }}
          </div>
        </div>

        <div class="col-12">
          <label for="password" class="form-label fw-medium">
            <i class="fas fa-lock me-1"></i>Password
          </label>
          <div class="input-group input-group-lg">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              required
              :disabled="loading"
              class="form-control"
              :class="{ 'is-invalid': validationErrors.password }"
              placeholder="Enter your password"
              @input="clearFieldError('password')"
            />
            <button
              type="button"
              @click="togglePasswordVisibility"
              class="btn btn-outline-secondary"
              :disabled="loading"
              :title="showPassword ? 'Hide password' : 'Show password'"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <div v-if="validationErrors.password" class="invalid-feedback d-block">
            {{ validationErrors.password }}
          </div>
        </div>
      </div>

      <!-- Login Button -->
      <button
        type="submit"
        :disabled="loading || !isFormValid"
        class="btn btn-primary w-100 py-3 fw-medium mt-4 btn-lg"
      >
        <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
        <i v-else class="fas fa-sign-in-alt me-2"></i>
        {{ loading ? 'Signing in...' : 'Sign in' }}
      </button>

      <!-- Register Link -->
      <div class="text-center mt-4">
        <span class="text-muted">Don't have an account?</span>
        <router-link to="/auth/register" class="text-decoration-none ms-1">
          <strong>Sign up here</strong>
        </router-link>
      </div>
    </form>


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
      clearFieldError
    }
  }
}
</script>

<style scoped>
.login-form {
  padding: 2.5rem;
}

/* Enhanced button hover effects */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  border: none;
}

.btn-primary:disabled {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  opacity: 0.6;
}



/* Form enhancements */
.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.input-group .btn:focus {
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}



/* Responsive design */
@media (max-width: 480px) {
  .login-form {
    padding: 2rem;
  }
}

/* Animation for error clearing */
.alert {
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