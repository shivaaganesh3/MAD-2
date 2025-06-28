<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/admin/dashboard" class="flex items-center">
              <div class="h-8 w-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                </svg>
              </div>
              <h1 class="ml-3 text-xl font-semibold text-gray-900">User Manager</h1>
            </router-link>
          </div>
          
          <div class="flex items-center space-x-4">
            <router-link to="/admin/dashboard" class="text-gray-500 hover:text-gray-700">
              ← Back to Dashboard
            </router-link>
            <button
              @click="handleLogout"
              class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Header Section -->
      <div class="md:flex md:items-center md:justify-between mb-6">
        <div class="flex-1 min-w-0">
          <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl">Users</h2>
          <p class="mt-1 text-sm text-gray-500">Manage user accounts and monitor activity</p>
        </div>
      </div>

      <!-- Search and Filters -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <label class="block text-sm font-medium text-gray-700">Search</label>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by username, email, or name..."
                class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Status</label>
              <select
                v-model="statusFilter"
                class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
              >
                <option value="all">All Status</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <div class="flex items-end">
              <button
                @click="loadUsers"
                class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
                Search
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error loading users</h3>
            <p class="mt-2 text-sm text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Users Table -->
      <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
        <ul class="divide-y divide-gray-200">
          <li v-for="user in users" :key="user.id" class="px-6 py-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <!-- Avatar -->
                <div class="flex-shrink-0 h-12 w-12">
                  <div class="h-12 w-12 rounded-full bg-gray-300 flex items-center justify-center">
                    <svg class="h-6 w-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                  </div>
                </div>
                
                <!-- User Info -->
                <div class="ml-4">
                  <div class="flex items-center">
                    <div class="text-sm font-medium text-gray-900">{{ user.full_name }}</div>
                    <span
                      :class="user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                      class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    >
                      {{ user.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                  <div class="text-sm text-gray-500">@{{ user.username }} • {{ user.email }}</div>
                  <div class="text-sm text-gray-500">{{ user.phone_number }}</div>
                </div>
              </div>
              
              <!-- Statistics -->
              <div class="hidden md:flex md:items-center md:space-x-8">
                <div class="text-center">
                  <div class="text-lg font-semibold text-gray-900">{{ user.statistics.total_reservations }}</div>
                  <div class="text-xs text-gray-500">Total Bookings</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-semibold text-green-600">{{ user.statistics.active_reservations }}</div>
                  <div class="text-xs text-gray-500">Active</div>
                </div>
                <div class="text-center">
                  <div class="text-lg font-semibold text-gray-900">₹{{ user.statistics.total_spent }}</div>
                  <div class="text-xs text-gray-500">Total Spent</div>
                </div>
              </div>
              
              <!-- Actions -->
              <div class="flex items-center space-x-2">
                <button
                  @click="viewUserDetails(user)"
                  class="bg-indigo-50 text-indigo-700 hover:bg-indigo-100 px-3 py-1 rounded-md text-sm font-medium"
                >
                  View Details
                </button>
                <button
                  @click="toggleUserStatus(user)"
                  :class="user.is_active ? 'bg-red-50 text-red-700 hover:bg-red-100' : 'bg-green-50 text-green-700 hover:bg-green-100'"
                  class="px-3 py-1 rounded-md text-sm font-medium"
                >
                  {{ user.is_active ? 'Deactivate' : 'Activate' }}
                </button>
              </div>
            </div>
            
            <!-- Current Reservation -->
            <div v-if="user.current_reservation" class="mt-4 bg-yellow-50 border border-yellow-200 rounded-md p-3">
              <div class="flex items-center">
                <svg class="h-5 w-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"></path>
                </svg>
                <div class="ml-3">
                  <h4 class="text-sm font-medium text-yellow-800">Currently Parked</h4>
                  <p class="text-sm text-yellow-700">
                    Spot {{ user.current_reservation.spot_number }} at {{ user.current_reservation.lot_name }} • 
                    {{ user.current_reservation.vehicle_number }} • 
                    {{ Math.floor(user.current_reservation.duration_minutes / 60) }}h {{ user.current_reservation.duration_minutes % 60 }}m
                  </p>
                </div>
              </div>
            </div>
            
            <!-- Mobile Statistics -->
            <div class="mt-4 grid grid-cols-3 gap-4 md:hidden">
              <div class="text-center">
                <div class="text-lg font-semibold text-gray-900">{{ user.statistics.total_reservations }}</div>
                <div class="text-xs text-gray-500">Bookings</div>
              </div>
              <div class="text-center">
                <div class="text-lg font-semibold text-green-600">{{ user.statistics.active_reservations }}</div>
                <div class="text-xs text-gray-500">Active</div>
              </div>
              <div class="text-center">
                <div class="text-lg font-semibold text-gray-900">₹{{ user.statistics.total_spent }}</div>
                <div class="text-xs text-gray-500">Spent</div>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && users.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No users found</h3>
        <p class="mt-1 text-sm text-gray-500">No users match your search criteria.</p>
      </div>

      <!-- Pagination -->
      <div v-if="pagination && pagination.pages > 1" class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6 mt-6 rounded-lg shadow">
        <div class="flex-1 flex justify-between sm:hidden">
          <button
            @click="changePage(pagination.page - 1)"
            :disabled="!pagination.has_prev"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>
          <button
            @click="changePage(pagination.page + 1)"
            :disabled="!pagination.has_next"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
          >
            Next
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Showing {{ (pagination.page - 1) * pagination.per_page + 1 }} to 
              {{ Math.min(pagination.page * pagination.per_page, pagination.total) }} of 
              {{ pagination.total }} results
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
              <button
                @click="changePage(pagination.page - 1)"
                :disabled="!pagination.has_prev"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
              >
                Previous
              </button>
              <button
                @click="changePage(pagination.page + 1)"
                :disabled="!pagination.has_next"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
              >
                Next
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- User Details Modal -->
    <div v-if="showUserModal" class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900">User Details</h3>
              <button
                @click="showUserModal = false"
                class="bg-white rounded-md text-gray-400 hover:text-gray-600"
              >
                <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
            
            <div v-if="selectedUser" class="space-y-6">
              <!-- User Info -->
              <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Full Name</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedUser.full_name }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Username</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedUser.username }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Email</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedUser.email }}</p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Phone</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedUser.phone_number }}</p>
                </div>
                <div class="sm:col-span-2">
                  <label class="block text-sm font-medium text-gray-700">Address</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedUser.address || 'Not provided' }}</p>
                </div>
              </div>
              
              <!-- Statistics -->
              <div>
                <h4 class="text-lg font-medium text-gray-900 mb-4">Statistics</h4>
                <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
                  <div class="text-center p-4 bg-gray-50 rounded-lg">
                    <div class="text-2xl font-bold text-gray-900">{{ selectedUser.statistics.total_reservations }}</div>
                    <div class="text-sm text-gray-500">Total Bookings</div>
                  </div>
                  <div class="text-center p-4 bg-green-50 rounded-lg">
                    <div class="text-2xl font-bold text-green-600">{{ selectedUser.statistics.completed_reservations }}</div>
                    <div class="text-sm text-gray-500">Completed</div>
                  </div>
                  <div class="text-center p-4 bg-yellow-50 rounded-lg">
                    <div class="text-2xl font-bold text-yellow-600">{{ selectedUser.statistics.active_reservations }}</div>
                    <div class="text-sm text-gray-500">Active</div>
                  </div>
                  <div class="text-center p-4 bg-blue-50 rounded-lg">
                    <div class="text-2xl font-bold text-blue-600">₹{{ selectedUser.statistics.total_spent }}</div>
                    <div class="text-sm text-gray-500">Total Spent</div>
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
import { adminAPI, authAPI } from '../../services/api'

