<template>
  <div class="parking-history">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1>Parking History</h1>
        <p class="text-muted">View your complete parking reservation history</p>
      </div>
      <div class="header-actions">
        <router-link to="/user/dashboard" class="btn btn-outline-primary">
          <i class="fas fa-arrow-left"></i> Back to Dashboard
        </router-link>
      </div>
    </div>

    <!-- Filters and Stats -->
    <div class="filters-stats mb-4">
      <div class="row">
        <!-- Summary Stats -->
        <div class="col-lg-8">
          <div class="stats-cards">
            <div class="stat-card bg-primary">
              <div class="stat-content">
                <h3>{{ totalReservations }}</h3>
                <p>Total Reservations</p>
              </div>
              <i class="fas fa-car stat-icon"></i>
            </div>
            <div class="stat-card bg-success">
              <div class="stat-content">
                <h3>{{ completedReservations }}</h3>
                <p>Completed</p>
              </div>
              <i class="fas fa-check-circle stat-icon"></i>
            </div>
            <div class="stat-card bg-warning">
              <div class="stat-content">
                <h3>{{ activeReservations }}</h3>
                <p>Active</p>
              </div>
              <i class="fas fa-clock stat-icon"></i>
            </div>
            <div class="stat-card bg-info">
              <div class="stat-content">
                <h3>₹{{ totalSpent }}</h3>
                <p>Total Spent</p>
              </div>
              <i class="fas fa-rupee-sign stat-icon"></i>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="col-lg-4">
          <div class="filter-controls">
            <div class="mb-3">
              <label class="form-label">Filter by Status</label>
              <select class="form-select" v-model="statusFilter" @change="applyFilters">
                <option value="">All Reservations</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <button @click="refreshHistory" class="btn btn-outline-secondary w-100">
              <i class="fas fa-refresh"></i> Refresh
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading reservation history...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="fas fa-exclamation-triangle"></i>
      {{ error }}
      <button @click="loadReservations" class="btn btn-sm btn-outline-danger ms-2">
        <i class="fas fa-refresh"></i> Retry
      </button>
    </div>

    <!-- No Results -->
    <div v-else-if="reservations.length === 0" class="no-results">
      <div class="text-center py-5">
        <i class="fas fa-history text-muted" style="font-size: 3rem;"></i>
        <h4 class="mt-3">No reservations found</h4>
        <p class="text-muted">
          {{ statusFilter ? 'No reservations match the selected filter.' : 'You haven\'t made any reservations yet.' }}
        </p>
        <router-link to="/user/parking-lots" class="btn btn-primary mt-3">
          <i class="fas fa-plus"></i> Make Your First Reservation
        </router-link>
      </div>
    </div>

    <!-- Reservations Table -->
    <div v-else class="reservations-table">
      <div class="table-responsive">
        <table class="table table-hover">
          <thead class="table-light">
            <tr>
              <th>Parking Lot</th>
              <th>Spot</th>
              <th>Vehicle</th>
              <th>Date & Time</th>
              <th>Duration</th>
              <th>Cost</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="reservation in reservations" :key="reservation.id">
              <td>
                <div class="lot-info">
                  <strong>{{ reservation.lot_name }}</strong><br>
                  <small class="text-muted">{{ truncateAddress(reservation.lot_address) }}</small>
                </div>
              </td>
              <td>
                <span class="badge bg-secondary">{{ reservation.spot_number }}</span>
              </td>
              <td>
                <div class="vehicle-info">
                  <strong>{{ reservation.vehicle_number }}</strong>
                  <br v-if="reservation.vehicle_model">
                  <small v-if="reservation.vehicle_model" class="text-muted">{{ reservation.vehicle_model }}</small>
                </div>
              </td>
              <td>
                <div class="time-info">
                  <div>{{ formatDate(reservation.parking_timestamp) }}</div>
                  <small class="text-muted">{{ formatTime(reservation.parking_timestamp) }}</small>
                  <div v-if="reservation.leaving_timestamp" class="text-muted">
                    <small>to {{ formatTime(reservation.leaving_timestamp) }}</small>
                  </div>
                </div>
              </td>
              <td>
                <div class="duration-info">
                  {{ formatDuration(reservation.duration_minutes) }}
                  <div v-if="reservation.status === 'active'" class="text-success">
                    <small><i class="fas fa-clock"></i> Ongoing</small>
                  </div>
                </div>
              </td>
              <td>
                <div class="cost-info">
                  <strong class="text-success">₹{{ reservation.cost || 0 }}</strong>
                  <div v-if="reservation.status === 'active'" class="text-muted">
                    <small>@₹{{ reservation.lot_price_per_hour }}/hr</small>
                  </div>
                </div>
              </td>
              <td>
                <span :class="getStatusBadgeClass(reservation.status)">
                  {{ getStatusText(reservation.status) }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button 
                    @click="viewReservationDetails(reservation)" 
                    class="btn btn-sm btn-outline-primary"
                    title="View Details"
                  >
                    <i class="fas fa-eye"></i>
                  </button>
                  <button 
                    v-if="reservation.status === 'active'" 
                    @click="releaseSpot(reservation.id)"
                    class="btn btn-sm btn-success"
                    :disabled="releasingSpot === reservation.id"
                    title="Release Spot"
                  >
                    <i class="fas fa-sign-out-alt"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="pagination && pagination.pages > 1" class="pagination-container">
      <nav>
        <ul class="pagination justify-content-center">
          <li class="page-item" :class="{ disabled: !pagination.has_prev }">
            <button 
              class="page-link" 
              @click="changePage(pagination.page - 1)"
              :disabled="!pagination.has_prev"
            >
              Previous
            </button>
          </li>
          
          <li 
            v-for="page in getPageNumbers()" 
            :key="page" 
            class="page-item" 
            :class="{ active: page === pagination.page }"
          >
            <button class="page-link" @click="changePage(page)">
              {{ page }}
            </button>
          </li>
          
          <li class="page-item" :class="{ disabled: !pagination.has_next }">
            <button 
              class="page-link" 
              @click="changePage(pagination.page + 1)"
              :disabled="!pagination.has_next"
            >
              Next
            </button>
          </li>
        </ul>
      </nav>
    </div>

    <!-- Reservation Details Modal -->
    <div v-if="showDetailsModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reservation Details</h5>
            <button @click="closeDetailsModal" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <div v-if="selectedReservation" class="reservation-details">
              <div class="row mb-3">
                <div class="col-md-6">
                  <h6>Parking Lot Information</h6>
                  <p><strong>Name:</strong> {{ selectedReservation.lot_name }}</p>
                  <p><strong>Address:</strong> {{ selectedReservation.lot_address }}</p>
                  <p><strong>PIN Code:</strong> {{ selectedReservation.lot_pin_code }}</p>
                  <p><strong>Price:</strong> ₹{{ selectedReservation.lot_price_per_hour }}/hour</p>
                </div>
                <div class="col-md-6">
                  <h6>Reservation Information</h6>
                  <p><strong>Spot Number:</strong> {{ selectedReservation.spot_number }}</p>
                  <p><strong>Status:</strong> 
                    <span :class="getStatusBadgeClass(selectedReservation.status)">
                      {{ getStatusText(selectedReservation.status) }}
                    </span>
                  </p>
                  <p><strong>Vehicle:</strong> {{ selectedReservation.vehicle_number }}</p>
                  <p v-if="selectedReservation.vehicle_model"><strong>Model:</strong> {{ selectedReservation.vehicle_model }}</p>
                </div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <h6>Timing Details</h6>
                  <p><strong>Start Time:</strong><br>{{ formatDateTime(selectedReservation.parking_timestamp) }}</p>
                  <p v-if="selectedReservation.leaving_timestamp">
                    <strong>End Time:</strong><br>{{ formatDateTime(selectedReservation.leaving_timestamp) }}
                  </p>
                  <p v-else class="text-muted"><em>Still ongoing...</em></p>
                </div>
                <div class="col-md-6">
                  <h6>Cost & Duration</h6>
                  <p><strong>Duration:</strong> {{ formatDuration(selectedReservation.duration_minutes) }}</p>
                  <p><strong>Total Cost:</strong> 
                    <span class="text-success">₹{{ selectedReservation.cost || 0 }}</span>
                  </p>
                  <p v-if="selectedReservation.status === 'active'" class="text-info">
                    <small><i class="fas fa-info-circle"></i> Cost is being calculated in real-time</small>
                  </p>
                </div>
              </div>

              <div v-if="selectedReservation.lot_description" class="row">
                <div class="col-12">
                  <h6>Lot Description</h6>
                  <p>{{ selectedReservation.lot_description }}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeDetailsModal" class="btn btn-secondary">Close</button>
            <button 
              v-if="selectedReservation?.status === 'active'" 
              @click="releaseSpot(selectedReservation.id)"
              class="btn btn-success"
              :disabled="releasingSpot === selectedReservation.id"
            >
              <i class="fas fa-sign-out-alt"></i>
              {{ releasingSpot === selectedReservation.id ? 'Releasing...' : 'Release Spot' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showDetailsModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { userAPI, dashboardAPI } from '../../services/api'

export default {
  name: 'ParkingHistory',
  setup() {
    // Reactive data
    const loading = ref(true)
    const error = ref('')
    const reservations = ref([])
    const pagination = ref(null)
    const statusFilter = ref('')
    const currentPage = ref(1)
    
    // Modal state
    const showDetailsModal = ref(false)
    const selectedReservation = ref(null)
    const releasingSpot = ref(null)

    // Load reservations
    const loadReservations = async (page = 1, status = '') => {
      try {
        loading.value = true
        error.value = ''
        
        const params = {
          page,
          per_page: 20,
          status: status.trim()
        }
        
        const response = await userAPI.getReservations(params)
        const data = response.data.data
        
        reservations.value = data.reservations || []
        pagination.value = data.pagination
        currentPage.value = page
        
      } catch (err) {
        console.error('Error loading reservations:', err)
        error.value = err.response?.data?.message || 'Failed to load reservation history'
        reservations.value = []
      } finally {
        loading.value = false
      }
    }

    // Computed stats
    const totalReservations = computed(() => {
      return reservations.value.length
    })

    const completedReservations = computed(() => {
      return reservations.value.filter(r => r.status === 'completed').length
    })

    const activeReservations = computed(() => {
      return reservations.value.filter(r => r.status === 'active').length
    })

    const totalSpent = computed(() => {
      return reservations.value
        .filter(r => r.status === 'completed' && r.cost)
        .reduce((total, r) => total + r.cost, 0)
        .toFixed(2)
    })

    // Filters
    const applyFilters = () => {
      loadReservations(1, statusFilter.value)
    }

    const refreshHistory = () => {
      loadReservations(currentPage.value, statusFilter.value)
    }

    // Pagination
    const changePage = (page) => {
      if (page >= 1 && page <= pagination.value.pages) {
        loadReservations(page, statusFilter.value)
      }
    }

    const getPageNumbers = () => {
      if (!pagination.value) return []
      
      const pages = []
      const total = pagination.value.pages
      const current = pagination.value.page
      
      // Show up to 5 page numbers
      let start = Math.max(1, current - 2)
      let end = Math.min(total, start + 4)
      start = Math.max(1, end - 4)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    }

    // View reservation details
    const viewReservationDetails = async (reservation) => {
      try {
        selectedReservation.value = reservation
        showDetailsModal.value = true
        
        // Optionally load fresh details
        const response = await userAPI.getReservation(reservation.id)
        selectedReservation.value = response.data.data
        
      } catch (err) {
        console.error('Error loading reservation details:', err)
        alert(err.response?.data?.message || 'Failed to load reservation details')
      }
    }

    const closeDetailsModal = () => {
      showDetailsModal.value = false
      selectedReservation.value = null
    }

    // Release spot
    const releaseSpot = async (reservationId) => {
      if (!confirm('Are you sure you want to release this parking spot?')) {
        return
      }
      
      try {
        releasingSpot.value = reservationId
        
        const response = await userAPI.releaseSpot(reservationId)
        const data = response.data.data
        
        alert(`Parking spot released successfully! Final cost: ₹${data.final_cost}`)
        closeDetailsModal()
        loadReservations(currentPage.value, statusFilter.value) // Refresh data
        
      } catch (err) {
        console.error('Error releasing spot:', err)
        alert(err.response?.data?.message || 'Failed to release parking spot')
      } finally {
        releasingSpot.value = null
      }
    }

    // Utility functions
    const formatDateTime = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleString()
    }

    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString()
    }

    const formatTime = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleTimeString()
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

    const truncateAddress = (address, maxLength = 50) => {
      if (!address) return ''
      if (address.length <= maxLength) return address
      return address.substring(0, maxLength) + '...'
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

    // Load data on mount
    onMounted(() => {
      loadReservations()
    })

    return {
      loading,
      error,
      reservations,
      pagination,
      statusFilter,
      currentPage,
      showDetailsModal,
      selectedReservation,
      releasingSpot,
      totalReservations,
      completedReservations,
      activeReservations,
      totalSpent,
      loadReservations,
      applyFilters,
      refreshHistory,
      changePage,
      getPageNumbers,
      viewReservationDetails,
      closeDetailsModal,
      releaseSpot,
      formatDateTime,
      formatDate,
      formatTime,
      formatDuration,
      truncateAddress,
      getStatusBadgeClass,
      getStatusText
    }
  }
}
</script>

<style scoped>
.parking-history {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.header-content h1 {
  margin: 0;
  color: #333;
}

.filters-stats {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #dee2e6;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  background: linear-gradient(135deg, var(--bs-primary), var(--bs-primary-dark));
  color: white;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stat-card.bg-success {
  background: linear-gradient(135deg, #28a745, #1e7e34);
}

.stat-card.bg-warning {
  background: linear-gradient(135deg, #ffc107, #d39e00);
}

.stat-card.bg-info {
  background: linear-gradient(135deg, #17a2b8, #117a8b);
}

.stat-content h3 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: bold;
}

.stat-content p {
  margin: 0;
  opacity: 0.9;
  font-size: 0.9rem;
}

.stat-icon {
  font-size: 2rem;
  opacity: 0.8;
}

.filter-controls {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.loading-container {
  text-align: center;
  padding: 50px;
}

.no-results {
  background: white;
  border-radius: 10px;
  border: 1px solid #dee2e6;
}

.reservations-table {
  background: white;
  border-radius: 10px;
  border: 1px solid #dee2e6;
  overflow: hidden;
}

.table th {
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

.lot-info strong {
  color: #333;
}

.vehicle-info strong {
  color: #333;
}

.time-info {
  font-size: 0.9rem;
}

.duration-info,
.cost-info {
  text-align: center;
}

.action-buttons {
  display: flex;
  gap: 5px;
  justify-content: center;
}

.pagination-container {
  margin-top: 30px;
}

.reservation-details h6 {
  color: #495057;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 5px;
  margin-bottom: 15px;
}

.modal.show {
  animation: fadeIn 0.15s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  
  .filters-stats .row {
    flex-direction: column-reverse;
  }
  
  .table-responsive {
    font-size: 0.8rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }

  .stat-content h3 {
    font-size: 1.5rem;
  }
}

@media (max-width: 576px) {
  .stats-cards {
    grid-template-columns: 1fr;
  }
}
</style> 