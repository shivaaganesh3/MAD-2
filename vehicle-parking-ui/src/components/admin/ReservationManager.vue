<template>
  <div class="reservation-manager">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1>Reservation Management</h1>
        <p class="text-muted">View and manage all parking reservations</p>
      </div>
      <div class="header-actions">
        <router-link to="/admin/dashboard" class="btn btn-outline-primary">
          <i class="fas fa-arrow-left"></i> Back to Dashboard
        </router-link>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-section mb-4">
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0">
            <i class="fas fa-filter"></i> Filters
          </h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-2">
              <label class="form-label">Status</label>
              <select class="form-select" v-model="filters.status" @change="applyFilters">
                <option value="">All Status</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">User</label>
              <input 
                type="text" 
                class="form-control" 
                placeholder="Search by name, username, email..."
                v-model="filters.user"
                @input="debouncedFilter"
              >
            </div>
            <div class="col-md-3">
              <label class="form-label">Parking Lot</label>
              <input 
                type="text" 
                class="form-control" 
                placeholder="Search by lot name..."
                v-model="filters.lot"
                @input="debouncedFilter"
              >
            </div>
            <div class="col-md-2">
              <label class="form-label">Date From</label>
              <input 
                type="date" 
                class="form-control" 
                v-model="filters.dateFrom"
                @change="applyFilters"
              >
            </div>
            <div class="col-md-2">
              <label class="form-label">Date To</label>
              <input 
                type="date" 
                class="form-control" 
                v-model="filters.dateTo"
                @change="applyFilters"
              >
            </div>
          </div>
          <div class="row mt-3">
            <div class="col-md-12">
              <button @click="clearFilters" class="btn btn-outline-secondary me-2">
                <i class="fas fa-times"></i> Clear Filters
              </button>
              <button @click="refreshReservations" class="btn btn-outline-primary">
                <i class="fas fa-refresh"></i> Refresh
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Stats -->
    <div class="summary-stats mb-4">
      <div class="row">
        <div class="col-md-3">
          <div class="stat-card bg-primary">
            <div class="stat-content">
              <h3>{{ pagination?.total || 0 }}</h3>
              <p>Total Reservations</p>
            </div>
            <i class="fas fa-list stat-icon"></i>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card bg-warning">
            <div class="stat-content">
              <h3>{{ activeCount }}</h3>
              <p>Active Now</p>
            </div>
            <i class="fas fa-clock stat-icon"></i>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card bg-success">
            <div class="stat-content">
              <h3>{{ completedCount }}</h3>
              <p>Completed</p>
            </div>
            <i class="fas fa-check-circle stat-icon"></i>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stat-card bg-info">
            <div class="stat-content">
              <h3>₹{{ totalRevenue }}</h3>
              <p>Total Revenue</p>
            </div>
            <i class="fas fa-rupee-sign stat-icon"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading reservations...</p>
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
        <i class="fas fa-search text-muted" style="font-size: 3rem;"></i>
        <h4 class="mt-3">No reservations found</h4>
        <p class="text-muted">Try adjusting your filter criteria.</p>
      </div>
    </div>

    <!-- Reservations Table -->
    <div v-else class="reservations-table">
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0">
            <i class="fas fa-table"></i> Reservations ({{ pagination?.total || 0 }})
          </h5>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>User</th>
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
                    <span class="badge bg-secondary">#{{ reservation.id }}</span>
                  </td>
                  <td>
                    <div class="user-info">
                      <strong>{{ reservation.user.full_name }}</strong><br>
                      <small class="text-muted">{{ reservation.user.username }}</small><br>
                      <small class="text-muted">{{ reservation.user.email }}</small>
                    </div>
                  </td>
                  <td>
                    <div class="lot-info">
                      <strong>{{ reservation.parking_lot.name }}</strong><br>
                      <small class="text-muted">{{ truncateText(reservation.parking_lot.address, 30) }}</small><br>
                      <small class="text-info">₹{{ reservation.parking_lot.price_per_hour }}/hr</small>
                    </div>
                  </td>
                  <td>
                    <span class="badge bg-dark">{{ reservation.spot_number }}</span>
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
                      <div v-if="reservation.status === 'active'" class="text-warning">
                        <small><i class="fas fa-calculator"></i> Estimated</small>
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
                        @click="forceRelease(reservation.id)"
                        class="btn btn-sm btn-warning"
                        :disabled="releasingReservation === reservation.id"
                        title="Force Release"
                      >
                        <i class="fas fa-eject"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
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
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reservation Details #{{ selectedReservation?.id }}</h5>
            <button @click="closeDetailsModal" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <div v-if="reservationDetails" class="reservation-details">
              <div class="row mb-4">
                <div class="col-md-6">
                  <h6>User Information</h6>
                  <table class="table table-sm">
                    <tr><td><strong>Name:</strong></td><td>{{ reservationDetails.user.full_name }}</td></tr>
                    <tr><td><strong>Username:</strong></td><td>{{ reservationDetails.user.username }}</td></tr>
                    <tr><td><strong>Email:</strong></td><td>{{ reservationDetails.user.email }}</td></tr>
                    <tr><td><strong>Phone:</strong></td><td>{{ reservationDetails.user.phone_number || 'N/A' }}</td></tr>
                    <tr><td><strong>Address:</strong></td><td>{{ reservationDetails.user.address || 'N/A' }}</td></tr>
                  </table>
                </div>
                <div class="col-md-6">
                  <h6>Parking Information</h6>
                  <table class="table table-sm">
                    <tr><td><strong>Lot Name:</strong></td><td>{{ reservationDetails.parking_lot.name }}</td></tr>
                    <tr><td><strong>Address:</strong></td><td>{{ reservationDetails.parking_lot.address }}</td></tr>
                    <tr><td><strong>PIN Code:</strong></td><td>{{ reservationDetails.parking_lot.pin_code }}</td></tr>
                    <tr><td><strong>Spot Number:</strong></td><td>{{ reservationDetails.parking_spot.spot_number }}</td></tr>
                    <tr><td><strong>Vehicle Type:</strong></td><td>{{ reservationDetails.parking_spot.vehicle_type }}</td></tr>
                  </table>
                </div>
              </div>

              <div class="row mb-4">
                <div class="col-md-6">
                  <h6>Vehicle Information</h6>
                  <table class="table table-sm">
                    <tr><td><strong>Vehicle Number:</strong></td><td>{{ reservationDetails.vehicle_number }}</td></tr>
                    <tr><td><strong>Vehicle Model:</strong></td><td>{{ reservationDetails.vehicle_model || 'N/A' }}</td></tr>
                  </table>
                </div>
                <div class="col-md-6">
                  <h6>Status & Timing</h6>
                  <table class="table table-sm">
                    <tr><td><strong>Status:</strong></td><td>
                      <span :class="getStatusBadgeClass(reservationDetails.status)">
                        {{ getStatusText(reservationDetails.status) }}
                      </span>
                    </td></tr>
                    <tr><td><strong>Start Time:</strong></td><td>{{ formatDateTime(reservationDetails.parking_timestamp) }}</td></tr>
                    <tr v-if="reservationDetails.leaving_timestamp"><td><strong>End Time:</strong></td><td>{{ formatDateTime(reservationDetails.leaving_timestamp) }}</td></tr>
                    <tr><td><strong>Duration:</strong></td><td>{{ formatDuration(reservationDetails.duration_minutes) }}</td></tr>
                  </table>
                </div>
              </div>

              <!-- Cost Breakdown -->
              <div v-if="reservationDetails.cost_breakdown" class="row mb-4">
                <div class="col-12">
                  <h6>Cost Breakdown</h6>
                  <div class="cost-breakdown-card">
                    <table class="table table-sm">
                      <tr><td><strong>Hourly Rate:</strong></td><td>₹{{ reservationDetails.cost_breakdown.hourly_rate }}/hour</td></tr>
                      <tr><td><strong>Billing Method:</strong></td><td>{{ reservationDetails.cost_breakdown.billing_method }}</td></tr>
                      <tr><td><strong>Duration (Minutes):</strong></td><td>{{ reservationDetails.cost_breakdown.duration_minutes }} minutes</td></tr>
                      <tr><td><strong>Duration (Hours):</strong></td><td>{{ reservationDetails.cost_breakdown.duration_hours }} hours</td></tr>
                      <tr v-if="reservationDetails.cost_breakdown.billing_hours"><td><strong>Billing Hours:</strong></td><td>{{ reservationDetails.cost_breakdown.billing_hours }} hours (rounded up)</td></tr>
                      <tr class="table-success">
                        <td><strong>{{ reservationDetails.cost_breakdown.is_final ? 'Final Cost:' : 'Estimated Cost:' }}</strong></td>
                        <td><strong>₹{{ reservationDetails.cost_breakdown.final_cost || reservationDetails.cost_breakdown.estimated_cost }}</strong></td>
                      </tr>
                    </table>
                    <div v-if="!reservationDetails.cost_breakdown.is_final" class="text-info">
                      <small><i class="fas fa-info-circle"></i> Cost is being calculated in real-time for active reservations</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeDetailsModal" class="btn btn-secondary">Close</button>
            <button 
              v-if="reservationDetails?.status === 'active'" 
              @click="forceRelease(reservationDetails.id)"
              class="btn btn-warning"
              :disabled="releasingReservation === reservationDetails.id"
            >
              <i class="fas fa-eject"></i>
              {{ releasingReservation === reservationDetails.id ? 'Releasing...' : 'Force Release' }}
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
import { adminAPI } from '../../services/api'

