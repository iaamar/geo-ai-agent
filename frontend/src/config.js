/**
 * Auto-detect API URL based on environment
 * 
 * Works on:
 * - Localhost (development)
 * - AWS EC2 (same server)
 * - Netlify (with VITE_API_URL env var)
 */

const getApiUrl = () => {
  // 1. Check environment variable (Netlify, production)
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  // 2. Check if running on localhost
  const hostname = window.location.hostname;
  
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    // Local development - use proxy or direct localhost
    return '';  // Empty = same origin, uses Vite proxy
  }
  
  // 3. Running on AWS or remote server
  // Backend is on same server at port 8000
  const protocol = window.location.protocol;
  return `${protocol}//${hostname}:8000`;
};

export const API_URL = getApiUrl();

// Helper to show current mode
export const getConnectionMode = () => {
  const url = API_URL || window.location.origin;
  
  if (url.includes('localhost') || url === '') {
    return {
      mode: 'local',
      message: 'Running on localhost',
      apiUrl: 'http://localhost:8000'
    };
  } else if (url.includes('3.12.198.127') || url.match(/\d+\.\d+\.\d+\.\d+/)) {
    return {
      mode: 'aws',
      message: 'Connected to AWS backend',
      apiUrl: url
    };
  } else {
    return {
      mode: 'demo',
      message: 'Demo mode - backend not available',
      apiUrl: url
    };
  }
};

