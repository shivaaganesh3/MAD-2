<template>
  <div class="register-form">
    <!-- Header -->
    <div class="text-center mb-4">
      <div class="d-inline-flex align-items-center justify-content-center bg-primary rounded-circle mb-3" style="width: 60px; height: 60px;">
        <i class="fas fa-user-plus text-white fs-4"></i>
      </div>
      <h2 class="fw-bold text-dark mb-2">Create your account</h2>
      <p class="text-muted">Join our parking system</p>
    </div>

    <!-- Registration Form -->
    <form @submit.prevent="handleRegister">
      <!-- Error Alert -->
      <div v-if="error" class="alert alert-danger d-flex align-items-center mb-4" role="alert">
        <i class="fas fa-exclamation-circle me-2"></i>
        <div>{{ error }}</div>
      </div>

      <div class="row g-4">
        <!-- Username -->
        <div class="col-md-6">
          <label for="username" class="form-label fw-medium">
            <i class="fas fa-user me-1"></i>Username *
          </label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            class="form-control form-control-lg"
            placeholder="Choose a username"
            :disabled="loading"
          />
        </div>

        <!-- Email -->
        <div class="col-md-6">
          <label for="email" class="form-label fw-medium">
            <i class="fas fa-envelope me-1"></i>Email *
          </label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            class="form-control form-control-lg"
            placeholder="your@email.com"
            :disabled="loading"
          />
        </div>

        <!-- Full Name -->
        <div class="col-12">
          <label for="full_name" class="form-label fw-medium">
            <i class="fas fa-id-card me-1"></i>Full Name *
          </label>
          <input
            id="full_name"
            v-model="form.full_name"
            type="text"
            required
            class="form-control form-control-lg"
            placeholder="Your full name"
            :disabled="loading"
          />
        </div>

        <!-- Phone Number -->
        <div class="col-md-6">
          <label for="phone_number" class="form-label fw-medium">
            <i class="fas fa-phone me-1"></i>Phone Number *
          </label>
          <input
            id="phone_number"
            v-model="form.phone_number"
            type="tel"
            required
            class="form-control form-control-lg"
            placeholder="Your phone number"
            :disabled="loading"
          />
        </div>

        <!-- Address -->
        <div class="col-md-6">
          <label for="address" class="form-label fw-medium">
            <i class="fas fa-map-marker-alt me-1"></i>Address
          </label>
          <input
            id="address"
            v-model="form.address"
            type="text"
            class="form-control form-control-lg"
            placeholder="Your address (optional)"
            :disabled="loading"
          />
        </div>

        <!-- Password -->
        <div class="col-md-6">
          <label for="password" class="form-label fw-medium">
            <i class="fas fa-lock me-1"></i>Password *
          </label>
          <div class="input-group input-group-lg">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              required
              class="form-control"
              placeholder="Create a strong password"
              :disabled="loading"
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
        </div>

        <!-- Confirm Password -->
        <div class="col-md-6">
          <label for="confirm_password" class="form-label fw-medium">
            <i class="fas fa-lock me-1"></i>Confirm Password *
          </label>
          <div class="input-group input-group-lg">
            <input
              id="confirm_password"
              v-model="form.confirm_password"
              :type="showConfirmPassword ? 'text' : 'password'"
              required
              class="form-control"
              placeholder="Confirm your password"
              :disabled="loading"
            />
            <button
              type="button"
              @click="toggleConfirmPasswordVisibility"
              class="btn btn-outline-secondary"
              :disabled="loading"
              :title="showConfirmPassword ? 'Hide password' : 'Show password'"
            >
              <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- Register Button -->
      <button
        type="submit"
        :disabled="loading"
        class="btn btn-primary w-100 py-3 fw-medium mt-4 btn-lg"
      >
        <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
        <i v-else class="fas fa-user-plus me-2"></i>
        {{ loading ? 'Creating account...' : 'Create account' }}
      </button>

      <!-- Login Link -->
      <div class="text-center mt-4">
        <span class="text-muted">Already have an account?</span>
        <router-link to="/auth/login" class="text-decoration-none ms-1">
          <strong>Sign in here</strong>
        </router-link>
      </div>
    </form>

    <!-- Registration Tips -->
    <div class="card mt-4 border-info bg-info-subtle">
      <div class="card-header bg-info text-white d-flex align-items-center">
        <i class="fas fa-lightbulb me-2"></i>
        <strong class="mb-0">Registration Tips</strong>
      </div>
      <div class="card-body p-4">
        <div class="row g-3">
          <div class="col-md-6">
            <div class="d-flex align-items-start">
              <i class="fas fa-check-circle text-success me-2 mt-1"></i>
              <div>
                <small class="fw-medium">Username Guidelines</small>
                <div class="small text-muted">Choose a unique username (3-20 characters)</div>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="d-flex align-items-start">
              <i class="fas fa-envelope text-primary me-2 mt-1"></i>
              <div>
                <small class="fw-medium">Email Verification</small>
                <div class="small text-muted">Use a valid email for account verification</div>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="d-flex align-items-start">
              <i class="fas fa-shield-alt text-warning me-2 mt-1"></i>
              <div>
                <small class="fw-medium">Strong Password</small>
                <div class="small text-muted">Create a password with at least 8 characters</div>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="d-flex align-items-start">
              <i class="fas fa-phone text-info me-2 mt-1"></i>
              <div>
                <small class="fw-medium">Phone Notifications</small>
                <div class="small text-muted">Used for important parking updates</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../../services/api'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    
    const form = ref({
      username: '',
      email: '',
      full_name: '',
      phone_number: '',
      address: '',
      password: '',
      confirm_password: ''
    })
    
    const loading = ref(false)
    const error = ref('')
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    
    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }
    
    const toggleConfirmPasswordVisibility = () => {
      showConfirmPassword.value = !showConfirmPassword.value
    }
    
    const handleRegister = async () => {
      try {
        loading.value = true
        error.value = ''

        // Validate passwords match
        if (form.value.password !== form.value.confirm_password) {
          error.value = 'Passwords do not match'
          return
        }

        // Remove confirm_password from request
        const { confirm_password, ...userData } = form.value
        
        console.log('🔐 Attempting registration for:', userData.username)
        
        // Show global loading
        if (window.app?.setGlobalLoading) {
          window.app.setGlobalLoading(true)
        }
        
        const response = await authAPI.register(userData)
        
        if (response.data.success) {
          console.log('✅ Registration successful')
          
          // Show success notification
          if (window.app?.showNotification) {
            window.app.showNotification(
              'Account created successfully! Please login to continue.',
              'success'
            )
          }
          
          // Redirect to login with a small delay
          setTimeout(() => {
            router.push('/auth/login')
          }, 1000)
        } else {
          throw new Error(response.data.message || 'Registration failed')
        }
      } catch (err) {
        console.error('❌ Registration error:', err)
        
        let errorMessage = 'Registration failed. Please try again.'
        
        if (err.response?.data?.errors) {
          errorMessage = err.response.data.errors.join(', ')
        } else if (err.response?.data?.message) {
          errorMessage = err.response.data.message
        } else if (err.message) {
          errorMessage = err.message
        }
        
        error.value = errorMessage
        
        // Show global notification
        if (window.app?.showNotification) {
          window.app.showNotification(errorMessage, 'error')
        }
      } finally {
        loading.value = false
        
        // Hide global loading
        if (window.app?.setGlobalLoading) {
          window.app.setGlobalLoading(false)
        }
      }
    }
    
    return {
      form,
      loading,
      error,
      showPassword,
      showConfirmPassword,
      togglePasswordVisibility,
      toggleConfirmPasswordVisibility,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-form {
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

/* Card hover effect */
.card {
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

/* Enhanced tips layout */
.card-body .small {
  line-height: 1.3;
}

/* Responsive design */
@media (max-width: 480px) {
  .register-form {
    padding: 2rem;
  }
  
  .row.g-4 {
    gap: 1.5rem !important;
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