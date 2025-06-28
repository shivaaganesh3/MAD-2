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
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <h1 class="ml-3 text-xl font-semibold text-gray-900">System Statistics</h1>
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
      <div class="mb-6">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl">System Analytics</h2>
        <p class="mt-1 text-sm text-gray-500">Comprehensive system statistics and insights</p>
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
            <h3 class="text-sm font-medium text-red-800">Error loading statistics</h3>
            <p class="mt-2 text-sm text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Statistics Content -->
      <div v-else class="space-y-6">
        <!-- Overview Cards -->
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
          <!-- Users Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Users</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ statistics.users?.total || 0 }}</dd>
                  </dl>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-5 py-3">
              <div class="text-sm">
                <span class="text-green-600 font-medium">{{ statistics.users?.active || 0 }} active</span>
                <span class="text-gray-500"> / {{ statistics.users?.inactive || 0 }} inactive</span>
              </div>
            </div>
          </div>

          <!-- Parking Lots Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H7m2 0v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0V9a2 2 0 012-2h2a2 2 0 012 2v6.01"></path>
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Parking Lots</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ statistics.parking_lots?.total || 0 }}</dd>
                  </dl>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-5 py-3">
              <div class="text-sm">
                <span class="text-green-600 font-medium">{{ statistics.parking_lots?.active || 0 }} active</span>
                <span class="text-gray-500"> / {{ statistics.parking_lots?.inactive || 0 }} inactive</span>
              </div>
            </div>
          </div>

          <!-- Parking Spots Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Parking Spots</dt>
                    <dd class="text-lg font-medium text-gray-900">{{ statistics.parking_spots?.total || 0 }}</dd>
                  </dl>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-5 py-3">
              <div class="text-sm">
                <span class="text-green-600 font-medium">{{ statistics.parking_spots?.available || 0 }} available</span>
                <span class="text-red-600"> / {{ statistics.parking_spots?.occupied || 0 }} occupied</span>
              </div>
            </div>
          </div>

          <!-- Revenue Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                  </svg>
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Revenue</dt>
                    <dd class="text-lg font-medium text-gray-900">₹{{ statistics.revenue?.total || 0 }}</dd>
                  </dl>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-5 py-3">
              <div class="text-sm">
                <span class="text-gray-500">{{ statistics.reservations?.completed || 0 }} completed bookings</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Detailed Statistics -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <!-- Reservations Overview -->
          <div class="bg-white shadow rounded-lg p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Reservations Overview</h3>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">Total Reservations</span>
                <span class="text-sm font-medium text-gray-900">{{ statistics.reservations?.total || 0 }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">Active Reservations</span>
                <span class="text-sm font-medium text-green-600">{{ statistics.reservations?.active || 0 }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">Completed Reservations</span>
                <span class="text-sm font-medium text-blue-600">{{ statistics.reservations?.completed || 0 }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sm text-gray-600">Cancelled Reservations</span>
                <span class="text-sm font-medium text-red-600">{{ statistics.reservations?.cancelled || 0 }}</span>
              </div>
            </div>
          </div>

          <!-- System Occupancy -->
          <div class="bg-white shadow rounded-lg p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">System Occupancy</h3>
            <div class="space-y-4">
              <div>
                <div class="flex items-center justify-between text-sm">
                  <span class="text-gray-600">Current Occupancy Rate</span>
                  <span class="font-medium">{{ statistics.parking_spots?.occupancy_rate || 0 }}%</span>
                </div>
                <div class="mt-1 w-full bg-gray-200 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full transition-all duration-300"
                    :class="getOccupancyColor(statistics.parking_spots?.occupancy_rate || 0)"
                    :style="{ width: `${statistics.parking_spots?.occupancy_rate || 0}%` }"
                  ></div>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4 text-center">
                <div class="p-3 bg-green-50 rounded-lg">
                  <div class="text-lg font-semibold text-green-600">{{ statistics.parking_spots?.available || 0 }}</div>
                  <div class="text-xs text-green-600">Available Spots</div>
                </div>
                <div class="p-3 bg-red-50 rounded-lg">
                  <div class="text-lg font-semibold text-red-600">{{ statistics.parking_spots?.occupied || 0 }}</div>
                  <div class="text-xs text-red-600">Occupied Spots</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Refresh Button -->
        <div class="flex justify-center">
          <button
            @click="loadStatistics"
            class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            Refresh Statistics
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAPI, authAPI } from '../../services/api'

export default {
  name: 'SystemStats',
  data() {
    return {
      loading: true,
      error: '',
      statistics: {}
    }
  },
  async mounted() {
    await this.loadStatistics()
  },
  methods: {
    async loadStatistics() {
      try {
        this.loading = true
        this.error = ''

        const response = await adminAPI.getStatistics()
        
        if (response.data.success) {
          this.statistics = response.data.data
        } else {
          this.error = response.data.message
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load statistics'
      } finally {
        this.loading = false
      }
    },
    
    getOccupancyColor(rate) {
      if (rate < 50) return 'bg-green-500'
      if (rate < 80) return 'bg-yellow-500'
      return 'bg-red-500'
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