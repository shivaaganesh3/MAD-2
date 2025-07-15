<template>
  <div class="container-fluid p-0">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center bg-white shadow-sm border-bottom px-4 py-3">
      <div class="d-flex align-items-center">
        <i class="fas fa-chart-line text-primary me-2"></i>
        <h4 class="mb-0 fw-bold">System Statistics</h4>
      </div>
      <div class="d-flex align-items-center gap-3">
        <button
          @click="loadStatistics"
          class="btn btn-outline-primary"
          :disabled="loading"
        >
          <i class="fas fa-sync-alt me-1" :class="{ 'fa-spin': loading }"></i>
          Refresh
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container-fluid">
        <div class="p-4">
          <!-- Loading State -->
          <div v-if="loading" class="d-flex justify-content-center align-items-center" style="height: 400px;">
            <div class="text-center">
              <div class="spinner-border text-primary mb-3" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="text-muted">Loading system statistics...</p>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="alert alert-danger" role="alert">
            <i class="fas fa-exclamation-triangle me-2"></i>
            {{ error }}
            <button @click="loadStatistics" class="btn btn-outline-danger btn-sm ms-2">
              <i class="fas fa-redo me-1"></i>
              Retry
            </button>
          </div>

          <!-- Statistics Content -->
          <div v-else>
            <!-- Overview Cards -->
            <div class="row mb-4">
              <div class="col-xl-3 col-lg-6 mb-3">
                <div class="card bg-primary bg-gradient text-white h-100">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h6 class="card-title text-white-50">Total Users</h6>
                        <h3 class="mb-0">{{ statistics.users?.total || 0 }}</h3>
                      </div>
                      <i class="fas fa-users fa-2x opacity-75"></i>
                    </div>
                    <div class="mt-2">
                      <small class="text-white-50">{{ statistics.users?.active || 0 }} active</small>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-xl-3 col-lg-6 mb-3">
                <div class="card bg-success bg-gradient text-white h-100">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h6 class="card-title text-white-50">Parking Lots</h6>
                        <h3 class="mb-0">{{ statistics.parking_lots?.total || 0 }}</h3>
                      </div>
                      <i class="fas fa-building fa-2x opacity-75"></i>
                    </div>
                    <div class="mt-2">
                      <small class="text-white-50">{{ statistics.parking_lots?.active || 0 }} active</small>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-xl-3 col-lg-6 mb-3">
                <div class="card bg-warning bg-gradient text-white h-100">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h6 class="card-title text-white-50">Parking Spots</h6>
                        <h3 class="mb-0">{{ statistics.parking_spots?.total || 0 }}</h3>
                      </div>
                      <i class="fas fa-parking fa-2x opacity-75"></i>
                    </div>
                    <div class="mt-2">
                      <small class="text-white-50">{{ statistics.parking_spots?.available || 0 }} available</small>
                    </div>
                  </div>
                </div>
              </div>

              <div class="col-xl-3 col-lg-6 mb-3">
                <div class="card bg-info bg-gradient text-white h-100">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h6 class="card-title text-white-50">Total Revenue</h6>
                        <h3 class="mb-0">₹{{ statistics.revenue?.total || 0 }}</h3>
                      </div>
                      <i class="fas fa-rupee-sign fa-2x opacity-75"></i>
                    </div>
                    <div class="mt-2">
                      <small class="text-white-50">{{ statistics.reservations?.completed || 0 }} completed bookings</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Detailed Analytics -->
            <div class="row">
              <!-- Reservations Overview -->
              <div class="col-lg-6 mb-4">
                <div class="card h-100">
                  <div class="card-header bg-primary text-white">
                    <h6 class="mb-0">
                      <i class="fas fa-calendar-check me-2"></i>
                      Reservations Overview
                    </h6>
                  </div>
                  <div class="card-body">
                    <div class="row g-3">
                      <div class="col-6">
                        <div class="text-center p-3 bg-light rounded">
                          <h4 class="mb-1 text-primary">{{ statistics.reservations?.total || 0 }}</h4>
                          <small class="text-muted">Total Reservations</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-center p-3 bg-success bg-gradient text-white rounded">
                          <h4 class="mb-1">{{ statistics.reservations?.active || 0 }}</h4>
                          <small class="text-white-50">Active</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-center p-3 bg-info bg-gradient text-white rounded">
                          <h4 class="mb-1">{{ statistics.reservations?.completed || 0 }}</h4>
                          <small class="text-white-50">Completed</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-center p-3 bg-danger bg-gradient text-white rounded">
                          <h4 class="mb-1">{{ statistics.reservations?.cancelled || 0 }}</h4>
                          <small class="text-white-50">Cancelled</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- System Occupancy -->
              <div class="col-lg-6 mb-4">
                <div class="card h-100">
                  <div class="card-header bg-warning text-white">
                    <h6 class="mb-0">
                      <i class="fas fa-chart-pie me-2"></i>
                      System Occupancy
                    </h6>
                  </div>
                  <div class="card-body">
                    <div class="text-center mb-4">
                      <div class="d-flex justify-content-center align-items-center mb-3">
                        <div class="position-relative">
                          <canvas id="occupancyChart" width="120" height="120"></canvas>
                          <div class="position-absolute top-50 start-50 translate-middle text-center">
                            <h3 class="mb-0 fw-bold">{{ statistics.parking_spots?.occupancy_rate || 0 }}%</h3>
                            <small class="text-muted">Occupied</small>
                          </div>
                        </div>
                      </div>
                      
                      <!-- Progress bar alternative -->
                      <div class="mb-3">
                        <div class="d-flex justify-content-between mb-1">
                          <small class="text-muted">Current Occupancy Rate</small>
                          <small class="fw-bold">{{ statistics.parking_spots?.occupancy_rate || 0 }}%</small>
                        </div>
                        <div class="progress" style="height: 8px;">
                          <div 
                            class="progress-bar"
                            :class="getOccupancyColor(statistics.parking_spots?.occupancy_rate || 0)"
                            :style="{ width: `${statistics.parking_spots?.occupancy_rate || 0}%` }"
                          ></div>
                        </div>
                      </div>
                    </div>

                    <div class="row g-2">
                      <div class="col-6">
                        <div class="text-center p-2 bg-success bg-gradient text-white rounded">
                          <h5 class="mb-0">{{ statistics.parking_spots?.available || 0 }}</h5>
                          <small>Available</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-center p-2 bg-danger bg-gradient text-white rounded">
                          <h5 class="mb-0">{{ statistics.parking_spots?.occupied || 0 }}</h5>
                          <small>Occupied</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- User & Revenue Analytics -->
            <div class="row">
              <!-- User Analytics -->
              <div class="col-lg-6 mb-4">
                <div class="card h-100">
                  <div class="card-header bg-success text-white">
                    <h6 class="mb-0">
                      <i class="fas fa-users me-2"></i>
                      User Analytics
                    </h6>
                  </div>
                  <div class="card-body">
                    <div class="row g-3">
                      <div class="col-12">
                        <div class="d-flex justify-content-between align-items-center p-3 bg-light rounded">
                          <div>
                            <h5 class="mb-0 text-primary">{{ statistics.users?.total || 0 }}</h5>
                            <small class="text-muted">Total Users</small>
                          </div>
                          <div class="text-end">
                            <div class="text-success fw-bold">{{ statistics.users?.active || 0 }}</div>
                            <small class="text-muted">Active</small>
                          </div>
                        </div>
                      </div>
                      <div class="col-12">
                        <div class="d-flex justify-content-between align-items-center p-3 bg-light rounded">
                          <div>
                            <h6 class="mb-0">Active Rate</h6>
                            <small class="text-muted">User engagement</small>
                          </div>
                          <div class="text-end">
                            <span class="badge bg-success fs-6">
                              {{ Math.round(((statistics.users?.active || 0) / Math.max(statistics.users?.total || 1, 1)) * 100) }}%
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Revenue Analytics -->
              <div class="col-lg-6 mb-4">
                <div class="card h-100">
                  <div class="card-header bg-info text-white">
                    <h6 class="mb-0">
                      <i class="fas fa-chart-line me-2"></i>
                      Revenue Analytics
                    </h6>
                  </div>
                  <div class="card-body">
                    <div class="row g-3">
                      <div class="col-12">
                        <div class="text-center p-3 bg-light rounded">
                          <h3 class="mb-1 text-success">₹{{ statistics.revenue?.total || 0 }}</h3>
                          <small class="text-muted">Total Revenue Generated</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-center p-2 bg-primary bg-gradient text-white rounded">
                          <h6 class="mb-0">{{ statistics.reservations?.completed || 0 }}</h6>
                          <small>Bookings</small>
                        </div>
                      </div>
                      <div class="col-6">
                        <div class="text-center p-2 bg-warning bg-gradient text-white rounded">
                          <h6 class="mb-0">₹{{ Math.round((statistics.revenue?.total || 0) / Math.max(statistics.reservations?.completed || 1, 1)) }}</h6>
                          <small>Avg/Booking</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- System Health -->
            <div class="row">
              <div class="col-12">
                <div class="card">
                  <div class="card-header bg-dark text-white">
                    <div class="d-flex justify-content-between align-items-center">
                      <h6 class="mb-0">
                        <i class="fas fa-heartbeat me-2"></i>
                        System Health Overview
                      </h6>
                      <small class="text-white-50">Last updated: {{ new Date().toLocaleString() }}</small>
                    </div>
                  </div>
                  <div class="card-body">
                    <div class="row g-3">
                      <div class="col-lg-3 col-md-6">
                        <div class="d-flex align-items-center p-3 bg-success bg-gradient text-white rounded">
                          <i class="fas fa-server fa-2x me-3"></i>
                          <div>
                            <h6 class="mb-0">System Status</h6>
                            <small>Operational</small>
                          </div>
                        </div>
                      </div>
                      <div class="col-lg-3 col-md-6">
                        <div class="d-flex align-items-center p-3 bg-info bg-gradient text-white rounded">
                          <i class="fas fa-database fa-2x me-3"></i>
                          <div>
                            <h6 class="mb-0">Database</h6>
                            <small>Connected</small>
                          </div>
                        </div>
                      </div>
                      <div class="col-lg-3 col-md-6">
                        <div class="d-flex align-items-center p-3 bg-warning bg-gradient text-white rounded">
                          <i class="fas fa-wifi fa-2x me-3"></i>
                          <div>
                            <h6 class="mb-0">Network</h6>
                            <small>Stable</small>
                          </div>
                        </div>
                      </div>
                      <div class="col-lg-3 col-md-6">
                        <div class="d-flex align-items-center p-3 bg-primary bg-gradient text-white rounded">
                          <i class="fas fa-users fa-2x me-3"></i>
                          <div>
                            <h6 class="mb-0">Active Sessions</h6>
                            <small>{{ statistics.users?.active || 0 }} users</small>
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
      </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI, authAPI } from '../../services/api'

