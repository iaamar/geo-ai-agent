import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Clock, TrendingUp, AlertTriangle } from 'lucide-react'
import { API_BASE_URL, isBackendAvailable } from '../config/api'

function HistoryPage() {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    // Skip loading if backend is not available
    if (!isBackendAvailable()) {
      setLoading(false)
      return
    }
    
    try {
      const response = await axios.get(`${API_BASE_URL}/history?limit=20`)
      setHistory(response.data.analyses || [])
    } catch (err) {
      console.error('Failed to load history:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-slate-900 mb-2">
          Analysis History
        </h1>
        <p className="text-lg text-slate-600">
          View past GEO analyses
        </p>
      </div>

      {/* Backend Status Warning */}
      {!isBackendAvailable() && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 flex items-start">
          <AlertTriangle className="h-5 w-5 text-amber-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-amber-900">Demo Mode - Backend Not Connected</h3>
            <p className="text-sm text-amber-700 mt-1">
              Backend API is required to view analysis history. Run locally or deploy the backend.
            </p>
          </div>
        </div>
      )}

      {loading ? (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-slate-600">Loading history...</p>
        </div>
      ) : history.length === 0 ? (
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12 text-center">
          <Clock className="h-12 w-12 text-slate-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-slate-900 mb-2">No analyses yet</h3>
          <p className="text-slate-600">Run your first analysis to see results here</p>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((item, idx) => (
            <HistoryCard key={idx} item={item} />
          ))}
        </div>
      )}
    </div>
  )
}

function HistoryCard({ item }) {
  const date = new Date(item.timestamp)
  const visibilityRate = (item.visibility_rate * 100).toFixed(1)

  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-slate-900 mb-1">
            {item.query}
          </h3>
          <p className="text-sm text-slate-600 mb-3">
            Brand: {item.brand}
          </p>
          <div className="flex items-center gap-4 text-sm text-slate-500">
            <span className="flex items-center">
              <Clock className="h-4 w-4 mr-1" />
              {date.toLocaleString()}
            </span>
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-center text-sm text-slate-600 mb-1">
            <TrendingUp className="h-4 w-4 mr-1" />
            Visibility
          </div>
          <div className="text-3xl font-bold text-primary-600">
            {visibilityRate}%
          </div>
        </div>
      </div>
      {item.num_hypotheses > 0 && (
        <div className="mt-4 pt-4 border-t border-slate-200">
          <div className="flex gap-4 text-sm text-slate-600">
            <span>{item.num_hypotheses} findings</span>
            <span>•</span>
            <span>{item.num_recommendations} recommendations</span>
          </div>
        </div>
      )}
    </div>
  )
}

export default HistoryPage



