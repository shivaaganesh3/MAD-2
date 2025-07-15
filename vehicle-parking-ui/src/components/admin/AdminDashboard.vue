<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom">
      <div>
        <h1 class="h3 mb-1 fw-bold text-dark">
          <i class="fas fa-crown me-2 text-warning"></i>Admin Dashboard
        </h1>
        <p class="text-muted mb-0">Welcome back, {{ user?.username || 'Admin' }}! Manage your parking system.</p>
      </div>
      <div class="d-flex align-items-center gap-2">
        <span class="badge bg-warning-subtle text-warning px-3 py-2">
          <i class="fas fa-crown me-1"></i>{{ user?.username || 'Admin' }}
        </span>
        <button @click="refreshData" class="btn btn-outline-primary btn-sm">
          <i class="fas fa-sync-alt me-1"></i>Refresh
        </button>
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
      <!-- Admin Statistics Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-6 col-xl-3">
          <div class="card border-0 shadow-sm h-100 stat-card bg-primary text-white">
            <div class="card-body d-flex align-items-center">
              <div class="flex-fill">
                <h3 class="mb-1 fw-bold">{{ statistics.users?.total || 0 }}</h3>
                <p class="mb-0 opacity-75">Total Users</p>
              </div>
              <div class="stat-icon">
                <i class="fas fa-users fa-2x opacity-75"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-xl-3">
          <div class="card border-0 shadow-sm h-100 stat-card bg-success text-white">
            <div class="card-body d-flex align-items-center">
              <div class="flex-fill">
                <h3 class="mb-1 fw-bold">{{ statistics.parking_lots?.total || 0 }}</h3>
                <p class="mb-0 opacity-75">Parking Lots</p>
              </div>
              <div class="stat-icon">
                <i class="fas fa-building fa-2x opacity-75"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-xl-3">
          <div class="card border-0 shadow-sm h-100 stat-card bg-warning text-white">
            <div class="card-body d-flex align-items-center">
              <div class="flex-fill">
                <h3 class="mb-1 fw-bold">{{ statistics.parking_spots?.available || 0 }}</h3>
                <p class="mb-0 opacity-75">Available Spots</p>
              </div>
              <div class="stat-icon">
                <i class="fas fa-parking fa-2x opacity-75"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-xl-3">
          <div class="card border-0 shadow-sm h-100 stat-card bg-info text-white">
            <div class="card-body d-flex align-items-center">
              <div class="flex-fill">
                <h3 class="mb-1 fw-bold">₹{{ statistics.revenue?.total || 0 }}</h3>
                <p class="mb-0 opacity-75">Total Revenue</p>
              </div>
              <div class="stat-icon">
                <i class="fas fa-rupee-sign fa-2x opacity-75"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- System Status Alert -->
      <div v-if="statistics.system_status" class="alert alert-success border-0 shadow-sm mb-4" role="alert">
        <div class="d-flex align-items-start">
          <div class="me-3">
            <i class="fas fa-check-circle fa-2x text-success"></i>
          </div>
          <div class="flex-fill">
            <h5 class="alert-heading mb-2">
              <i class="fas fa-circle text-success me-2" style="font-size: 0.5rem;"></i>
              System Status: Online
            </h5>
            <div class="row align-items-center">
              <div class="col-lg-8">
                <p class="mb-2">
                  <strong class="text-dark">All systems operational</strong>
                  <span class="badge bg-success-subtle text-success ms-2">{{ statistics.users?.active || 0 }} Active Users</span>
                </p>
                <div class="small text-muted mb-2">
                  <div class="d-flex flex-wrap gap-3">
                    <span><i class="fas fa-server me-1"></i>Server: Healthy</span>
                    <span><i class="fas fa-database me-1"></i>Database: Connected</span>
                    <span><i class="fas fa-wifi me-1"></i>API: Responsive</span>
                  </div>
                </div>
                <p class="mb-0 small text-muted">
                  <i class="fas fa-clock me-1"></i>Last updated: {{ new Date().toLocaleString() }}
                </p>
              </div>
              <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
                <button @click="loadDashboard" class="btn btn-success btn-lg px-4">
                  <i class="fas fa-sync-alt me-2"></i>Refresh Status
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <!-- Quick Actions -->
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center py-3">
              <h5 class="mb-0 fw-bold">
                <i class="fas fa-bolt me-2 text-primary"></i>Quick Actions
              </h5>
              <span class="badge bg-primary-subtle text-primary">Management Tools</span>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <router-link to="/admin/parking-lots" class="text-decoration-none">
                    <div class="quick-action-card p-3 rounded border h-100 d-flex align-items-center">
                      <div class="action-icon me-3">
                        <i class="fas fa-building fa-2x text-primary"></i>
                      </div>
                      <div class="flex-fill">
                        <h6 class="mb-1 fw-bold">Manage Parking Lots</h6>
                        <p class="mb-0 small text-muted">Create, edit, and manage parking locations</p>
                      </div>
                      <i class="fas fa-chevron-right text-muted"></i>
                    </div>
                  </router-link>
                </div>
                <div class="col-md-6">
                  <router-link to="/admin/users" class="text-decoration-none">
                    <div class="quick-action-card p-3 rounded border h-100 d-flex align-items-center">
                      <div class="action-icon me-3">
                        <i class="fas fa-users fa-2x text-success"></i>
                      </div>
                      <div class="flex-fill">
                        <h6 class="mb-1 fw-bold">Manage Users</h6>
                        <p class="mb-0 small text-muted">View and manage user accounts</p>
                      </div>
                      <i class="fas fa-chevron-right text-muted"></i>
                    </div>
                  </router-link>
                </div>
                <div class="col-md-6">
                  <router-link to="/admin/reservations" class="text-decoration-none">
                    <div class="quick-action-card p-3 rounded border h-100 d-flex align-items-center">
                      <div class="action-icon me-3">
                        <i class="fas fa-clipboard-list fa-2x text-warning"></i>
                      </div>
                      <div class="flex-fill">
                        <h6 class="mb-1 fw-bold">View Reservations</h6>
                        <p class="mb-0 small text-muted">Monitor all parking reservations</p>
                      </div>
                      <i class="fas fa-chevron-right text-muted"></i>
                    </div>
                  </router-link>
                </div>
                <div class="col-md-6">
                  <router-link to="/admin/analytics" class="text-decoration-none">
                    <div class="quick-action-card p-3 rounded border h-100 d-flex align-items-center">
                      <div class="action-icon me-3">
                        <i class="fas fa-chart-line fa-2x text-info"></i>
                      </div>
                      <div class="flex-fill">
                        <h6 class="mb-1 fw-bold">Analytics & Reports</h6>
                        <p class="mb-0 small text-muted">View trends and system insights</p>
                      </div>
                      <i class="fas fa-chevron-right text-muted"></i>
                    </div>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="col-lg-4">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center py-3">
              <h5 class="mb-0 fw-bold">
                <i class="fas fa-activity me-2 text-primary"></i>Recent Activity
              </h5>
              <router-link to="/admin/reservations" class="btn btn-outline-primary btn-sm">
                <i class="fas fa-external-link-alt me-1"></i>View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="!statistics.recent_activity || statistics.recent_activity.length === 0" class="text-center py-4">
                <i class="fas fa-chart-line text-muted fa-2x mb-3"></i>
                <h6 class="text-muted">No Recent Activity</h6>
                <p class="text-muted mb-0 small">System activity will appear here.</p>
              </div>
              <div v-else class="recent-activity">
                <div 
                  v-for="(activity, index) in (statistics.recent_activity || []).slice(0, 5)" 
                  :key="index"
                  class="activity-item p-2 rounded mb-2"
                  :class="{'border-bottom': index < Math.min((statistics.recent_activity || []).length, 5) - 1}"
                >
                  <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-fill">
                      <h6 class="mb-1 small fw-medium">{{ activity.type || 'System Event' }}</h6>
                      <p class="mb-1 small text-muted">{{ activity.description || 'Recent system activity' }}</p>
                      <small class="text-muted">
                        <i class="fas fa-clock me-1"></i>{{ activity.timestamp || 'Just now' }}
                      </small>
                    </div>
                    <span class="badge bg-primary-subtle text-primary small">New</span>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI, authAPI, authHelpers } from '../../services/api'