export default {
  name: 'SystemStats',
  setup() {
    const router = useRouter()
    
    // Reactive data
    const loading = ref(true)
    const error = ref('')
    const statistics = ref({})

    // Methods
    const loadStatistics = async () => {
      try {
        loading.value = true
        error.value = ''

        const response = await adminAPI.getStatistics()
        
        if (response.data.success) {
          statistics.value = response.data.data
        } else {
          error.value = response.data.message
        }
      } catch (err) {
        error.value = err.response?.data?.message || 'Failed to load statistics'
      } finally {
        loading.value = false
      }
    }
    
    const getOccupancyColor = (rate) => {
      if (rate < 50) return 'bg-success'
      if (rate < 80) return 'bg-warning'
      return 'bg-danger'
    }
    


    // Lifecycle
    onMounted(() => {
      loadStatistics()
    })

    return {
      loading,
      error,
      statistics,
      loadStatistics,
      getOccupancyColor
    }
  }
}
</script>

<style scoped>
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
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.bg-gradient {
  background-image: linear-gradient(180deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0));
}

.progress {
  background-color: #e9ecef;
}

/* Custom animations */
@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

.card-header {
  position: relative;
  overflow: hidden;
}

.card-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.card:hover .card-header::before {
  left: 100%;
}

.fa-spin {
  animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style> 