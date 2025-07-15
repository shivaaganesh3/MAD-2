<template>
  <div class="user-dashboard">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom">
      <div>
        <h1 class="h3 mb-1 fw-bold text-dark">
          <i class="fas fa-tachometer-alt me-2 text-primary"></i>User Dashboard
        </h1>
        <p class="text-muted mb-0">Welcome back, {{ userInfo?.full_name || 'User' }}!</p>
      </div>
      <div class="d-flex align-items-center gap-2">
        <span class="badge bg-primary-subtle text-primary px-3 py-2">
          <i class="fas fa-user me-1"></i>{{ currentUser?.username }}
        </span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary mb-3" style="width: 3rem; height: 3rem;" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-muted">Loading dashboard data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-danger d-flex align-items-center" role="alert">
      <i class="fas fa-exclamation-triangle me-3 fs-4"></i>
      <div class="flex-fill">
        <h5 class="alert-heading mb-1">Unable to load dashboard</h5>
        <p class="mb-2">{{ error }}</p>
        <button @click="loadDashboard" class="btn btn-outline-danger btn-sm">
          <i class="fas fa-redo me-1"></i>Retry
        </button>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- User Statistics Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-6 col-xl-3">
          <div class="card border-0 shadow-sm h-100 stat-card bg-primary text-white">
            <div class="card-body d-flex align-items-center">
              <div class="flex-fill">
                <h3 class="mb-1 fw-bold">{{ userStats?.total_reservations || 0 }}</h3>
                <p class="mb-0 opacity-75">Total Reservations</p>
              </div>
              <div class="stat-icon">
                <i class="fas fa-car fa-2x opacity-75"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-xl-3">
          <div class="card border-0 shadow-sm h-100 stat-card bg-success text-white">
            <div class="card-body d-flex align-items-center">
              <div class="flex-fill">
                <h3 class="mb-1 fw-bold">{{ userStats?.completed_reservations || 0 }}</h3>
                <p class="mb-0 opacity-75">Completed</p>
              </div>
              <div class="stat-icon">
                <i class="fas fa-check-circle fa-2x opacity-75"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-xl-3">
          <div class="card border-0 shadow-sm h-100 stat-card bg-warning text-white">
            <div class="card-body d-flex align-items-center">
              <div class="flex-fill">
                <h3 class="mb-1 fw-bold">{{ userStats?.active_reservations || 0 }}</h3>
                <p class="mb-0 opacity-75">Active</p>
              </div>
              <div class="stat-icon">
                <i class="fas fa-clock fa-2x opacity-75"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-xl-3">
          <div class="card border-0 shadow-sm h-100 stat-card bg-danger text-white">
            <div class="card-body d-flex align-items-center">
              <div class="flex-fill">
                <h3 class="mb-1 fw-bold">{{ userStats?.cancelled_reservations || 0 }}</h3>
                <p class="mb-0 opacity-75">Cancelled</p>
              </div>
              <div class="stat-icon">
                <i class="fas fa-times-circle fa-2x opacity-75"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Reservation Alert -->
      <div v-if="activeReservation" class="alert alert-info border-0 shadow-sm mb-4" role="alert">
        <div class="d-flex align-items-start">
          <div class="me-3">
            <i class="fas fa-parking fa-2x text-info"></i>
          </div>
          <div class="flex-fill">
            <h5 class="alert-heading mb-2">
              <i class="fas fa-circle text-success me-2" style="font-size: 0.5rem;"></i>
              Active Parking Session
            </h5>
            <div class="row align-items-center">
              <div class="col-lg-8">
                <p class="mb-2">
                  <strong class="text-dark">{{ activeReservation.lot_name }}</strong>
                  <span class="badge bg-info-subtle text-info ms-2">Spot {{ activeReservation.spot_number }}</span>
                </p>
                <div class="small text-muted mb-2">
                  <div class="d-flex flex-wrap gap-3">
                    <span><i class="fas fa-car me-1"></i>{{ activeReservation.vehicle_number }}</span>
                    <span><i class="fas fa-clock me-1"></i>{{ formatDuration(activeReservation.duration_minutes) }}</span>
                    <span><i class="fas fa-rupee-sign me-1"></i>{{ activeReservation.current_cost_estimate }}</span>
                  </div>
                </div>
                <p class="mb-0 small text-muted">
                  <i class="fas fa-calendar-alt me-1"></i>Started: {{ formatDateTime(activeReservation.parking_timestamp) }}
                </p>
              </div>
              <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
                <button 
                  @click="releaseSpot(activeReservation.id)" 
                  class="btn btn-success btn-lg px-4"
                  :disabled="releasingSpot"
                >
                  <span v-if="releasingSpot" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="fas fa-sign-out-alt me-2"></i>
                  {{ releasingSpot ? 'Releasing...' : 'Release Spot' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <!-- Available Parking Lots -->
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center py-3">
              <h5 class="mb-0 fw-bold">
                <i class="fas fa-map-marker-alt me-2 text-primary"></i>Available Parking Lots
              </h5>
              <router-link to="/user/parking-lots" class="btn btn-primary btn-sm">
                <i class="fas fa-external-link-alt me-1"></i>View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="availableLots.length === 0" class="text-center py-5">
                <i class="fas fa-info-circle text-muted fa-3x mb-3"></i>
                <h6 class="text-muted">No Available Parking</h6>
                <p class="text-muted mb-0">All parking lots are currently full. Please check back later.</p>
              </div>
              <div v-else class="parking-lots-list">
                <div 
                  v-for="(lot, index) in availableLots.slice(0, 3)" 
                  :key="lot.id" 
                  class="parking-lot-item p-3 rounded"
                  :class="{'border-bottom': index < Math.min(availableLots.length, 3) - 1}"
                >
                  <div class="d-flex justify-content-between align-items-center">
                    <div class="flex-fill">
                      <h6 class="mb-1 fw-bold">{{ lot.name }}</h6>
                      <p class="text-muted mb-2 small">
                        <i class="fas fa-map-marker-alt me-1"></i>{{ lot.address }}
                      </p>
                      <div class="d-flex align-items-center gap-3">
                        <span class="badge bg-success-subtle text-success px-2 py-1">
                          <i class="fas fa-parking me-1"></i>{{ lot.available_spots }} available
                        </span>
                        <span class="fw-bold text-primary">
                          <i class="fas fa-rupee-sign me-1"></i>{{ lot.price_per_hour }}/hour
                        </span>
                      </div>
                    </div>
                    <div class="ms-3">
                      <button 
                        @click="quickReserve(lot)" 
                        class="btn btn-primary"
                        :disabled="activeReservation || reservingLot === lot.id"
                      >
                        <span v-if="reservingLot === lot.id" class="spinner-border spinner-border-sm me-2"></span>
                        <i v-else class="fas fa-plus me-2"></i>
                        {{ reservingLot === lot.id ? 'Reserving...' : 'Quick Reserve' }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Reservations -->
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center py-3">
              <h5 class="mb-0 fw-bold">
                <i class="fas fa-history me-2 text-primary"></i>Recent Activity
              </h5>
              <router-link to="/user/history" class="btn btn-outline-primary btn-sm">
                <i class="fas fa-external-link-alt me-1"></i>View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="recentReservations.length === 0" class="text-center py-4">
                <i class="fas fa-history text-muted fa-2x mb-3"></i>
                <h6 class="text-muted">No Recent Activity</h6>
                <p class="text-muted mb-0 small">Your recent reservations will appear here.</p>
              </div>
              <div v-else class="recent-reservations">
                <div 
                  v-for="(reservation, index) in recentReservations.slice(0, 5)" 
                  :key="reservation.id"
                  class="reservation-item p-2 rounded"
                  :class="{'border-bottom': index < Math.min(recentReservations.length, 5) - 1}"
                >
                  <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-fill">
                      <h6 class="mb-1 small fw-medium">{{ reservation.lot_name }}</h6>
                      <p class="mb-1 small text-muted">
                        <i class="fas fa-parking me-1"></i>Spot {{ reservation.spot_number }}
                      </p>
                      <small class="text-muted">
                        <i class="fas fa-calendar me-1"></i>{{ formatDateTime(reservation.parking_timestamp) }}
                      </small>
                    </div>
                    <div class="text-end">
                      <span :class="getStatusBadgeClass(reservation.status)" class="badge small">
                        {{ getStatusText(reservation.status) }}
                      </span>
                      <div v-if="reservation.parking_cost" class="fw-bold text-success small mt-1">
                        <i class="fas fa-rupee-sign"></i>{{ reservation.parking_cost }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Reserve Modal -->
    <div v-if="showReserveModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0, 0, 0, 0.5);" @click.self="closeReserveModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow">
          <div class="modal-header border-0 pb-0">
            <h5 class="modal-title fw-bold">
              <i class="fas fa-parking me-2 text-primary"></i>Reserve Parking Spot
            </h5>
            <button @click="closeReserveModal" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <div class="alert alert-info border-0 bg-info-subtle">
              <div class="d-flex align-items-center">
                <i class="fas fa-info-circle me-2"></i>
                <div>
                  <strong>{{ selectedLot?.name }}</strong>
                  <div class="small text-muted">{{ selectedLot?.address }}</div>
                </div>
              </div>
            </div>
            
            <form @submit.prevent="confirmReservation">
              <div class="mb-3">
                <label for="vehicleNumber" class="form-label fw-medium">
                  <i class="fas fa-car me-1"></i>Vehicle Number *
                </label>
                <input 
                  type="text" 
                  class="form-control form-control-lg" 
                  id="vehicleNumber"
                  v-model="reservationForm.vehicle_number"
                  placeholder="Enter vehicle number (e.g., KA01AB1234)"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="vehicleModel" class="form-label fw-medium">
                  <i class="fas fa-car-side me-1"></i>Vehicle Model (Optional)
                </label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="vehicleModel"
                  v-model="reservationForm.vehicle_model"
                  placeholder="Enter vehicle model (e.g., Honda City)"
                >
              </div>
            </form>
          </div>
          <div class="modal-footer border-0 pt-0">
            <button @click="closeReserveModal" class="btn btn-light">Cancel</button>
            <button 
              @click="confirmReservation" 
              class="btn btn-primary px-4"
              :disabled="!reservationForm.vehicle_number || reservingLot"
            >
              <span v-if="reservingLot" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="fas fa-check me-2"></i>
              {{ reservingLot ? 'Reserving...' : 'Confirm Reservation' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { dashboardAPI, userAPI, authAPI, authHelpers } from '../../services/api'

export default {
  name: 'UserDashboard',
  setup() {
    const router = useRouter()
    
    // Reactive data
    const loading = ref(true)
    const error = ref('')
    const userInfo = ref(null)
    const userStats = ref(null)
    const activeReservation = ref(null)
    const availableLots = ref([])
    const recentReservations = ref([])
    
    // Modal and form state
    const showReserveModal = ref(false)
    const selectedLot = ref(null)
    const reservationForm = ref({
      vehicle_number: '',
      vehicle_model: ''
    })
    const reservingLot = ref(null)
    const releasingSpot = ref(false)

    // Computed properties
    const currentUser = computed(() => authHelpers.getCurrentUser())

    // Load dashboard data
    const loadDashboard = async () => {
      try {
        loading.value = true
        error.value = ''
        
        const response = await dashboardAPI.getUserDashboard()
        const data = response.data.data
        
        userInfo.value = data.user_info
        userStats.value = data.user_stats
        activeReservation.value = data.active_reservation
        availableLots.value = data.available_lots || []
        recentReservations.value = data.recent_reservations || []
        
      } catch (err) {
        console.error('Error loading dashboard:', err)
        error.value = err.response?.data?.message || 'Failed to load dashboard data'
      } finally {
        loading.value = false
      }
    }

    // Quick reserve functionality
    const quickReserve = (lot) => {
      if (activeReservation.value) {
        alert('You already have an active reservation')
        return
      }
      
      selectedLot.value = lot
      showReserveModal.value = true
      reservationForm.value = { vehicle_number: '', vehicle_model: '' }
    }

    const closeReserveModal = () => {
      showReserveModal.value = false
      selectedLot.value = null
      reservationForm.value = { vehicle_number: '', vehicle_model: '' }
    }

    const confirmReservation = async () => {
      try {
        console.log('Dashboard - Starting reservation confirmation...')
        console.log('Dashboard - Selected lot:', selectedLot.value)
        console.log('Dashboard - Reservation form:', reservationForm.value)
        
        if (!selectedLot.value) {
          alert('No parking lot selected. Please try again.')
          return
        }
        
        if (!reservationForm.value.vehicle_number?.trim()) {
          alert('Please enter a vehicle number.')
          return
        }
        
        reservingLot.value = selectedLot.value.id
        
        const reservationData = {
          lot_id: selectedLot.value.id,
          vehicle_number: reservationForm.value.vehicle_number.trim().toUpperCase(),
          vehicle_model: reservationForm.value.vehicle_model.trim() || undefined
        }
        
        console.log('Dashboard - Sending reservation data:', reservationData)
        
        const response = await userAPI.createReservation(reservationData)
        
        console.log('Dashboard - Reservation response:', response.data)
        alert('Parking spot reserved successfully!')
        closeReserveModal()
        loadDashboard() // Refresh dashboard data
        
      } catch (err) {
        console.error('Dashboard - Error creating reservation:', err)
        console.error('Dashboard - Error details:', err.response)
        alert(err.response?.data?.message || 'Failed to create reservation')
      } finally {
        reservingLot.value = null
      }
    }

    // Release spot functionality
    const releaseSpot = async (reservationId) => {
      if (!confirm('Are you sure you want to release this parking spot?')) {
        return
      }
      
      try {
        releasingSpot.value = true
        
        const response = await userAPI.releaseSpot(reservationId)
        const data = response.data.data
        
        alert(`Parking spot released successfully! Final cost: ₹${data.final_cost}`)
        loadDashboard() // Refresh dashboard data
        
      } catch (err) {
        console.error('Error releasing spot:', err)
        alert(err.response?.data?.message || 'Failed to release parking spot')
      } finally {
        releasingSpot.value = false
      }
    }

    // Logout functionality
    const logout = async () => {
      try {
        await authAPI.logout()
        router.push('/login')
      } catch (err) {
        console.error('Logout error:', err)
        router.push('/login')
      }
    }

    // Utility functions
    const formatDateTime = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString()
    }

    const formatDuration = (minutes) => {
      if (!minutes) return '0 minutes'
      const hours = Math.floor(minutes / 60)
      const mins = Math.floor(minutes % 60)
      
      if (hours > 0) {
        return `${hours}h ${mins}m`
      }
      return `${mins}m`
    }

    const getStatusBadgeClass = (status) => {
      const classes = {
        'active': 'bg-warning-subtle text-warning',
        'completed': 'bg-success-subtle text-success',
        'cancelled': 'bg-danger-subtle text-danger'
      }
      return classes[status] || 'bg-secondary-subtle text-secondary'
    }

    const getStatusText = (status) => {
      const texts = {
        'active': 'Active',
        'completed': 'Completed',
        'cancelled': 'Cancelled'
      }
      return texts[status] || 'Unknown'
    }

    // Load data on component mount
    onMounted(() => {
      loadDashboard()
    })

    return {
      loading,
      error,
      userInfo,
      userStats,
      activeReservation,
      availableLots,
      recentReservations,
      showReserveModal,
      selectedLot,
      reservationForm,
      reservingLot,
      releasingSpot,
      currentUser,
      loadDashboard,
      quickReserve,
      closeReserveModal,
      confirmReservation,
      releaseSpot,
      logout,
      formatDateTime,
      formatDuration,
      getStatusBadgeClass,
      getStatusText
    }
  }
}
</script>

<style scoped>
/* Custom stat card styling */
.stat-card {
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  opacity: 0.8;
}

/* Enhanced card styling */
.card {
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}

/* Parking lot item hover effect */
.parking-lot-item:hover {
  background-color: #f8f9fa;
}

.reservation-item:hover {
  background-color: #f8f9fa;
}

/* Modal backdrop */
.modal {
  backdrop-filter: blur(4px);
}

/* Custom focus styles */
.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .parking-lot-item .d-flex {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 0.75rem;
  }
  
  .parking-lot-item .ms-3 {
    margin-left: 0 !important;
    width: 100%;
  }
  
  .parking-lot-item .btn {
    width: 100%;
  }
}

/* Badge enhancements */
.badge {
  font-weight: 500;
}

/* Border utilities */
.border-bottom:last-child {
  border-bottom: none !important;
}
</style> 