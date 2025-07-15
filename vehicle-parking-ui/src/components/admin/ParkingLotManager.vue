<template>
  <div class="container-fluid p-0">
    <!-- Header with Search Bar -->
    <div class="d-flex justify-content-between align-items-center bg-white shadow-sm border-bottom px-4 py-3">
      <div class="d-flex align-items-center">
        <i class="fas fa-building text-primary me-2"></i>
        <h4 class="mb-0 fw-bold">Parking Lot Manager</h4>
      </div>
      <div class="d-flex align-items-center gap-3">
        <div class="input-group" style="width: 300px;">
          <input
            v-model="searchQuery"
            type="text"
            class="form-control"
            placeholder="Search parking lots..."
            @input="debouncedSearch"
          />
          <button class="btn btn-outline-secondary" type="button" @click="loadParkingLots">
            <i class="fas fa-search"></i>
          </button>
        </div>
        <button
          @click="openCreateModal"
          class="btn btn-primary"
        >
          <i class="fas fa-plus me-1"></i>
          Add Lot
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container-fluid">
        <div class="p-4">
          <!-- Statistics Cards -->
          <div class="row mb-4">
            <div class="col-xl-3 col-lg-6 mb-3">
              <div class="card bg-primary bg-gradient text-white h-100">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="card-title text-white-50">Total Lots</h6>
                      <h3 class="mb-0">{{ totalStats.total || 0 }}</h3>
                    </div>
                    <i class="fas fa-building fa-2x opacity-75"></i>
                  </div>
                  <div class="mt-2">
                    <small class="text-white-50">{{ totalStats.active || 0 }} active</small>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-xl-3 col-lg-6 mb-3">
              <div class="card bg-success bg-gradient text-white h-100">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="card-title text-white-50">Total Spots</h6>
                      <h3 class="mb-0">{{ totalStats.total_spots || 0 }}</h3>
                    </div>
                    <i class="fas fa-parking fa-2x opacity-75"></i>
                  </div>
                  <div class="mt-2">
                    <small class="text-white-50">{{ totalStats.available_spots || 0 }} available</small>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-xl-3 col-lg-6 mb-3">
              <div class="card bg-warning bg-gradient text-white h-100">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="card-title text-white-50">Occupancy</h6>
                      <h3 class="mb-0">{{ totalStats.occupancy_rate || 0 }}%</h3>
                    </div>
                    <i class="fas fa-chart-pie fa-2x opacity-75"></i>
                  </div>
                  <div class="mt-2">
                    <small class="text-white-50">{{ totalStats.occupied_spots || 0 }} occupied</small>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-xl-3 col-lg-6 mb-3">
              <div class="card bg-info bg-gradient text-white h-100">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="card-title text-white-50">Revenue</h6>
                      <h3 class="mb-0">₹{{ totalStats.total_revenue || 0 }}</h3>
                    </div>
                    <i class="fas fa-rupee-sign fa-2x opacity-75"></i>
                  </div>
                  <div class="mt-2">
                    <small class="text-white-50">Total earnings</small>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Filters -->
          <div class="card mb-4">
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Status Filter</label>
                  <select v-model="statusFilter" class="form-select" @change="loadParkingLots">
                    <option value="all">All Status</option>
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                  </select>
                </div>
                <div class="col-md-6 d-flex align-items-end">
                  <button @click="resetFilters" class="btn btn-outline-secondary">
                    <i class="fas fa-undo me-1"></i>
                    Reset Filters
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loading" class="d-flex justify-content-center align-items-center" style="height: 300px;">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="alert alert-danger" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            {{ error }}
          </div>

          <!-- Parking Lots Grid -->
          <div v-else class="row">
            <div
              v-for="lot in parkingLots"
              :key="lot.id"
              class="col-xl-4 col-lg-6 col-md-6 mb-4"
            >
              <div class="card h-100 shadow-sm hover-shadow-lg">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h6 class="card-title mb-0 fw-bold">{{ lot.prime_location_name }}</h6>
                  <span
                    :class="lot.is_active ? 'badge bg-success' : 'badge bg-danger'"
                  >
                    {{ lot.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </div>
                
                <div class="card-body">
                  <div class="mb-3">
                    <p class="text-muted mb-1">
                      <i class="fas fa-map-marker-alt me-1"></i>
                      {{ lot.address }}
                    </p>
                    <p class="text-muted mb-1">
                      <i class="fas fa-hashtag me-1"></i>
                      Pin: {{ lot.pin_code }}
                    </p>
                    <p class="text-muted mb-0">
                      <i class="fas fa-rupee-sign me-1"></i>
                      ₹{{ lot.price_per_hour }}/hour
                    </p>
                  </div>

                  <!-- Spot Statistics -->
                  <div class="row mb-3">
                    <div class="col-6 text-center">
                      <div class="bg-light p-2 rounded">
                        <h5 class="mb-0 text-primary">{{ lot.number_of_spots }}</h5>
                        <small class="text-muted">Total</small>
                      </div>
                    </div>
                    <div class="col-6 text-center">
                      <div class="bg-light p-2 rounded">
                        <h5 class="mb-0 text-success">{{ lot.available_spots }}</h5>
                        <small class="text-muted">Available</small>
                      </div>
                    </div>
                  </div>

                  <!-- Occupancy Progress -->
                  <div class="mb-3">
                    <div class="d-flex justify-content-between mb-1">
                      <small class="text-muted">Occupancy</small>
                      <small class="fw-bold">{{ lot.occupancy_rate }}%</small>
                    </div>
                    <div class="progress" style="height: 6px;">
                      <div
                        class="progress-bar"
                        :class="getOccupancyColor(lot.occupancy_rate)"
                        :style="{ width: `${lot.occupancy_rate}%` }"
                      ></div>
                    </div>
                  </div>

                  <!-- Revenue -->
                  <div class="border-top pt-3">
                    <div class="d-flex justify-content-between align-items-center">
                      <span class="text-muted">Revenue</span>
                      <span class="fw-bold h6 mb-0">₹{{ lot.total_revenue }}</span>
                    </div>
                  </div>
                </div>

                <!-- Actions -->
                <div class="card-footer bg-transparent">
                  <div class="d-grid gap-2 d-md-flex">
                    <button
                      @click="viewLotDetails(lot)"
                      class="btn btn-outline-primary btn-sm flex-fill"
                    >
                      <i class="fas fa-eye me-1"></i>
                      View
                    </button>
                    <button
                      @click="editLot(lot)"
                      class="btn btn-outline-success btn-sm flex-fill"
                    >
                      <i class="fas fa-edit me-1"></i>
                      Edit
                    </button>
                    <button
                      @click="deleteLot(lot)"
                      class="btn btn-outline-danger btn-sm"
                    >
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="!loading && !error && parkingLots.length === 0" class="text-center py-5">
            <i class="fas fa-building fa-3x text-muted mb-3"></i>
            <h5 class="text-muted">No parking lots found</h5>
            <p class="text-muted">Get started by creating your first parking lot.</p>
            <button
              @click="openCreateModal"
              class="btn btn-primary"
            >
              <i class="fas fa-plus me-1"></i>
              Add Parking Lot
            </button>
          </div>

          <!-- Pagination -->
          <nav v-if="pagination && pagination.pages > 1" aria-label="Parking lots pagination">
            <ul class="pagination justify-content-center">
              <li class="page-item" :class="{ disabled: !pagination.has_prev }">
                <button class="page-link" @click="changePage(pagination.page - 1)" :disabled="!pagination.has_prev">
                  Previous
                </button>
              </li>
              <li class="page-item active">
                <span class="page-link">{{ pagination.page }}</span>
              </li>
              <li class="page-item" :class="{ disabled: !pagination.has_next }">
                <button class="page-link" @click="changePage(pagination.page + 1)" :disabled="!pagination.has_next">
                  Next
                </button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0, 0, 0, 0.5);" @click.self="closeModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <form @submit.prevent="submitForm">
            <div class="modal-header">
              <h5 class="modal-title">
                <i class="fas fa-building me-2"></i>
                {{ showCreateModal ? 'Create Parking Lot' : 'Edit Parking Lot' }}
              </h5>
              <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
            </div>
            
            <div class="modal-body">
              <div class="row g-3">
                <div class="col-12">
                  <label class="form-label">Location Name *</label>
                  <input
                    v-model="lotForm.prime_location_name"
                    type="text"
                    class="form-control"
                    placeholder="e.g., City Center Mall"
                    required
                  />
                </div>
                
                <div class="col-12">
                  <label class="form-label">Address *</label>
                  <textarea
                    v-model="lotForm.address"
                    class="form-control"
                    rows="3"
                    placeholder="Full address..."
                    required
                  ></textarea>
                </div>
                
                <div class="col-md-6">
                  <label class="form-label">Pin Code *</label>
                  <input
                    v-model="lotForm.pin_code"
                    type="text"
                    class="form-control"
                    placeholder="110001"
                    pattern="[0-9]{6}"
                    maxlength="6"
                    required
                  />
                </div>
                
                <div class="col-md-6">
                  <label class="form-label">Price per Hour *</label>
                  <div class="input-group">
                    <span class="input-group-text">₹</span>
                    <input
                      v-model="lotForm.price_per_hour"
                      type="number"
                      class="form-control"
                      placeholder="50"
                      min="1"
                      max="10000"
                      step="0.01"
                      required
                    />
                  </div>
                </div>
                
                <div class="col-md-6">
                  <label class="form-label">Number of Spots *</label>
                  <input
                    v-model="lotForm.number_of_spots"
                    type="number"
                    class="form-control"
                    placeholder="50"
                    min="1"
                    max="1000"
                    required
                  />
                </div>
                
                <div class="col-12">
                  <label class="form-label">Description</label>
                  <textarea
                    v-model="lotForm.description"
                    class="form-control"
                    rows="2"
                    placeholder="Optional description..."
                  ></textarea>
                </div>
                
                <div class="col-12">
                  <div class="form-check">
                    <input
                      v-model="lotForm.is_active"
                      type="checkbox"
                      class="form-check-input"
                      id="isActive"
                    />
                    <label class="form-check-label" for="isActive">
                      Active
                    </label>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">
                Cancel
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="submitting"
              >
                <span v-if="submitting" class="spinner-border spinner-border-sm me-1"></span>
                {{ submitting ? 'Saving...' : (showCreateModal ? 'Create' : 'Update') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI, authAPI } from '../../services/api'

export default {
  name: 'ParkingLotManager',
  setup() {
    const router = useRouter()
    
    // Reactive data
    const loading = ref(true)
    const error = ref('')
    const parkingLots = ref([])
    const pagination = ref(null)
    const searchQuery = ref('')
    const statusFilter = ref('all')
    const currentPage = ref(1)
    const perPage = ref(9)
    
    // Modals
    const showCreateModal = ref(false)
    const showEditModal = ref(false)
    const submitting = ref(false)
    const editingLot = ref(null)
    
    // Form
    const lotForm = reactive({
      prime_location_name: '',
      address: '',
      pin_code: '',
      price_per_hour: '',
      number_of_spots: '',
      description: '',
      is_active: true
    })

    // Computed stats
    const totalStats = computed(() => {
      const stats = {
        total: parkingLots.value.length,
        active: 0,
        total_spots: 0,
        available_spots: 0,
        occupied_spots: 0,
        occupancy_rate: 0,
        total_revenue: 0
      }
      
      parkingLots.value.forEach(lot => {
        if (lot.is_active) stats.active++
        stats.total_spots += lot.number_of_spots || 0
        stats.available_spots += lot.available_spots || 0
        stats.occupied_spots += (lot.number_of_spots || 0) - (lot.available_spots || 0)
        stats.total_revenue += lot.total_revenue || 0
      })
      
      if (stats.total_spots > 0) {
        stats.occupancy_rate = Math.round((stats.occupied_spots / stats.total_spots) * 100)
      }
      
      return stats
    })

    // Methods
    const loadParkingLots = async () => {
      try {
        loading.value = true
        error.value = ''

        const params = {
          page: currentPage.value,
          per_page: perPage.value,
          search: searchQuery.value,
          status: statusFilter.value
        }

        const response = await adminAPI.getParkingLots(params)
        
        if (response.data.success) {
          parkingLots.value = response.data.data.parking_lots
          pagination.value = response.data.data.pagination
        } else {
          error.value = response.data.message
        }
      } catch (err) {
        error.value = err.response?.data?.message || 'Failed to load parking lots'
      } finally {
        loading.value = false
      }
    }
    
    const debouncedSearch = (() => {
      let timeout
      return () => {
        clearTimeout(timeout)
        timeout = setTimeout(() => {
          currentPage.value = 1
          loadParkingLots()
        }, 500)
      }
    })()
    
    const getOccupancyColor = (rate) => {
      if (rate < 50) return 'bg-success'
      if (rate < 80) return 'bg-warning'
      return 'bg-danger'
    }
    
    const changePage = (page) => {
      if (page >= 1 && page <= pagination.value.pages) {
        currentPage.value = page
        loadParkingLots()
      }
    }
    
    const resetFilters = () => {
      searchQuery.value = ''
      statusFilter.value = 'all'
      currentPage.value = 1
      loadParkingLots()
    }
    
    const openCreateModal = () => {
      console.log('Opening create modal...')
      resetForm()
      showCreateModal.value = true
      console.log('showCreateModal.value is now:', showCreateModal.value)
    }
    
    const editLot = (lot) => {
      editingLot.value = lot
      Object.assign(lotForm, lot)
      showEditModal.value = true
    }
    
    const deleteLot = async (lot) => {
      if (!confirm(`Are you sure you want to delete "${lot.prime_location_name}"? This action cannot be undone.`)) {
        return
      }
      
      try {
        const response = await adminAPI.deleteParkingLot(lot.id)
        if (response.data.success) {
          alert('Parking lot deleted successfully')
          loadParkingLots()
        } else {
          alert(response.data.message)
        }
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to delete parking lot')
      }
    }
    
    const viewLotDetails = (lot) => {
      alert(`Viewing details for ${lot.prime_location_name}`)
    }
    
    const closeModal = () => {
      console.log('Closing modal...')
      showCreateModal.value = false
      showEditModal.value = false
      editingLot.value = null
      resetForm()
      console.log('Modal closed, showCreateModal.value is now:', showCreateModal.value)
    }
    
    const resetForm = () => {
      Object.assign(lotForm, {
        prime_location_name: '',
        address: '',
        pin_code: '',
        price_per_hour: '',
        number_of_spots: '',
        description: '',
        is_active: true
      })
    }
    
    const submitForm = async () => {
      try {
        submitting.value = true
        
        let response
        if (showCreateModal.value) {
          response = await adminAPI.createParkingLot(lotForm)
        } else {
          response = await adminAPI.updateParkingLot(editingLot.value.id, lotForm)
        }
        
        if (response.data.success) {
          alert(response.data.message)
          closeModal()
          loadParkingLots()
        } else {
          alert(response.data.message || 'Operation failed')
        }
      } catch (err) {
        if (err.response?.data?.errors) {
          alert(err.response.data.errors.join('\n'))
        } else {
          alert(err.response?.data?.message || 'Operation failed')
        }
      } finally {
        submitting.value = false
      }
    }
    


    // Lifecycle
    onMounted(() => {
      loadParkingLots()
    })

    return {
      loading,
      error,
      parkingLots,
      pagination,
      searchQuery,
      statusFilter,
      currentPage,
      perPage,
      showCreateModal,
      showEditModal,
      submitting,
      editingLot,
      lotForm,
      totalStats,
      loadParkingLots,
      debouncedSearch,
      getOccupancyColor,
      changePage,
      resetFilters,
      openCreateModal,
      editLot,
      deleteLot,
      viewLotDetails,
      closeModal,
      resetForm,
      submitForm
    }
  }
}
</script>

<style scoped>
.hover-shadow-lg:hover {
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175) !important;
  transition: box-shadow 0.15s ease-in-out;
}

.nav-link.active {
  background-color: rgba(13, 110, 253, 0.1);
  color: #0d6efd !important;
  font-weight: 600;
}

.nav-link:hover {
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 0.375rem;
}

.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

.modal {
  z-index: 1050;
}

.modal-dialog {
  margin: 1.75rem auto;
  max-width: 800px;
}

.modal-content {
  background-clip: padding-box;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 0.3rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.5);
}

.progress {
  background-color: #e9ecef;
}

.bg-gradient {
  background-image: linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0));
}
</style> 