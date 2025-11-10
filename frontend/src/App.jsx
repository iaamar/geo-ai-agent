import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { Activity, BarChart3, History, Home } from 'lucide-react'

import HomePage from './pages/HomePage'
import AnalysisPage from './pages/AnalysisPage'
import HistoryPage from './pages/HistoryPage'
import ComparePage from './pages/ComparePage'

function App() {
  const [currentPath, setCurrentPath] = useState('/')

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <div className="flex-shrink-0 flex items-center">
                  <Activity className="h-8 w-8 text-primary-600" />
                  <span className="ml-2 text-xl font-bold text-slate-900">
                    GEO Expert Agent
                  </span>
                </div>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link
                    to="/"
                    className={`${
                      currentPath === '/'
                        ? 'border-primary-500 text-slate-900'
                        : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-700'
                    } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                    onClick={() => setCurrentPath('/')}
                  >
                    <Home className="h-4 w-4 mr-1" />
                    Home
                  </Link>
                  <Link
                    to="/analyze"
                    className={`${
                      currentPath === '/analyze'
                        ? 'border-primary-500 text-slate-900'
                        : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-700'
                    } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                    onClick={() => setCurrentPath('/analyze')}
                  >
                    <Activity className="h-4 w-4 mr-1" />
                    Analyze
                  </Link>
                  <Link
                    to="/compare"
                    className={`${
                      currentPath === '/compare'
                        ? 'border-primary-500 text-slate-900'
                        : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-700'
                    } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                    onClick={() => setCurrentPath('/compare')}
                  >
                    <BarChart3 className="h-4 w-4 mr-1" />
                    Compare
                  </Link>
                  <Link
                    to="/history"
                    className={`${
                      currentPath === '/history'
                        ? 'border-primary-500 text-slate-900'
                        : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-700'
                    } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                    onClick={() => setCurrentPath('/history')}
                  >
                    <History className="h-4 w-4 mr-1" />
                    History
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/analyze" element={<AnalysisPage />} />
            <Route path="/compare" element={<ComparePage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-slate-200 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <p className="text-center text-sm text-slate-500">
              GEO Expert Agent v1.0.0
            </p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App



