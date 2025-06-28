<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header with Navigation -->
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/admin/dashboard" class="flex items-center">
              <div class="h-8 w-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H7m2 0v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0V9a2 2 0 012-2h2a2 2 0 012 2v6.01"></path>
                </svg>
              </div>
              <h1 class="ml-3 text-xl font-semibold text-gray-900">Parking Lot Manager</h1>
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
          <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl">Parking Lots</h2>
          <p class="mt-1 text-sm text-gray-500">Manage parking lots and their spots</p>
        </div>
        <div class="mt-4 flex md:mt-0 md:ml-4">
          <button
            @click="showCreateModal = true"
            class="ml-3 inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Add Parking Lot
          </button>
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
                placeholder="Search by name, address, or pin code..."
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
                @click="loadParkingLots"
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
            <h3 class="text-sm font-medium text-red-800">Error loading parking lots</h3>
            <p class="mt-2 text-sm text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Parking Lots Grid -->
      <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="lot in parkingLots"
          :key="lot.id"
          class="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow"
        >
          <div class="px-4 py-5 sm:p-6">
            <!-- Header -->
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-medium text-gray-900 truncate">{{ lot.prime_location_name }}</h3>
              <div class="flex items-center space-x-2">
                <span
                  :class="lot.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                >
                  {{ lot.is_active ? 'Active' : 'Inactive' }}
                </span>
              </div>
            </div>

            <!-- Details -->
            <div class="space-y-2">
              <p class="text-sm text-gray-600">
                <svg class="inline h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                {{ lot.address }}
              </p>
              <p class="text-sm text-gray-600">
                <svg class="inline h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                </svg>
                Pin: {{ lot.pin_code }}
              </p>
              <p class="text-sm text-gray-600">
                <svg class="inline h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                </svg>
                ₹{{ lot.price_per_hour }}/hour
              </p>
            </div>

            <!-- Statistics -->
            <div class="mt-4 grid grid-cols-2 gap-4">
              <div class="text-center">
                <div class="text-2xl font-bold text-gray-900">{{ lot.number_of_spots }}</div>
                <div class="text-xs text-gray-500">Total Spots</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-green-600">{{ lot.available_spots }}</div>
                <div class="text-xs text-gray-500">Available</div>
              </div>
            </div>

            <!-- Occupancy Bar -->
            <div class="mt-4">
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-600">Occupancy</span>
                <span class="font-medium">{{ lot.occupancy_rate }}%</span>
              </div>
              <div class="mt-1 w-full bg-gray-200 rounded-full h-2">
                <div
                  :class="getOccupancyColor(lot.occupancy_rate)"
                  class="h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${lot.occupancy_rate}%` }"
                ></div>
              </div>
            </div>

            <!-- Revenue -->
            <div class="mt-4 pt-4 border-t border-gray-200">
              <div class="flex justify-between items-center">
                <span class="text-sm text-gray-600">Total Revenue</span>
                <span class="text-lg font-semibold text-gray-900">₹{{ lot.total_revenue }}</span>
              </div>
            </div>

            <!-- Actions -->
            <div class="mt-6 flex space-x-2">
              <button
                @click="viewLotDetails(lot)"
                class="flex-1 bg-indigo-50 text-indigo-700 hover:bg-indigo-100 px-3 py-2 rounded-md text-sm font-medium"
              >
                View Details
              </button>
              <button
                @click="editLot(lot)"
                class="flex-1 bg-green-50 text-green-700 hover:bg-green-100 px-3 py-2 rounded-md text-sm font-medium"
              >
                Edit
              </button>
              <button
                @click="deleteLot(lot)"
                class="bg-red-50 text-red-700 hover:bg-red-100 px-3 py-2 rounded-md text-sm font-medium"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && parkingLots.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H7m2 0v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0V9a2 2 0 012-2h2a2 2 0 012 2v6.01"></path>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No parking lots</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by creating a new parking lot.</p>
        <div class="mt-6">
          <button
            @click="showCreateModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Add Parking Lot
          </button>
        </div>
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

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="fixed inset-0 z-10 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <form @submit.prevent="submitForm">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                {{ showCreateModal ? 'Create Parking Lot' : 'Edit Parking Lot' }}
              </h3>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Location Name *</label>
                  <input
                    v-model="lotForm.prime_location_name"
                    type="text"
                    required
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    placeholder="e.g., City Center Mall"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">Address *</label>
                  <textarea
                    v-model="lotForm.address"
                    required
                    rows="3"
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    placeholder="Full address..."
                  ></textarea>
                </div>
                
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Pin Code *</label>
                    <input
                      v-model="lotForm.pin_code"
                      type="text"
                      required
                      pattern="[0-9]{6}"
                      maxlength="6"
                      class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                      placeholder="110001"
                    />
                  </div>
                  
                  <div>
                    <label class="block text-sm font-medium text-gray-700">Price per Hour *</label>
                    <input
                      v-model="lotForm.price_per_hour"
                      type="number"
                      required
                      min="1"
                      max="10000"
                      step="0.01"
                      class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                      placeholder="50"
                    />
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">Number of Spots *</label>
                  <input
                    v-model="lotForm.number_of_spots"
                    type="number"
                    required
                    min="1"
                    max="1000"
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    placeholder="50"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700">Description</label>
                  <textarea
                    v-model="lotForm.description"
                    rows="2"
                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    placeholder="Optional description..."
                  ></textarea>
                </div>
                
                <div class="flex items-center">
                  <input
                    v-model="lotForm.is_active"
                    type="checkbox"
                    class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
                  />
                  <label class="ml-2 block text-sm text-gray-900">Active</label>
                </div>
              </div>
            </div>
            
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button
                type="submit"
                :disabled="submitting"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
              >
                {{ submitting ? 'Saving...' : (showCreateModal ? 'Create' : 'Update') }}
              </button>
              <button
                type="button"
                @click="closeModal"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAPI, authAPI } from '../../services/api'

