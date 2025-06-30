<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation Header -->
    <nav class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <div class="h-8 w-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                <svg class="h-5 w-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H7m2 0v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0V9a2 2 0 012-2h2a2 2 0 012 2v6.01"></path>
                </svg>
              </div>
              <h1 class="ml-3 text-xl font-semibold text-gray-900">Admin Dashboard</h1>
            </div>
            
            <!-- Navigation Links -->
            <div class="hidden md:ml-8 md:flex md:space-x-8">
              <router-link
                v-for="item in navigation"
                :key="item.name"
                :to="item.href"
                class="inline-flex items-center px-1 pt-1 text-sm font-medium border-b-2"
                :class="$route.path === item.href 
                  ? 'border-indigo-500 text-gray-900' 
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                {{ item.name }}
              </router-link>
            </div>
          </div>

          <!-- User Menu -->
          <div class="flex items-center space-x-4">
            <span class="text-sm text-gray-700">Welcome, {{ user.username }}</span>
            <button
              @click="handleLogout"
              class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error loading dashboard</h3>
            <p class="mt-2 text-sm text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Statistics Cards -->
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
                <div class="flex justify-between">
                  <span class="text-green-600 font-medium">Today: ₹{{ statistics.revenue?.today || 0 }}</span>
                  <span class="text-blue-600">Month: ₹{{ statistics.revenue?.this_month || 0 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Occupancy Rate -->
        <div v-if="statistics.parking_spots?.total > 0" class="mt-8">
          <div class="bg-white shadow rounded-lg p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">System Occupancy Rate</h3>
            <div class="flex items-center">
              <div class="flex-1">
                <div class="bg-gray-200 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full transition-all duration-300"
                    :class="getOccupancyColor(statistics.parking_spots.occupancy_rate)"
                    :style="{ width: `${statistics.parking_spots.occupancy_rate}%` }"
                  ></div>
                </div>
              </div>
              <div class="ml-4">
                <span class="text-2xl font-bold text-gray-900">{{ statistics.parking_spots.occupancy_rate }}%</span>
              </div>
            </div>
            <div class="mt-2 text-sm text-gray-600">
              {{ statistics.parking_spots.occupied }} of {{ statistics.parking_spots.total }} spots occupied
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="mt-8">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Quick Actions</h3>
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <router-link
              to="/admin/parking-lots"
              class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-500 rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <div>
                <span class="rounded-lg inline-flex p-3 bg-indigo-50 text-indigo-600 ring-4 ring-white">
                  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H7m2 0v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0V9a2 2 0 012-2h2a2 2 0 012 2v6.01"></path>
                  </svg>
                </span>
              </div>
              <div class="mt-8">
                <h3 class="text-lg font-medium">
                  <span class="absolute inset-0" aria-hidden="true"></span>
                  Manage Parking Lots
                </h3>
                <p class="mt-2 text-sm text-gray-500">
                  Create, edit, and manage parking lots and their spots.
                </p>
              </div>
            </router-link>

            <router-link
              to="/admin/users"
              class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-500 rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <div>
                <span class="rounded-lg inline-flex p-3 bg-green-50 text-green-600 ring-4 ring-white">
                  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z"></path>
                  </svg>
                </span>
              </div>
              <div class="mt-8">
                <h3 class="text-lg font-medium">
                  <span class="absolute inset-0" aria-hidden="true"></span>
                  Manage Users
                </h3>
                <p class="mt-2 text-sm text-gray-500">
                  View user details, manage accounts, and monitor activity.
                </p>
              </div>
            </router-link>

            <router-link
              to="/admin/reservations"
              class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-500 rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <div>
                <span class="rounded-lg inline-flex p-3 bg-purple-50 text-purple-600 ring-4 ring-white">
                  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </span>
              </div>
              <div class="mt-8">
                <h3 class="text-lg font-medium">
                  <span class="absolute inset-0" aria-hidden="true"></span>
                  View Reservations
                </h3>
                <p class="mt-2 text-sm text-gray-500">
                  Monitor all parking reservations and manage bookings.
                </p>
              </div>
            </router-link>

            <router-link
              to="/admin/analytics"
              class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-500 rounded-lg shadow hover:shadow-md transition-shadow"
            >
              <div>
                <span class="rounded-lg inline-flex p-3 bg-blue-50 text-blue-600 ring-4 ring-white">
                  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                  </svg>
                </span>
              </div>
              <div class="mt-8">
                <h3 class="text-lg font-medium">
                  <span class="absolute inset-0" aria-hidden="true"></span>
                  Analytics & Reports
                </h3>
                <p class="mt-2 text-sm text-gray-500">
                  View revenue analytics, usage patterns, and system reports.
                </p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAPI, authAPI } from '../../services/api'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      loading: true,
      error: '',
      statistics: {},
      user: { username: 'Admin' },
      navigation: [
        { name: 'Dashboard', href: '/admin/dashboard' },
        { name: 'Parking Lots', href: '/admin/parking-lots' },
        { name: 'Users', href: '/admin/users' },
        { name: 'Reservations', href: '/admin/reservations' },
        { name: 'Analytics', href: '/admin/analytics' },
        { name: 'Statistics', href: '/admin/statistics' }
      ]
    }
  },
  async mounted() {
    await this.loadDashboard()
  },
  methods: {
    async loadDashboard() {
      try {
        this.loading = true
        this.error = ''

        const [statsResponse, profileResponse] = await Promise.all([
          adminAPI.getStatistics(),
          authAPI.getProfile()
        ])

        if (statsResponse.data.success) {
          this.statistics = statsResponse.data.data
        }

        if (profileResponse.data.success) {
          this.user = profileResponse.data.user
        }
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load dashboard'
      } finally {
        this.loading = false
      }
    },
    refreshData() {
      this.loadDashboard()
    },
    async handleLogout() {
      try {
        await authAPI.logout()
        this.$router.push('/login')
      } catch (err) {
        console.error('Logout failed:', err)
        this.$router.push('/login')
      }
    },
    getOccupancyColor(rate) {
      if (rate < 50) return 'bg-green-500'
      if (rate < 80) return 'bg-yellow-500'
      return 'bg-red-500'
    }
  }
}
</script> 