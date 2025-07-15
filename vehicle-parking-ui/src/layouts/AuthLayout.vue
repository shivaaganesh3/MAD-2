<template>
  <div class="auth-layout min-vh-100 d-flex align-items-center justify-content-center position-relative">
    <div class="container-fluid">
      <div class="row justify-content-center">
        <div class="col-11 col-sm-10 col-md-8 col-lg-7 col-xl-6 col-xxl-5">
          <div class="auth-container position-relative">
            <!-- Header -->
            <div class="text-center mb-4">
              <div class="brand">
                <h1 class="text-white fw-bold mb-2">🅿️ Vehicle Parking System</h1>
                <p class="tagline text-white-50 fs-6 mb-0">Secure, Smart, Simple Parking Solutions</p>
              </div>
            </div>
            
            <!-- Main Auth Content -->
            <div class="auth-content bg-white rounded-4 shadow-lg">
              <router-view />
            </div>
            
            <!-- Footer -->
            <div class="text-center mt-4">
              <p class="text-white-50 small mb-0">&copy; 2025 Vehicle Parking System. All rights reserved.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Background Animation -->
    <div class="background-animation position-absolute top-0 start-0 w-100 h-100 overflow-hidden">
      <div class="floating-shape shape-1 position-absolute rounded-circle"></div>
      <div class="floating-shape shape-2 position-absolute rounded-circle"></div>
      <div class="floating-shape shape-3 position-absolute rounded-circle"></div>
      <div class="floating-shape shape-4 position-absolute rounded-circle"></div>
      <div class="floating-shape shape-5 position-absolute rounded-circle"></div>
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}

.auth-container {
  z-index: 2;
}

.brand h1 {
  font-size: 2.8rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.tagline {
  font-weight: 300;
  font-size: 1.1rem;
}

.auth-content {
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
  overflow: hidden;
  padding: 0;
}

/* Background Animation */
.background-animation {
  z-index: 1;
}

.floating-shape {
  background: rgba(255,255,255,0.1);
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
  .brand h1 {
    font-size: 2.2rem !important;
  }
  
  .tagline {
    font-size: 1rem !important;
  }
  
  .floating-shape {
    display: none; /* Hide animations on mobile for performance */
  }
}

@media (max-width: 480px) {
  .brand h1 {
    font-size: 1.9rem !important;
  }
  
  .tagline {
    font-size: 0.9rem !important;
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
  border-radius: 1.5rem;
  z-index: -1;
}

/* Glassmorphism effect */
@supports (backdrop-filter: blur(10px)) {
  .auth-content {
    background: rgba(255,255,255,0.95) !important;
    backdrop-filter: blur(10px);
  }
}

/* Enhanced box shadow using Bootstrap custom properties */
.shadow-lg {
  box-shadow: 0 20px 40px rgba(0,0,0,0.2) !important;
}
</style> 