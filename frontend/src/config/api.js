// API Configuration - Smart auto-detection
// Use environment variable or fallback to relative path (for local development)
export const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// Check if backend is available
export const isBackendAvailable = () => {
  const hostname = window.location.hostname;
  
  // Backend is available if:
  // 1. VITE_API_URL environment variable is set (Netlify/production)
  // 2. Running on localhost (local development)
  // 3. Running on an IP address (AWS EC2 or remote server)
  return (
    import.meta.env.VITE_API_URL !== undefined || 
    hostname === 'localhost' ||
    hostname === '127.0.0.1' ||
    /^\d+\.\d+\.\d+\.\d+$/.test(hostname)  // Detects AWS IP addresses!
  );
}

