// API Configuration
// Use environment variable or fallback to relative path (for local development)
export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// Check if backend is available
export const isBackendAvailable = () => {
  // In production without env var, backend is not available
  return import.meta.env.VITE_API_URL !== undefined || window.location.hostname === 'localhost'
}