export default {
  name: 'ParkingLotManager',
  data() {
    return {
      loading: true,
      error: '',
      parkingLots: [],
      pagination: null,
      searchQuery: '',
      statusFilter: 'all',
      currentPage: 1,
      perPage: 9,
      
      // Modals
      showCreateModal: false,
      showEditModal: false,
      submitting: false,
      editingLot: null,
      
      // Form
      lotForm: {
        prime_location_name: '',
        address: '',
        pin_code: '',
        price_per_hour: '',
        number_of_spots: '',
        description: '',
        is_active: true
      }
    }
  },
  async mounted() {
    await this.loadParkingLots()
  },
  methods: {
    async loadParkingLots() {
      try {
        this.loading = true
        this.error = ''

        const params = {
          page: this.currentPage,
          per_page: this.perPage,
          search: this.searchQuery,
          status: this.statusFilter
        }

        const response = await adminAPI.getParkingLots(params)
        
        if (response.data.success) {
          this.parkingLots = response.data.data.parking_lots
          this.pagination = response.data.data.pagination
        } else {
          this.error = response.data.message
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load parking lots'
      } finally {
        this.loading = false
      }
    },
    
    getOccupancyColor(rate) {
      if (rate < 50) return 'bg-green-500'
      if (rate < 80) return 'bg-yellow-500'
      return 'bg-red-500'
    },
    
    changePage(page) {
      if (page >= 1 && page <= this.pagination.pages) {
        this.currentPage = page
        this.loadParkingLots()
      }
    },
    
    editLot(lot) {
      this.editingLot = lot
      this.lotForm = { ...lot }
      this.showEditModal = true
    },
    
    async deleteLot(lot) {
      if (!confirm(`Are you sure you want to delete "${lot.prime_location_name}"? This action cannot be undone.`)) {
        return
      }
      
      try {
        const response = await adminAPI.deleteParkingLot(lot.id)
        if (response.data.success) {
          alert('Parking lot deleted successfully')
          this.loadParkingLots()
        } else {
          alert(response.data.message)
        }
      } catch (err) {
        alert(err.response?.data?.message || 'Failed to delete parking lot')
      }
    },
    
    viewLotDetails(lot) {
      // Navigate to detailed view (you can implement this later)
      alert(`Viewing details for ${lot.prime_location_name}`)
    },
    
    closeModal() {
      this.showCreateModal = false
      this.showEditModal = false
      this.editingLot = null
      this.resetForm()
    },
    
    resetForm() {
      this.lotForm = {
        prime_location_name: '',
        address: '',
        pin_code: '',
        price_per_hour: '',
        number_of_spots: '',
        description: '',
        is_active: true
      }
    },
    
    async submitForm() {
      try {
        this.submitting = true
        
        let response
        if (this.showCreateModal) {
          response = await adminAPI.createParkingLot(this.lotForm)
        } else {
          response = await adminAPI.updateParkingLot(this.editingLot.id, this.lotForm)
        }
        
        if (response.data.success) {
          alert(response.data.message)
          this.closeModal()
          this.loadParkingLots()
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
        this.submitting = false
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