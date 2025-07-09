<template>
  <div class="auth-layout">
    <div class="auth-container">
      <!-- Header -->
      <div class="auth-header">
        <div class="brand">
          <h1>🅿️ Vehicle Parking System</h1>
          <p class="tagline">Secure, Smart, Simple Parking Solutions</p>
        </div>
      </div>
      
      <!-- Main Auth Content -->
      <div class="auth-content">
        <router-view />
      </div>
      
      <!-- Footer -->
      <div class="auth-footer">
        <p>&copy; 2025 Vehicle Parking System. All rights reserved.</p>
      </div>
    </div>
    
    <!-- Background Animation -->
    <div class="background-animation">
      <div class="floating-shape shape-1"></div>
      <div class="floating-shape shape-2"></div>
      <div class="floating-shape shape-3"></div>
      <div class="floating-shape shape-4"></div>
      <div class="floating-shape shape-5"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthLayout'
}
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.auth-container {
  width: 100%;
  max-width: 450px;
  margin: 0 auto;
  padding: 2rem;
  position: relative;
  z-index: 2;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.brand h1 {
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.tagline {
  color: rgba(255,255,255,0.9);
  font-size: 1.1rem;
  margin: 0;
  font-weight: 300;
}

.auth-content {
  background: white;
  border-radius: 15px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  overflow: hidden;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
}

.auth-footer {
  text-align: center;
  margin-top: 2rem;
}

.auth-footer p {
  color: rgba(255,255,255,0.8);
  font-size: 0.9rem;
  margin: 0;
}

/* Background Animation */
.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;
}

.floating-shape {
  position: absolute;
  background: rgba(255,255,255,0.1);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

.shape-1 {
  width: 80px;
  height: 80px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.shape-2 {
  width: 120px;
  height: 120px;
  top: 20%;
  right: 10%;
  animation-delay: 1s;
}

.shape-3 {
  width: 60px;
  height: 60px;
  bottom: 30%;
  left: 20%;
  animation-delay: 2s;
}

.shape-4 {
  width: 100px;
  height: 100px;
  bottom: 10%;
  right: 20%;
  animation-delay: 3s;
}

.shape-5 {
  width: 140px;
  height: 140px;
  top: 50%;
  left: 50%;
  animation-delay: 4s;
  opacity: 0.05;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  33% {
    transform: translateY(-20px) rotate(120deg);
  }
  66% {
    transform: translateY(20px) rotate(240deg);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .auth-container {
    padding: 1rem;
    max-width: 90%;
  }
  
  .brand h1 {
    font-size: 2rem;
  }
  
  .tagline {
    font-size: 1rem;
  }
  
  .floating-shape {
    display: none; /* Hide animations on mobile for performance */
  }
}

@media (max-width: 480px) {
  .auth-container {
    padding: 0.5rem;
  }
  
  .brand h1 {
    font-size: 1.8rem;
  }
  
  .auth-header {
    margin-bottom: 1.5rem;
  }
}

/* Enhanced shadow for better depth */
.auth-content {
  position: relative;
}

.auth-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
  border-radius: 15px;
  z-index: -1;
}

/* Glassmorphism effect */
@supports (backdrop-filter: blur(10px)) {
  .auth-content {
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(10px);
  }
}
</style> 