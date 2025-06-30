<template>
  <div class="analytics">
    <!-- Header -->
    <div class="page-header">
      <div class="header-content">
        <h1>Analytics & Reports</h1>
        <p class="text-muted">Comprehensive parking system analytics and revenue reports</p>
      </div>
      <div class="header-actions">
        <router-link to="/admin/dashboard" class="btn btn-outline-primary">
          <i class="fas fa-arrow-left"></i> Back to Dashboard
        </router-link>
      </div>
    </div>

    <!-- Revenue Analytics Section -->
    <div class="analytics-section mb-5">
      <div class="card">
        <div class="card-header">
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="mb-0">
              <i class="fas fa-chart-line"></i> Revenue Analytics
            </h5>
            <div class="period-selector">
              <select class="form-select" v-model="revenuePeriod" @change="loadRevenueAnalytics">
                <option value="day">Last 30 Days</option>
                <option value="month">Last 12 Months</option>
              </select>
            </div>
          </div>
        </div>
        <div class="card-body">
          <div v-if="loadingRevenue" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p>Loading revenue analytics...</p>
          </div>
          
          <div v-else-if="revenueError" class="alert alert-danger">
            <i class="fas fa-exclamation-triangle"></i>
            {{ revenueError }}
            <button @click="loadRevenueAnalytics" class="btn btn-sm btn-outline-danger ms-2">
              <i class="fas fa-refresh"></i> Retry
            </button>
          </div>
          
          <div v-else-if="revenueData" class="revenue-analytics-content">
            <!-- Revenue Trend Chart -->
            <div class="revenue-chart mb-4">
              <h6>Revenue Trend</h6>
              <div class="chart-container">
                <div class="simple-chart">
                  <div 
                    v-for="(item, index) in revenueData.revenue_trend" 
                    :key="index"
                    class="chart-bar"
                    :style="{ 
                      height: getBarHeight(item.revenue, revenueData.revenue_trend) + '%',
                      backgroundColor: '#007bff'
                    }"
                    :title="`${revenuePeriod === 'month' ? item.month : item.date}: ₹${item.revenue}`"
                  >
                    <div class="bar-value">₹{{ item.revenue }}</div>
                    <div class="bar-label">
                      {{ revenuePeriod === 'month' ? item.month?.split(' ')[0] : formatShortDate(item.date) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Revenue by Parking Lot -->
            <div class="row">
              <div class="col-lg-6">
                <h6>Revenue by Parking Lot</h6>
                <div class="table-responsive">
                  <table class="table table-sm">
                    <thead>
                      <tr>
                        <th>Parking Lot</th>
                        <th>Revenue</th>
                        <th>Reservations</th>
                        <th>Avg/Booking</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="lot in revenueData.revenue_by_lot" :key="lot.lot_name">
                        <td>{{ lot.lot_name }}</td>
                        <td class="text-success">₹{{ lot.revenue }}</td>
                        <td>{{ lot.reservations }}</td>
                        <td class="text-muted">₹{{ lot.avg_revenue_per_reservation }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              
              <div class="col-lg-6">
                <h6>Top Users by Spending</h6>
                <div class="table-responsive">
                  <table class="table table-sm">
                    <thead>
                      <tr>
                        <th>User</th>
                        <th>Total Spent</th>
                        <th>Bookings</th>
                        <th>Avg/Booking</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="user in revenueData.top_users" :key="user.username">
                        <td>
                          <div>{{ user.full_name }}</div>
                          <small class="text-muted">{{ user.username }}</small>
                        </td>
                        <td class="text-success">₹{{ user.total_spent }}</td>
                        <td>{{ user.total_reservations }}</td>
                        <td class="text-muted">₹{{ user.avg_spent_per_reservation }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Usage Analytics Section -->
    <div class="analytics-section mb-5">
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0">
            <i class="fas fa-chart-bar"></i> Usage Analytics
          </h5>
        </div>
        <div class="card-body">
          <div v-if="loadingUsage" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p>Loading usage analytics...</p>
          </div>
          
          <div v-else-if="usageError" class="alert alert-danger">
            <i class="fas fa-exclamation-triangle"></i>
            {{ usageError }}
            <button @click="loadUsageAnalytics" class="btn btn-sm btn-outline-danger ms-2">
              <i class="fas fa-refresh"></i> Retry
            </button>
          </div>
          
          <div v-else-if="usageData" class="usage-analytics-content">
            <div class="row">
              <!-- Peak Hours Chart -->
              <div class="col-lg-6 mb-4">
                <h6>Peak Hours Analysis</h6>
                <div class="peak-hours-chart">
                  <div 
                    v-for="hour in usageData.peak_hours" 
                    :key="hour.hour"
                    class="hour-bar"
                    :style="{ 
                      height: getBarHeight(hour.reservations, usageData.peak_hours) + '%',
                      backgroundColor: getPeakHourColor(hour.hour)
                    }"
                    :title="`${hour.time_label}: ${hour.reservations} reservations`"
                  >
                    <div class="hour-value">{{ hour.reservations }}</div>
                    <div class="hour-label">{{ hour.time_label }}</div>
                  </div>
                </div>
              </div>
              
              <!-- Current Occupancy -->
              <div class="col-lg-6 mb-4">
                <h6>Current System Status</h6>
                <div class="occupancy-display">
                  <div class="occupancy-circle">
                    <div class="occupancy-percentage">
                      {{ usageData.current_occupancy.occupancy_rate }}%
                    </div>
                    <div class="occupancy-label">Occupied</div>
                  </div>
                  <div class="occupancy-details">
                    <div class="occupancy-item">
                      <span class="badge bg-danger">{{ usageData.current_occupancy.occupied_spots }}</span>
                      Occupied Spots
                    </div>
                    <div class="occupancy-item">
                      <span class="badge bg-success">{{ usageData.current_occupancy.total_spots - usageData.current_occupancy.occupied_spots }}</span>
                      Available Spots
                    </div>
                    <div class="occupancy-item">
                      <span class="badge bg-primary">{{ usageData.current_occupancy.total_spots }}</span>
                      Total Spots
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Average Duration by Lot -->
            <div class="row">
              <div class="col-12">
                <h6>Average Session Duration by Parking Lot</h6>
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead class="table-light">
                      <tr>
                        <th>Parking Lot</th>
                        <th>Avg Duration (Hours)</th>
                        <th>Avg Duration (Minutes)</th>
                        <th>Total Sessions</th>
                        <th>Duration Indicator</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="lot in usageData.average_duration_by_lot" :key="lot.lot_name">
                        <td>{{ lot.lot_name }}</td>
                        <td>{{ lot.avg_duration_hours }}h</td>
                        <td>{{ lot.avg_duration_minutes }}m</td>
                        <td>{{ lot.total_sessions }}</td>
                        <td>
                          <div class="duration-bar">
                            <div 
                              class="duration-fill"
                              :style="{ 
                                width: getDurationBarWidth(lot.avg_duration_hours) + '%',
                                backgroundColor: getDurationBarColor(lot.avg_duration_hours)
                              }"
                            ></div>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Statistics -->
    <div class="analytics-section">
      <div class="card">
        <div class="card-header">
          <h5 class="mb-0">
            <i class="fas fa-chart-pie"></i> Summary Statistics
          </h5>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-3">
              <div class="summary-stat">
                <div class="stat-value text-primary">{{ revenueData?.revenue_trend?.length || 0 }}</div>
                <div class="stat-label">Data Points</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="summary-stat">
                <div class="stat-value text-success">
                  ₹{{ getTotalRevenue() }}
                </div>
                <div class="stat-label">Total Revenue (Period)</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="summary-stat">
                <div class="stat-value text-info">
                  {{ getAverageSessionDuration() }}h
                </div>
                <div class="stat-label">Avg Session Duration</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="summary-stat">
                <div class="stat-value text-warning">
                  {{ getPeakHour() }}
                </div>
                <div class="stat-label">Peak Hour</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { adminAPI } from '../../services/api'

export default {
  name: 'Analytics',
  setup() {
    // Reactive data
    const loadingRevenue = ref(true)
    const loadingUsage = ref(true)
    const revenueError = ref('')
    const usageError = ref('')
    const revenueData = ref(null)
    const usageData = ref(null)
    const revenuePeriod = ref('month')

    // Load revenue analytics
    const loadRevenueAnalytics = async () => {
      try {
        loadingRevenue.value = true
        revenueError.value = ''
        
        const params = { period: revenuePeriod.value }
        const response = await adminAPI.getRevenueAnalytics(params)
        revenueData.value = response.data.data
        
      } catch (err) {
        console.error('Error loading revenue analytics:', err)
        revenueError.value = err.response?.data?.message || 'Failed to load revenue analytics'
      } finally {
        loadingRevenue.value = false
      }
    }

    // Load usage analytics
    const loadUsageAnalytics = async () => {
      try {
        loadingUsage.value = true
        usageError.value = ''
        
        const response = await adminAPI.getUsageAnalytics()
        usageData.value = response.data.data
        
      } catch (err) {
        console.error('Error loading usage analytics:', err)
        usageError.value = err.response?.data?.message || 'Failed to load usage analytics'
      } finally {
        loadingUsage.value = false
      }
    }

    // Chart helper functions
    const getBarHeight = (value, dataArray) => {
      if (!dataArray || dataArray.length === 0) return 0
      const maxValue = Math.max(...dataArray.map(item => item.revenue || item.reservations || 0))
      if (maxValue === 0) return 0
      return Math.max(5, (value / maxValue) * 100)
    }

    const getPeakHourColor = (hour) => {
      // Color code based on typical business hours
      if (hour >= 9 && hour <= 17) return '#28a745' // Business hours - green
      if (hour >= 18 && hour <= 22) return '#ffc107' // Evening - yellow
      return '#6c757d' // Night/early morning - gray
    }

    const getDurationBarWidth = (hours) => {
      // Assume max 8 hours for scale
      return Math.min((hours / 8) * 100, 100)
    }

    const getDurationBarColor = (hours) => {
      if (hours <= 1) return '#28a745' // Short sessions - green
      if (hours <= 3) return '#ffc107' // Medium sessions - yellow
      if (hours <= 6) return '#fd7e14' // Long sessions - orange
      return '#dc3545' // Very long sessions - red
    }

    // Utility functions
    const formatShortDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return `${date.getMonth() + 1}/${date.getDate()}`
    }

    // Summary calculations
    const getTotalRevenue = () => {
      if (!revenueData.value?.revenue_trend) return '0'
      const total = revenueData.value.revenue_trend.reduce((sum, item) => sum + item.revenue, 0)
      return total.toFixed(2)
    }

    const getAverageSessionDuration = () => {
      if (!usageData.value?.average_duration_by_lot) return '0'
      const lots = usageData.value.average_duration_by_lot
      if (lots.length === 0) return '0'
      const avgDuration = lots.reduce((sum, lot) => sum + lot.avg_duration_hours, 0) / lots.length
      return avgDuration.toFixed(1)
    }

    const getPeakHour = () => {
      if (!usageData.value?.peak_hours) return 'N/A'
      const peakHour = usageData.value.peak_hours.reduce((peak, hour) => 
        hour.reservations > peak.reservations ? hour : peak
      , { reservations: 0, time_label: 'N/A' })
      return peakHour.time_label
    }

    // Load data on mount
    onMounted(() => {
      loadRevenueAnalytics()
      loadUsageAnalytics()
    })

    return {
      loadingRevenue,
      loadingUsage,
      revenueError,
      usageError,
      revenueData,
      usageData,
      revenuePeriod,
      loadRevenueAnalytics,
      loadUsageAnalytics,
      getBarHeight,
      getPeakHourColor,
      getDurationBarWidth,
      getDurationBarColor,
      formatShortDate,
      getTotalRevenue,
      getAverageSessionDuration,
      getPeakHour
    }
  }
}
</script>

<style scoped>
.analytics {
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

.period-selector .form-select {
  min-width: 150px;
}

/* Chart Styles */
.chart-container {
  height: 300px;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 20px;
  background: #f8f9fa;
}

.simple-chart {
  display: flex;
  align-items: end;
  justify-content: space-around;
  height: 100%;
  gap: 5px;
}

.chart-bar {
  flex: 1;
  min-height: 20px;
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: all 0.3s ease;
  cursor: pointer;
  max-width: 40px;
}

.chart-bar:hover {
  opacity: 0.8;
  transform: translateY(-2px);
}

.bar-value {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.8rem;
  font-weight: bold;
  color: #333;
  white-space: nowrap;
}

.bar-label {
  position: absolute;
  bottom: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.7rem;
  color: #666;
  white-space: nowrap;
}

/* Peak Hours Chart */
.peak-hours-chart {
  display: flex;
  align-items: end;
  justify-content: space-around;
  height: 200px;
  gap: 2px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.hour-bar {
  flex: 1;
  min-height: 10px;
  border-radius: 2px 2px 0 0;
  position: relative;
  max-width: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.hour-bar:hover {
  opacity: 0.8;
}

.hour-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.7rem;
  font-weight: bold;
  color: #333;
}

.hour-label {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.6rem;
  color: #666;
  writing-mode: vertical-lr;
  text-orientation: mixed;
}

/* Occupancy Display */
.occupancy-display {
  display: flex;
  align-items: center;
  gap: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.occupancy-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: conic-gradient(#dc3545 0% var(--occupancy-percentage, 0%), #e9ecef var(--occupancy-percentage, 0%) 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.occupancy-circle::before {
  content: '';
  position: absolute;
  width: 80px;
  height: 80px;
  background: white;
  border-radius: 50%;
}

.occupancy-percentage {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  z-index: 1;
}

.occupancy-label {
  font-size: 0.8rem;
  color: #666;
  z-index: 1;
}

.occupancy-details {
  flex: 1;
}

.occupancy-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

/* Duration Bar */
.duration-bar {
  width: 100%;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.duration-fill {
  height: 100%;
  transition: width 0.3s ease;
}

/* Summary Statistics */
.summary-stat {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .chart-container, .peak-hours-chart {
    height: 200px;
  }
  
  .occupancy-display {
    flex-direction: column;
    text-align: center;
  }
  
  .simple-chart, .peak-hours-chart {
    gap: 2px;
  }
  
  .bar-value, .hour-value {
    display: none;
  }
}
</style> 