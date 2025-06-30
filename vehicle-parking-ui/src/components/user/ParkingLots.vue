<template>
  <div class="parking-lots">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1>Available Parking Lots</h1>
        <p class="text-muted">Find and reserve parking spots near you</p>
      </div>
      <div class="header-actions">
        <router-link to="/user/dashboard" class="btn btn-outline-primary">
          <i class="fas fa-arrow-left"></i> Back to Dashboard
        </router-link>
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="search-filters mb-4">
      <div class="row">
        <div class="col-md-6">
          <div class="input-group">
            <span class="input-group-text">
              <i class="fas fa-search"></i>
            </span>
            <input 
              type="text" 
              class="form-control" 
              placeholder="Search by location, address, or pin code..."
              v-model="searchQuery"
              @input="debouncedSearch"
            >
          </div>
        </div>
        <div class="col-md-3">
          <select class="form-select" v-model="sortBy" @change="sortLots">
            <option value="name">Sort by Name</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="available_spots">Most Available</option>
          </select>
        </div>
        <div class="col-md-3">
          <button @click="refreshLots" class="btn btn-outline-secondary w-100">
            <i class="fas fa-refresh"></i> Refresh
          </button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading parking lots...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="fas fa-exclamation-triangle"></i>
      {{ error }}
      <button @click="loadParkingLots" class="btn btn-sm btn-outline-danger ms-2">
        <i class="fas fa-refresh"></i> Retry
      </button>
    </div>

    <!-- No Results -->
    <div v-else-if="parkingLots.length === 0" class="no-results">
      <div class="text-center py-5">
        <i class="fas fa-search text-muted" style="font-size: 3rem;"></i>
        <h4 class="mt-3">No parking lots found</h4>
        <p class="text-muted">Try adjusting your search criteria or check back later.</p>
      </div>
    </div>

    <!-- Parking Lots Grid -->
    <div v-else class="parking-lots-grid">
      <div 
        v-for="lot in parkingLots" 
        :key="lot.id" 
        class="parking-lot-card"
      >
        <div class="card h-100">
          <div class="card-header">
            <div class="lot-header">
              <h5 class="mb-1">{{ lot.name }}</h5>
              <div class="lot-status">
                <span 
                  :class="getAvailabilityBadgeClass(lot.available_spots)"
                  class="badge"
                >
                  {{ lot.available_spots }} available
                </span>
              </div>
            </div>
          </div>
          
          <div class="card-body">
            <div class="lot-details">
              <div class="detail-item">
                <i class="fas fa-map-marker-alt text-muted"></i>
                <span>{{ lot.address }}</span>
              </div>
              
              <div class="detail-item">
                <i class="fas fa-location-dot text-muted"></i>
                <span>PIN: {{ lot.pin_code }}</span>
              </div>
              
              <div class="detail-item">
                <i class="fas fa-rupee-sign text-success"></i>
                <span class="price">₹{{ lot.price_per_hour }}/hour</span>
              </div>
              
              <div class="detail-item">
                <i class="fas fa-car text-muted"></i>
                <span>{{ lot.available_spots }}/{{ lot.total_spots }} spots available</span>
              </div>
              
              <div v-if="lot.description" class="detail-item">
                <i class="fas fa-info-circle text-muted"></i>
                <span class="description">{{ lot.description }}</span>
              </div>
            </div>
            
            <!-- Occupancy Progress Bar -->
            <div class="occupancy-meter mt-3">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <small class="text-muted">Occupancy</small>
                <small class="text-muted">{{ lot.occupancy_rate }}%</small>
              </div>
              <div class="progress">
                <div 
                  class="progress-bar" 
                  :class="getOccupancyProgressClass(lot.occupancy_rate)"
                  :style="{ width: lot.occupancy_rate + '%' }"
                ></div>
              </div>
            </div>
          </div>
          
          <div class="card-footer">
            <div class="lot-actions">
              <button 
                @click="viewLotDetails(lot)" 
                class="btn btn-outline-primary btn-sm"
              >
                <i class="fas fa-eye"></i> View Details
              </button>
              
              <button 
                @click="reserveSpot(lot)" 
                class="btn btn-primary btn-sm"
                :disabled="lot.available_spots === 0 || activeReservation || reservingLot === lot.id"
              >
                <i class="fas fa-plus"></i>
                {{ reservingLot === lot.id ? 'Reserving...' : 'Reserve Spot' }}
              </button>
            </div>
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

    <!-- Lot Details Modal -->
    <div v-if="showDetailsModal" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedLot?.name }}</h5>
            <button @click="closeDetailsModal" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <div v-if="lotDetails" class="lot-full-details">
              <div class="row mb-3">
                <div class="col-md-6">
                  <strong>Address:</strong><br>
                  {{ lotDetails.address }}
                </div>
                <div class="col-md-6">
                  <strong>PIN Code:</strong><br>
                  {{ lotDetails.pin_code }}
                </div>
              </div>
              
              <div class="row mb-3">
                <div class="col-md-6">
                  <strong>Price per Hour:</strong><br>
                  ₹{{ lotDetails.price_per_hour }}
                </div>
                <div class="col-md-6">
                  <strong>Available Spots:</strong><br>
                  {{ lotDetails.available_spots_count }}/{{ lotDetails.total_spots }}
                </div>
              </div>
              
              <div v-if="lotDetails.description" class="row mb-3">
                <div class="col-12">
                  <strong>Description:</strong><br>
                  {{ lotDetails.description }}
                </div>
              </div>
              
              <!-- Available Spots List -->
              <div v-if="lotDetails.available_spots?.length > 0" class="available-spots">
                <h6>Available Spots:</h6>
                <div class="spots-grid">
                  <span 
                    v-for="spot in lotDetails.available_spots" 
                    :key="spot.id"
                    class="badge bg-success me-1 mb-1"
                  >
                    {{ spot.spot_number }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeDetailsModal" class="btn btn-secondary">Close</button>
            <button 
              @click="reserveSpot(selectedLot)" 
              class="btn btn-primary"
              :disabled="!lotDetails?.available_spots_count || activeReservation"
            >
              <i class="fas fa-plus"></i> Reserve Spot
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showDetailsModal" class="modal-backdrop fade show"></div>

    <!-- Reserve Modal -->
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
                <small class="text-muted">Price: ₹{{ selectedLot?.price_per_hour }}/hour</small>
              </div>
              <div class="mb-3">
                <label for="vehicleNumber" class="form-label">Vehicle Number *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="vehicleNumber"
                  v-model="reservationForm.vehicle_number"
                  placeholder="Enter vehicle number (e.g., DL01AB1234)"
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
                  placeholder="Enter vehicle model (e.g., Honda City)"
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
import { ref, onMounted, watch } from 'vue'
import { userAPI, dashboardAPI } from '../../services/api'

export default {
  name: 'ParkingLots',
  setup() {
    // Reactive data
    const loading = ref(true)
    const error = ref('')
    const parkingLots = ref([])
    const pagination = ref(null)
    const searchQuery = ref('')
    const sortBy = ref('name')
    const currentPage = ref(1)
    
    // Modal state
    const showDetailsModal = ref(false)
    const showReserveModal = ref(false)
    const selectedLot = ref(null)
    const lotDetails = ref(null)
    
    // Reservation state
    const activeReservation = ref(null)
    const reservationForm = ref({
      vehicle_number: '',
      vehicle_model: ''
    })
    const reservingLot = ref(null)

    // Load parking lots
    const loadParkingLots = async (page = 1, search = '') => {
      try {
        loading.value = true
        error.value = ''
        
        const params = {
          page,
          per_page: 12,
          search: search.trim()
        }
        
        const response = await userAPI.getParkingLots(params)
        const data = response.data.data
        
        parkingLots.value = data.lots || []
        pagination.value = data.pagination
        currentPage.value = page
        
      } catch (err) {
        console.error('Error loading parking lots:', err)
        error.value = err.response?.data?.message || 'Failed to load parking lots'
        parkingLots.value = []
      } finally {
        loading.value = false
      }
    }

    // Check for active reservation
    const checkActiveReservation = async () => {
      try {
        const response = await dashboardAPI.getUserDashboard()
        activeReservation.value = response.data.data.active_reservation
      } catch (err) {
        console.error('Error checking active reservation:', err)
      }
    }

    // Debounced search
    let searchTimeout
    const debouncedSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        loadParkingLots(1, searchQuery.value)
      }, 500)
    }

    // Sort lots
    const sortLots = () => {
      const sorted = [...parkingLots.value]
      
      switch (sortBy.value) {
        case 'name':
          sorted.sort((a, b) => a.name.localeCompare(b.name))
          break
        case 'price_asc':
          sorted.sort((a, b) => a.price_per_hour - b.price_per_hour)
          break
        case 'price_desc':
          sorted.sort((a, b) => b.price_per_hour - a.price_per_hour)
          break
        case 'available_spots':
          sorted.sort((a, b) => b.available_spots - a.available_spots)
          break
      }
      
      parkingLots.value = sorted
    }

    // Pagination
    const changePage = (page) => {
      if (page >= 1 && page <= pagination.value.pages) {
        loadParkingLots(page, searchQuery.value)
      }
    }

    const getPageNumbers = () => {
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

    // View lot details
    const viewLotDetails = async (lot) => {
      try {
        selectedLot.value = lot
        showDetailsModal.value = true
        
        const response = await userAPI.getParkingLot(lot.id)
        lotDetails.value = response.data.data
        
      } catch (err) {
        console.error('Error loading lot details:', err)
        alert(err.response?.data?.message || 'Failed to load lot details')
      }
    }

    const closeDetailsModal = () => {
      showDetailsModal.value = false
      selectedLot.value = null
      lotDetails.value = null
    }

    // Reserve spot
    const reserveSpot = (lot) => {
      if (activeReservation.value) {
        alert('You already have an active reservation. Please complete it before making a new one.')
        return
      }
      
      selectedLot.value = lot
      showReserveModal.value = true
      reservationForm.value = { vehicle_number: '', vehicle_model: '' }
      closeDetailsModal()
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
        loadParkingLots(currentPage.value, searchQuery.value) // Refresh data
        checkActiveReservation() // Update active reservation
        
      } catch (err) {
        console.error('Error creating reservation:', err)
        alert(err.response?.data?.message || 'Failed to create reservation')
      } finally {
        reservingLot.value = null
      }
    }

    // Utility functions
    const refreshLots = () => {
      loadParkingLots(currentPage.value, searchQuery.value)
    }

    const getAvailabilityBadgeClass = (availableSpots) => {
      if (availableSpots === 0) return 'bg-danger'
      if (availableSpots <= 5) return 'bg-warning'
      return 'bg-success'
    }

    const getOccupancyProgressClass = (occupancyRate) => {
      if (occupancyRate >= 90) return 'bg-danger'
      if (occupancyRate >= 70) return 'bg-warning'
      return 'bg-success'
    }

    // Load data on mount
    onMounted(() => {
      loadParkingLots()
      checkActiveReservation()
    })

    return {
      loading,
      error,
      parkingLots,
      pagination,
      searchQuery,
      sortBy,
      currentPage,
      showDetailsModal,
      showReserveModal,
      selectedLot,
      lotDetails,
      activeReservation,
      reservationForm,
      reservingLot,
      loadParkingLots,
      debouncedSearch,
      sortLots,
      changePage,
      getPageNumbers,
      viewLotDetails,
      closeDetailsModal,
      reserveSpot,
      closeReserveModal,
      confirmReservation,
      refreshLots,
      getAvailabilityBadgeClass,
      getOccupancyProgressClass
    }
  }
}
</script>

<style scoped>
.parking-lots {
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

.search-filters {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #dee2e6;
}

.loading-container {
  text-align: center;
  padding: 50px;
}

.no-results {
  background: #f8f9fa;
  border-radius: 10px;
  border: 1px solid #dee2e6;
}

.parking-lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.parking-lot-card .card {
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #dee2e6;
}

.parking-lot-card .card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.lot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.detail-item i {
  width: 16px;
  flex-shrink: 0;
}

.price {
  font-weight: 600;
  color: #28a745;
}

.description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.occupancy-meter .progress {
  height: 6px;
  border-radius: 3px;
}

.lot-actions {
  display: flex;
  gap: 10px;
}

.lot-actions .btn {
  flex: 1;
}

.pagination-container {
  margin-top: 30px;
}

.spots-grid {
  max-height: 200px;
  overflow-y: auto;
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
  
  .parking-lots-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .search-filters .row > div {
    margin-bottom: 10px;
  }
  
  .lot-actions {
    flex-direction: column;
  }
}
</style> 