export default {
  name: 'AdminDashboard',
  setup() {
    const router = useRouter()
    
    // Reactive data
    const loading = ref(true)
    const error = ref('')
    const statistics = ref({})
    const user = ref({ username: 'Admin' })

    // Computed properties
    const currentUser = computed(() => authHelpers.getCurrentUser())

    // Load dashboard data
    const loadDashboard = async () => {
      try {
        loading.value = true
        error.value = ''

        const [statsResponse, profileResponse] = await Promise.all([
          adminAPI.getStatistics(),
          authAPI.getProfile()
        ])

        if (statsResponse.data.success) {
          statistics.value = statsResponse.data.data
          // Set system_status to true by default for the status alert
          statistics.value.system_status = true
        }

        if (profileResponse.data.success) {
          user.value = profileResponse.data.user
        }
      } catch (err) {
        console.error('Error loading dashboard:', err)
        error.value = err.response?.data?.message || 'Failed to load dashboard'
      } finally {
        loading.value = false
      }
    }

    // Refresh data
    const refreshData = () => {
      loadDashboard()
    }

    // Logout functionality
    const handleLogout = async () => {
      try {
        await authAPI.logout()
        router.push('/login')
      } catch (err) {
        console.error('Logout failed:', err)
        router.push('/login')
      }
    }

    // Load data on component mount
    onMounted(() => {
      loadDashboard()
    })

    return {
      loading,
      error,
      statistics,
      user,
      currentUser,
      loadDashboard,
      refreshData,
      handleLogout
    }
  }
}
</script> 