export default {
  name: 'UserManager',
  data() {
    return {
      loading: true,
      error: '',
      users: [],
      pagination: null,
      searchQuery: '',
      statusFilter: 'all',
      currentPage: 1,
      perPage: 10,
      
      // Modals
      showUserModal: false,
      selectedUser: null
    }
  },
  async mounted() {
    await this.loadUsers()
  },
  methods: {
    async loadUsers() {
      try {
        this.loading = true
        this.error = ''

        const params = {
          page: this.currentPage,
          per_page: this.perPage,
          search: this.searchQuery,
          status: this.statusFilter
        }

        const response = await adminAPI.getUsers(params)
        
        if (response.data.success) {
          this.users = response.data.data.users
          this.pagination = response.data.data.pagination
        } else {
          this.error = response.data.message
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load users'
      } finally {
        this.loading = false
      }
    },
    
    changePage(page) {
      if (page >= 1 && page <= this.pagination.pages) {
        this.currentPage = page
        this.loadUsers()
      }
    },
    
    async viewUserDetails(user) {
      try {
        const response = await adminAPI.getUser(user.id)
        if (response.data.success) {
          this.selectedUser = response.data.data
          this.showUserModal = true
        }
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to load user details')
      }
    },
    
    async toggleUserStatus(user) {
      const action = user.is_active ? 'deactivate' : 'activate'
      if (!confirm(`Are you sure you want to ${action} user "${user.username}"?`)) {
        return
      }
      
      try {
        const response = await adminAPI.toggleUserStatus(user.id)
        if (response.data.success) {
          alert(response.data.message)
          this.loadUsers()
        } else {
          alert(response.data.message)
        }
      } catch (err) {
        alert(err.response?.data?.message || `Failed to ${action} user`)
      }
    },
    
    async handleLogout() {
      try {
        await authAPI.logout()
        this.$router.push('/login')
      } catch (err) {
        console.error('Logout failed:', err)
        this.$router.push('/login')
      }
    }
  }
}
</script> 