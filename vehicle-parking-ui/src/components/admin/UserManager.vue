<template>
  <div class="container-fluid p-0">
    <!-- Header with Search Bar -->
    <div class="d-flex justify-content-between align-items-center bg-white shadow-sm border-bottom px-4 py-3">
      <div class="d-flex align-items-center">
        <i class="fas fa-users text-primary me-2"></i>
        <h4 class="mb-0 fw-bold">User Manager</h4>
      </div>
      <div class="d-flex align-items-center gap-3">
        <div class="input-group" style="width: 300px;">
          <input
            v-model="searchQuery"
            type="text"
            class="form-control"
            placeholder="Search users..."
            @input="debouncedSearch"
          />
          <button class="btn btn-outline-secondary" type="button" @click="loadUsers">
            <i class="fas fa-search"></i>
          </button>
        </div>
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
                      <h6 class="card-title text-white-50">Total Users</h6>
                      <h3 class="mb-0">{{ totalStats.total || 0 }}</h3>
                    </div>
                    <i class="fas fa-users fa-2x opacity-75"></i>
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
                      <h6 class="card-title text-white-50">Active Users</h6>
                      <h3 class="mb-0">{{ totalStats.active || 0 }}</h3>
                    </div>
                    <i class="fas fa-user-check fa-2x opacity-75"></i>
                  </div>
                  <div class="mt-2">
                    <small class="text-white-50">Currently online</small>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="col-xl-3 col-lg-6 mb-3">
              <div class="card bg-warning bg-gradient text-white h-100">
                <div class="card-body">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="card-title text-white-50">Reservations</h6>
                      <h3 class="mb-0">{{ totalStats.total_reservations || 0 }}</h3>
                    </div>
                    <i class="fas fa-calendar-check fa-2x opacity-75"></i>
                  </div>
                  <div class="mt-2">
                    <small class="text-white-50">{{ totalStats.active_reservations || 0 }} active</small>
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
                      <h3 class="mb-0">₹{{ totalStats.total_spent || 0 }}</h3>
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
                  <select v-model="statusFilter" class="form-select" @change="loadUsers">
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

          <!-- Users List -->
          <div v-else class="row">
            <div
              v-for="user in users"
              :key="user.id"
              class="col-xl-6 col-lg-12 mb-4"
            >
              <div class="card h-100 shadow-sm hover-shadow-lg">
                <div class="card-body">
                  <div class="d-flex align-items-start">
                    <!-- Avatar -->
                    <div class="me-3">
                      <div class="bg-light rounded-circle d-flex align-items-center justify-content-center" style="width: 60px; height: 60px;">
                        <i class="fas fa-user fa-2x text-muted"></i>
                      </div>
                    </div>
                    
                    <!-- User Info -->
                    <div class="flex-grow-1">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                        <div>
                          <h6 class="mb-1 fw-bold">{{ user.full_name }}</h6>
                          <div class="d-flex align-items-center gap-2 mb-1">
                            <span class="text-muted small">@{{ user.username }}</span>
                            <span
                              :class="user.is_active ? 'badge bg-success' : 'badge bg-danger'"
                            >
                              {{ user.is_active ? 'Active' : 'Inactive' }}
                            </span>
                          </div>
                          <p class="text-muted small mb-1">
                            <i class="fas fa-envelope me-1"></i>
                            {{ user.email }}
                          </p>
                          <p class="text-muted small mb-0">
                            <i class="fas fa-phone me-1"></i>
                            {{ user.phone_number }}
                          </p>
                        </div>
                      </div>

                      <!-- Statistics -->
                      <div class="row g-2 mb-3">
                        <div class="col-4 text-center">
                          <div class="bg-light p-2 rounded">
                            <div class="fw-bold text-primary">{{ user.statistics.total_reservations }}</div>
                            <small class="text-muted">Bookings</small>
                          </div>
                        </div>
                        <div class="col-4 text-center">
                          <div class="bg-light p-2 rounded">
                            <div class="fw-bold text-success">{{ user.statistics.active_reservations }}</div>
                            <small class="text-muted">Active</small>
                          </div>
                        </div>
                        <div class="col-4 text-center">
                          <div class="bg-light p-2 rounded">
                            <div class="fw-bold text-info">₹{{ user.statistics.total_spent }}</div>
                            <small class="text-muted">Spent</small>
                          </div>
                        </div>
                      </div>

                      <!-- Current Reservation Alert -->
                      <div v-if="user.current_reservation" class="alert alert-warning py-2 mb-3">
                        <div class="d-flex align-items-center">
                          <i class="fas fa-parking me-2"></i>
                          <div class="small">
                            <strong>Currently Parked:</strong><br>
                            Spot {{ user.current_reservation.spot_number }} at {{ user.current_reservation.lot_name }}<br>
                            {{ user.current_reservation.vehicle_number }} • 
                            {{ Math.floor(user.current_reservation.duration_minutes / 60) }}h {{ user.current_reservation.duration_minutes % 60 }}m
                          </div>
                        </div>
                      </div>

                      <!-- Actions -->
                      <div class="d-flex gap-2">
                        <button
                          @click="viewUserDetails(user)"
                          class="btn btn-outline-primary btn-sm flex-fill"
                        >
                          <i class="fas fa-eye me-1"></i>
                          View Details
                        </button>
                        <button
                          @click="toggleUserStatus(user)"
                          :class="user.is_active ? 'btn btn-outline-danger btn-sm' : 'btn btn-outline-success btn-sm'"
                        >
                          <i :class="user.is_active ? 'fas fa-user-times' : 'fas fa-user-check'"></i>
                          {{ user.is_active ? 'Deactivate' : 'Activate' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="!loading && !error && users.length === 0" class="text-center py-5">
            <i class="fas fa-users fa-3x text-muted mb-3"></i>
            <h5 class="text-muted">No users found</h5>
            <p class="text-muted">No users match your search criteria.</p>
          </div>

          <!-- Pagination -->
          <nav v-if="pagination && pagination.pages > 1" aria-label="Users pagination">
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

    <!-- User Details Modal -->
    <div v-if="showUserModal" class="modal d-block" tabindex="-1" style="background-color: rgba(0, 0, 0, 0.5);" @click.self="closeUserModal">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-user me-2"></i>
              User Details
            </h5>
            <button type="button" class="btn-close" @click="closeUserModal" aria-label="Close"></button>
          </div>
          
          <div class="modal-body">
            <div v-if="selectedUser" class="row g-4">
              <!-- Personal Information -->
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">
                      <i class="fas fa-id-card me-2"></i>
                      Personal Information
                    </h6>
                  </div>
                  <div class="card-body">
                    <div class="row g-3">
                      <div class="col-12">
                        <label class="form-label text-muted">Full Name</label>
                        <p class="mb-0 fw-semibold">{{ selectedUser.full_name }}</p>
                      </div>
                      <div class="col-6">
                        <label class="form-label text-muted">Username</label>
                        <p class="mb-0">{{ selectedUser.username }}</p>
                      </div>
                      <div class="col-6">
                        <label class="form-label text-muted">Status</label>
                        <p class="mb-0">
                          <span :class="selectedUser.is_active ? 'badge bg-success' : 'badge bg-danger'">
                            {{ selectedUser.is_active ? 'Active' : 'Inactive' }}
                          </span>
                        </p>
                      </div>
                      <div class="col-12">
                        <label class="form-label text-muted">Email</label>
                        <p class="mb-0">{{ selectedUser.email }}</p>
                      </div>
                      <div class="col-12">
                        <label class="form-label text-muted">Phone</label>
                        <p class="mb-0">{{ selectedUser.phone_number }}</p>
                      </div>
                      <div class="col-12">
                        <label class="form-label text-muted">Address</label>
                        <p class="mb-0">{{ selectedUser.address || 'Not provided' }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Statistics -->
              <div class="col-md-6">
                <div class="card">
                  <div class="card-header">
                    <h6 class="mb-0">
                      <i class="fas fa-chart-bar me-2"></i>
                      Statistics
                    </h6>
                  </div>
                  <div class="card-body">
                    <div class="row g-3">
                      <div class="col-6">
                        <div class="text-center p-3 bg-primary bg-gradient text-white rounded">
                          <h4 class="mb-0">{{ selectedUser.statistics.total_reservations }}</h4>
                          <small>Total Bookings</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-center p-3 bg-success bg-gradient text-white rounded">
                          <h4 class="mb-0">{{ selectedUser.statistics.completed_reservations }}</h4>
                          <small>Completed</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-center p-3 bg-warning bg-gradient text-white rounded">
                          <h4 class="mb-0">{{ selectedUser.statistics.active_reservations }}</h4>
                          <small>Active</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-center p-3 bg-info bg-gradient text-white rounded">
                          <h4 class="mb-0">₹{{ selectedUser.statistics.total_spent }}</h4>
                          <small>Total Spent</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeUserModal">
              Close
            </button>
            <button
              @click="toggleUserStatus(selectedUser)"
              :class="selectedUser?.is_active ? 'btn btn-danger' : 'btn btn-success'"
            >
              <i :class="selectedUser?.is_active ? 'fas fa-user-times' : 'fas fa-user-check'" class="me-1"></i>
              {{ selectedUser?.is_active ? 'Deactivate User' : 'Activate User' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI, authAPI } from '../../services/api'

export default {
  name: 'UserManager',
  setup() {
    const router = useRouter()
    
    // Reactive data
    const loading = ref(true)
    const error = ref('')
    const users = ref([])
    const pagination = ref(null)
    const searchQuery = ref('')
    const statusFilter = ref('all')
    const currentPage = ref(1)
    const perPage = ref(10)
    
    // Modals
    const showUserModal = ref(false)
    const selectedUser = ref(null)

    // Computed stats
    const totalStats = computed(() => {
      const stats = {
        total: users.value.length,
        active: 0,
        total_reservations: 0,
        active_reservations: 0,
        total_spent: 0
      }
      
      users.value.forEach(user => {
        if (user.is_active) stats.active++
        stats.total_reservations += user.statistics?.total_reservations || 0
        stats.active_reservations += user.statistics?.active_reservations || 0
        stats.total_spent += user.statistics?.total_spent || 0
      })
      
      return stats
    })

    // Methods
    const loadUsers = async () => {
      try {
        loading.value = true
        error.value = ''

        const params = {
          page: currentPage.value,
          per_page: perPage.value,
          search: searchQuery.value,
          status: statusFilter.value
        }

        const response = await adminAPI.getUsers(params)
        
        if (response.data.success) {
          users.value = response.data.data.users
          pagination.value = response.data.data.pagination
        } else {
          error.value = response.data.message
        }
      } catch (err) {
        error.value = err.response?.data?.message || 'Failed to load users'
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
          loadUsers()
        }, 500)
      }
    })()
    
    const changePage = (page) => {
      if (page >= 1 && page <= pagination.value.pages) {
        currentPage.value = page
        loadUsers()
      }
    }
    
    const resetFilters = () => {
      searchQuery.value = ''
      statusFilter.value = 'all'
      currentPage.value = 1
      loadUsers()
    }
    
    const viewUserDetails = async (user) => {
      try {
        console.log('Loading user details for:', user.username)
        const response = await adminAPI.getUser(user.id)
        if (response.data.success) {
          selectedUser.value = response.data.data
          showUserModal.value = true
          console.log('User modal opened, showUserModal.value is now:', showUserModal.value)
        } else {
          alert(response.data.message || 'Failed to load user details')
        }
      } catch (err) {
        console.error('Error loading user details:', err)
        alert(err.response?.data?.message || 'Failed to load user details')
      }
    }
    
    const closeUserModal = () => {
      console.log('Closing user modal...')
      showUserModal.value = false
      selectedUser.value = null
      console.log('User modal closed, showUserModal.value is now:', showUserModal.value)
    }
    
    const toggleUserStatus = async (user) => {
      const action = user.is_active ? 'deactivate' : 'activate'
      if (!confirm(`Are you sure you want to ${action} user "${user.username}"?`)) {
        return
      }
      
      try {
        const response = await adminAPI.toggleUserStatus(user.id)
        if (response.data.success) {
          alert(response.data.message)
          loadUsers()
          // Update selectedUser if it's the same user
          if (selectedUser.value && selectedUser.value.id === user.id) {
            selectedUser.value.is_active = !selectedUser.value.is_active
          }
        } else {
          alert(response.data.message)
        }
      } catch (err) {
        alert(err.response?.data?.message || `Failed to ${action} user`)
      }
    }
    


    // Lifecycle
    onMounted(() => {
      loadUsers()
    })

    return {
      loading,
      error,
      users,
      pagination,
      searchQuery,
      statusFilter,
      currentPage,
      perPage,
      showUserModal,
      selectedUser,
      totalStats,
      loadUsers,
      debouncedSearch,
      changePage,
      resetFilters,
      viewUserDetails,
      closeUserModal,
      toggleUserStatus
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
}

.modal-content {
  background-clip: padding-box;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 0.3rem;
  box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.5);
}

.bg-gradient {
  background-image: linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0));
}

.avatar-circle {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: bold;
  font-size: 1.2rem;
}
</style> 