export default {
  name: 'ReservationManager',
  setup() {
    // Reactive data
    const loading = ref(true)
    const error = ref('')
    const reservations = ref([])
    const pagination = ref(null)
    const currentPage = ref(1)
    
    // Filters
    const filters = ref({
      status: '',
      user: '',
      lot: '',
      dateFrom: '',
      dateTo: ''
    })
    
    // Modal state
    const showDetailsModal = ref(false)
    const selectedReservation = ref(null)
    const reservationDetails = ref(null)
    const releasingReservation = ref(null)

    // Load reservations
    const loadReservations = async (page = 1) => {
      try {
        loading.value = true
        error.value = ''
        
        const params = {
          page,
          per_page: 20,
          status: filters.value.status,
          user: filters.value.user,
          lot: filters.value.lot,
          date_from: filters.value.dateFrom,
          date_to: filters.value.dateTo
        }
        
        const response = await adminAPI.getReservations(params)
        const data = response.data.data
        
        reservations.value = data.reservations || []
        pagination.value = data.pagination
        currentPage.value = page
        
      } catch (err) {
        console.error('Error loading reservations:', err)
        error.value = err.response?.data?.message || 'Failed to load reservations'
        reservations.value = []
      } finally {
        loading.value = false
      }
    }

    // Computed stats
    const activeCount = computed(() => {
      return reservations.value.filter(r => r.status === 'active').length
    })

    const completedCount = computed(() => {
      return reservations.value.filter(r => r.status === 'completed').length
    })

    const totalRevenue = computed(() => {
      return reservations.value
        .filter(r => r.status === 'completed' && r.cost)
        .reduce((total, r) => total + r.cost, 0)
        .toFixed(2)
    })

    // Filter functions
    let filterTimeout
    const debouncedFilter = () => {
      clearTimeout(filterTimeout)
      filterTimeout = setTimeout(() => {
        applyFilters()
      }, 500)
    }

    const applyFilters = () => {
      loadReservations(1)
    }

    const clearFilters = () => {
      filters.value = {
        status: '',
        user: '',
        lot: '',
        dateFrom: '',
        dateTo: ''
      }
      loadReservations(1)
    }

    const refreshReservations = () => {
      loadReservations(currentPage.value)
    }

    // Pagination
    const changePage = (page) => {
      if (page >= 1 && page <= pagination.value.pages) {
        loadReservations(page)
      }
    }

    const getPageNumbers = () => {
      if (!pagination.value) return []
      
      const pages = []
      const total = pagination.value.pages
      const current = pagination.value.page
      
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
        
        const response = await adminAPI.getReservation(reservation.id)
        reservationDetails.value = response.data.data
        
      } catch (err) {
        console.error('Error loading reservation details:', err)
        alert(err.response?.data?.message || 'Failed to load reservation details')
      }
    }

    const closeDetailsModal = () => {
      showDetailsModal.value = false
      selectedReservation.value = null
      reservationDetails.value = null
    }

    // Force release reservation
    const forceRelease = async (reservationId) => {
      if (!confirm('Are you sure you want to force release this parking spot? This action cannot be undone.')) {
        return
      }
      
      try {
        releasingReservation.value = reservationId
        
        const response = await adminAPI.forceReleaseReservation(reservationId)
        const data = response.data.data
        
        alert(`Parking spot force-released successfully! Final cost: ₹${data.final_cost}`)
        closeDetailsModal()
        loadReservations(currentPage.value) // Refresh data
        
      } catch (err) {
        console.error('Error force-releasing reservation:', err)
        alert(err.response?.data?.message || 'Failed to force release reservation')
      } finally {
        releasingReservation.value = null
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

    const truncateText = (text, maxLength) => {
      if (!text) return ''
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
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
      currentPage,
      filters,
      showDetailsModal,
      selectedReservation,
      reservationDetails,
      releasingReservation,
      activeCount,
      completedCount,
      totalRevenue,
      loadReservations,
      debouncedFilter,
      applyFilters,
      clearFilters,
      refreshReservations,
      changePage,
      getPageNumbers,
      viewReservationDetails,
      closeDetailsModal,
      forceRelease,
      formatDateTime,
      formatDate,
      formatTime,
      formatDuration,
      truncateText,
      getStatusBadgeClass,
      getStatusText
    }
  }
}
</script>

<style scoped>
.reservation-manager {
  padding: 20px;
  max-width: 1600px;
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

.filters-section {
  background: #f8f9fa;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
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

.loading-container {
  text-align: center;
  padding: 50px;
}

.no-results {
  background: white;
  border-radius: 10px;
  border: 1px solid #dee2e6;
}

.user-info, .lot-info, .vehicle-info, .time-info, .duration-info, .cost-info {
  font-size: 0.9rem;
}

.action-buttons {
  display: flex;
  gap: 5px;
  justify-content: center;
}

.pagination-container {
  margin-top: 30px;
}

.cost-breakdown-card {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #dee2e6;
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
  
  .summary-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .table-responsive {
    font-size: 0.8rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}

@media (max-width: 576px) {
  .summary-stats {
    grid-template-columns: 1fr;
  }
}
</style> 