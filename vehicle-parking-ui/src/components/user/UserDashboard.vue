<template>
  <div class="user-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">User Dashboard</h1>
      <div class="user-info">
        <span class="welcome-text">Welcome, {{ userInfo?.full_name || 'User' }}!</span>
        <button @click="logout" class="btn btn-outline-danger btn-sm">
          <i class="fas fa-sign-out-alt"></i> Logout
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading dashboard data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="fas fa-exclamation-triangle"></i>
      {{ error }}
      <button @click="loadDashboard" class="btn btn-sm btn-outline-danger ms-2">
        <i class="fas fa-refresh"></i> Retry
      </button>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- User Statistics -->
      <div class="row mb-4">
        <div class="col-md-3">
          <div class="stats-card bg-primary">
            <div class="stats-content">
              <h3>{{ userStats?.total_reservations || 0 }}</h3>
              <p>Total Reservations</p>
            </div>
            <i class="fas fa-car stats-icon"></i>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stats-card bg-success">
            <div class="stats-content">
              <h3>{{ userStats?.completed_reservations || 0 }}</h3>
              <p>Completed</p>
            </div>
            <i class="fas fa-check-circle stats-icon"></i>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stats-card bg-warning">
            <div class="stats-content">
              <h3>{{ userStats?.active_reservations || 0 }}</h3>
              <p>Active</p>
            </div>
            <i class="fas fa-clock stats-icon"></i>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stats-card bg-danger">
            <div class="stats-content">
              <h3>{{ userStats?.cancelled_reservations || 0 }}</h3>
              <p>Cancelled</p>
            </div>
            <i class="fas fa-times-circle stats-icon"></i>
          </div>
        </div>
      </div>

      <!-- Active Reservation Alert -->
      <div v-if="activeReservation" class="alert alert-info active-reservation-alert mb-4">
        <div class="row align-items-center">
          <div class="col-md-8">
            <h5 class="alert-heading">
              <i class="fas fa-parking"></i> Active Parking Session
            </h5>
            <p class="mb-1">
              <strong>{{ activeReservation.lot_name }}</strong> - Spot {{ activeReservation.spot_number }}
            </p>
            <p class="mb-1">
              <small>Vehicle: {{ activeReservation.vehicle_number }} | 
              Duration: {{ formatDuration(activeReservation.duration_minutes) }} | 
              Current Cost: ₹{{ activeReservation.current_cost_estimate }}</small>
            </p>
            <p class="mb-0">
              <small>Started: {{ formatDateTime(activeReservation.parking_timestamp) }}</small>
            </p>
          </div>
          <div class="col-md-4 text-end">
            <button 
              @click="releaseSpot(activeReservation.id)" 
              class="btn btn-success"
              :disabled="releasingSpot"
            >
              <i class="fas fa-sign-out-alt"></i>
              {{ releasingSpot ? 'Releasing...' : 'Release Spot' }}
            </button>
          </div>
        </div>
      </div>

      <div class="row">
        <!-- Available Parking Lots -->
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">
                <i class="fas fa-map-marker-alt"></i> Available Parking Lots
              </h5>
              <router-link to="/user/parking-lots" class="btn btn-sm btn-primary">
                View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="availableLots.length === 0" class="text-center py-4">
                <i class="fas fa-info-circle text-muted"></i>
                <p class="text-muted">No parking lots with available spots</p>
              </div>
              <div v-else class="parking-lots-list">
                <div 
                  v-for="lot in availableLots.slice(0, 3)" 
                  :key="lot.id" 
                  class="parking-lot-item"
                >
                  <div class="lot-info">
                    <h6>{{ lot.name }}</h6>
                    <p class="text-muted mb-1">{{ lot.address }}</p>
                    <div class="lot-details">
                      <span class="badge bg-success">{{ lot.available_spots }} available</span>
                      <span class="price">₹{{ lot.price_per_hour }}/hour</span>
                    </div>
                  </div>
                  <div class="lot-actions">
                    <button 
                      @click="quickReserve(lot)" 
                      class="btn btn-sm btn-primary"
                      :disabled="activeReservation || reservingLot === lot.id"
                    >
                      <i class="fas fa-plus"></i>
                      {{ reservingLot === lot.id ? 'Reserving...' : 'Quick Reserve' }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Reservations -->
        <div class="col-lg-4">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">
                <i class="fas fa-history"></i> Recent Activity
              </h5>
              <router-link to="/user/history" class="btn btn-sm btn-outline-primary">
                View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="recentReservations.length === 0" class="text-center py-4">
                <i class="fas fa-info-circle text-muted"></i>
                <p class="text-muted">No recent reservations</p>
              </div>
              <div v-else class="recent-reservations">
                <div 
                  v-for="reservation in recentReservations.slice(0, 5)" 
                  :key="reservation.id"
                  class="reservation-item"
                >
                  <div class="reservation-info">
                    <h6>{{ reservation.lot_name }}</h6>
                    <p class="mb-1">Spot {{ reservation.spot_number }}</p>
                    <small class="text-muted">{{ formatDateTime(reservation.parking_timestamp) }}</small>
                  </div>
                  <div class="reservation-status">
                    <span :class="getStatusBadgeClass(reservation.status)">
                      {{ getStatusText(reservation.status) }}
                    </span>
                    <div v-if="reservation.parking_cost" class="cost">
                      ₹{{ reservation.parking_cost }}
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
    <div v-if="showReserveModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reserve Parking Spot</h5>
            <button @click="closeReserveModal" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="confirmReservation">
              <div class="mb-3">
                <label class="form-label">Parking Lot</label>
                <p class="form-text">{{ selectedLot?.name }} - {{ selectedLot?.address }}</p>
              </div>
              <div class="mb-3">
                <label for="vehicleNumber" class="form-label">Vehicle Number *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="vehicleNumber"
                  v-model="reservationForm.vehicle_number"
                  placeholder="Enter vehicle number"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="vehicleModel" class="form-label">Vehicle Model (Optional)</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="vehicleModel"
                  v-model="reservationForm.vehicle_model"
                  placeholder="Enter vehicle model"
                >
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button @click="closeReserveModal" class="btn btn-secondary">Cancel</button>
            <button 
              @click="confirmReservation" 
              class="btn btn-primary"
              :disabled="!reservationForm.vehicle_number || reservingLot"
            >
              {{ reservingLot ? 'Reserving...' : 'Confirm Reservation' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showReserveModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { dashboardAPI, userAPI, authAPI } from '../../services/api'

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
        reservingLot.value = selectedLot.value.id
        
        const reservationData = {
          lot_id: selectedLot.value.id,
          vehicle_number: reservationForm.value.vehicle_number.trim().toUpperCase(),
          vehicle_model: reservationForm.value.vehicle_model.trim() || undefined
        }
        
        const response = await userAPI.createReservation(reservationData)
        
        alert('Parking spot reserved successfully!')
        closeReserveModal()
        loadDashboard() // Refresh dashboard data
        
      } catch (err) {
        console.error('Error creating reservation:', err)
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
        'active': 'badge bg-warning',
        'completed': 'badge bg-success',
        'cancelled': 'badge bg-danger'
      }
      return classes[status] || 'badge bg-secondary'
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
.user-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.dashboard-title {
  margin: 0;
  color: #333;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.welcome-text {
  font-weight: 500;
  color: #666;
}

.loading-container {
  text-align: center;
  padding: 50px;
}

.stats-card {
  background: linear-gradient(135deg, var(--bs-primary), var(--bs-primary-dark));
  color: white;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stats-card.bg-success {
  background: linear-gradient(135deg, #28a745, #1e7e34);
}

.stats-card.bg-warning {
  background: linear-gradient(135deg, #ffc107, #d39e00);
}

.stats-card.bg-danger {
  background: linear-gradient(135deg, #dc3545, #bd2130);
}

.stats-content h3 {
  margin: 0;
  font-size: 2rem;
  font-weight: bold;
}

.stats-content p {
  margin: 0;
  opacity: 0.9;
}

.stats-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

.active-reservation-alert {
  border-left: 4px solid #007bff;
}

.parking-lot-item, .reservation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.parking-lot-item:last-child, .reservation-item:last-child {
  border-bottom: none;
}

.lot-info h6, .reservation-info h6 {
  margin: 0 0 5px 0;
  font-weight: 600;
}

.lot-details {
  display: flex;
  gap: 10px;
  align-items: center;
}

.price {
  font-weight: 600;
  color: #007bff;
}

.cost {
  font-weight: 600;
  color: #28a745;
  font-size: 0.9rem;
}

.modal.show {
  animation: fadeIn 0.15s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .parking-lot-item, .reservation-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .lot-actions, .reservation-status {
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }
}
</style> 