<style scoped>
/* Admin Dashboard Bootstrap Styling */
.admin-dashboard {
  padding: 0;
  background: #f8f9fa;
}

/* Custom stat card styling */
.stat-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
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

/* Quick action cards */
.quick-action-card {
  transition: all 0.2s ease;
  border: 1px solid #dee2e6 !important;
}

.quick-action-card:hover {
  background-color: #f8f9fa;
  border-color: #667eea !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.action-icon {
  transition: all 0.2s ease;
}

.quick-action-card:hover .action-icon {
  transform: scale(1.1);
}

/* Activity item hover effect */
.activity-item:hover {
  background-color: #f8f9fa;
}

/* Alert customization */
.alert {
  border: none;
  border-radius: 12px;
}

.alert-success {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border-left: 4px solid #28a745;
}

/* Badge enhancements */
.badge {
  font-weight: 500;
  font-size: 0.75rem;
  padding: 0.5rem 0.75rem;
}

/* Header styling */
.border-bottom {
  border-color: #e9ecef !important;
}

/* Card header styling */
.card-header {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border-bottom: 1px solid #e9ecef;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .quick-action-card {
    text-align: center;
  }
  
  .quick-action-card .d-flex {
    flex-direction: column;
    align-items: center !important;
    gap: 0.75rem;
  }
  
  .activity-item .d-flex {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 0.5rem;
  }
}

/* Border utilities */
.border-bottom:last-child {
  border-bottom: none !important;
}

/* Custom focus styles */
.btn:focus {
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Loading spinner customization */
.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* System status styling */
.alert-success .fas.fa-check-circle {
  color: #28a745;
}

/* Stat card specific colors */
.stat-card.bg-primary {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%) !important;
}

.stat-card.bg-success {
  background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%) !important;
}

.stat-card.bg-warning {
  background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%) !important;
}

.stat-card.bg-info {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%) !important;
}

/* Text shadow for better readability on colored backgrounds */
.stat-card h3,
.stat-card p {
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Quick action card link styling */
.quick-action-card h6 {
  color: #495057;
  margin-bottom: 0.25rem;
}

.quick-action-card:hover h6 {
  color: #667eea;
}

/* Activity styling */
.recent-activity .activity-item {
  border-radius: 8px;
  transition: background-color 0.2s ease;
}
</style> 