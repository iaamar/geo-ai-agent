import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Loader2, GitCompare, ChevronDown, ChevronUp, CheckCircle, TrendingUp, ExternalLink, Shuffle, AlertTriangle, AlertCircle } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { API_BASE_URL, isBackendAvailable } from '../config/api'

// Real-world comparison examples
const COMPARISON_EXAMPLES = [
  {
    name: "CRM Platforms",
    query: "best CRM software",
    domains: "hubspot.com, salesforce.com, pipedrive.com, zoho.com"
  },
  {
    name: "Project Management",
    query: "best project management tool",
    domains: "asana.com, monday.com, clickup.com, notion.so"
  },
  {
    name: "Email Marketing",
    query: "best email marketing software",
    domains: "mailchimp.com, constant-contact.com, sendinblue.com, activecampaign.com"
  },
  {
    name: "E-commerce",
    query: "best e-commerce platform",
    domains: "shopify.com, woocommerce.com, bigcommerce.com, wix.com"
  },
  {
    name: "Cloud Storage",
    query: "best cloud storage service",
    domains: "dropbox.com, box.com, google.com, onedrive.com"
  }
]

function ComparePage() {
  const getRandomExample = () => {
    return COMPARISON_EXAMPLES[Math.floor(Math.random() * COMPARISON_EXAMPLES.length)]
  }

  const [currentExample, setCurrentExample] = useState(getRandomExample())
  const [formData, setFormData] = useState({
    query: currentExample.query,
    domains: currentExample.domains
  })
  
  useEffect(() => {
    const example = getRandomExample()
    setCurrentExample(example)
    setFormData({
      query: example.query,
      domains: example.domains
    })
  }, [])
  
  const loadRandomExample = () => {
    const example = getRandomExample()
    setCurrentExample(example)
    setFormData({
      query: example.query,
      domains: example.domains
    })
  }
  
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Check if backend is available
    if (!isBackendAvailable()) {
      setError('Backend API is not available. This is a frontend-only demo deployment.')
      return
    }
    
    setLoading(true)
    setError(null)

    try {
      const payload = {
        query: formData.query,
        domains: formData.domains.split(',').map(d => d.trim()).filter(Boolean),
        platforms: ['chatgpt', 'perplexity']
      }

      const response = await axios.post(`${API_BASE_URL}/compare`, payload)
      setResult(response.data)
    } catch (err) {
      console.error('Comparison failed:', err)
      setError(err.response?.data?.detail || err.message || 'Comparison failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Backend Status Warning */}
      {!isBackendAvailable() && (
        <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 flex items-start">
          <AlertTriangle className="h-5 w-5 text-amber-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-amber-900">Demo Mode - Backend Not Connected</h3>
            <p className="text-sm text-amber-700 mt-1">
              Backend API is required for comparison functionality. Run locally or deploy the backend.
            </p>
          </div>
        </div>
      )}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-slate-900 mb-2">
          Brand Comparison
        </h1>
        <p className="text-lg text-slate-600">
          Compare visibility across multiple brands
        </p>
        
        {/* Current Example Badge */}
        <div className="mt-4 inline-flex items-center gap-2 bg-purple-50 border border-purple-200 px-4 py-2 rounded-lg">
          <span className="text-sm font-medium text-purple-900">Example:</span>
          <span className="text-sm text-purple-700">{currentExample.name}</span>
          <button
            onClick={loadRandomExample}
            className="ml-2 p-1 hover:bg-purple-100 rounded transition-colors"
            title="Load another example"
          >
            <Shuffle size={16} className="text-purple-600" />
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
        {/* Example Selector */}
        <div className="mb-6 pb-4 border-b border-slate-200">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-slate-700">Comparison Examples</h3>
            <button
              type="button"
              onClick={loadRandomExample}
              className="text-sm text-purple-600 hover:text-purple-700 font-medium flex items-center gap-1"
            >
              <Shuffle size={14} />
              Load Random
            </button>
          </div>
          <div className="grid grid-cols-5 gap-2">
            {COMPARISON_EXAMPLES.map((example, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => {
                  setCurrentExample(example)
                  setFormData({
                    query: example.query,
                    domains: example.domains
                  })
                }}
                className={`text-xs px-3 py-2 rounded border transition-colors ${
                  currentExample.name === example.name
                    ? 'bg-purple-600 text-white border-purple-600'
                    : 'bg-white text-slate-700 border-slate-300 hover:border-purple-400'
                }`}
              >
                {example.name}
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Search Query
            </label>
            <input
              type="text"
              value={formData.query}
              onChange={(e) => setFormData({...formData, query: e.target.value})}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Domains to Compare (comma-separated, 2-5 domains)
            </label>
            <input
              type="text"
              value={formData.domains}
              onChange={(e) => setFormData({...formData, domains: e.target.value})}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full inline-flex items-center justify-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin mr-2 h-5 w-5" />
                Comparing...
              </>
            ) : (
              <>
                <GitCompare className="mr-2 h-5 w-5" />
                Compare Brands
              </>
            )}
          </button>
        </form>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
          <AlertCircle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-red-900">Comparison Error</h3>
            <p className="text-sm text-red-700 mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-slate-200">
          <Loader2 className="animate-spin h-12 w-12 text-primary-600 mx-auto mb-4" />
          <p className="text-slate-600">Comparing brands...</p>
        </div>
      )}

      {result && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">
              Comparison Results for "{result.query}"
            </h2>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={result.comparison}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="domain" />
                <YAxis label={{ value: 'Mention Rate (%)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="visibility_rate" name="Visibility Rate" fill="#0ea5e9" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {result.comparison.map((item, idx) => (
              <div
                key={idx}
                className={`bg-white rounded-lg shadow-sm border p-4 ${
                  item.domain === result.winner ? 'border-green-500 ring-2 ring-green-200' : 'border-slate-200'
                }`}
              >
                <h3 className="font-semibold text-slate-900 mb-2">{item.domain}</h3>
                <div className="space-y-2">
                  <div>
                    <p className="text-sm text-slate-600">Visibility Rate</p>
                    <p className="text-2xl font-bold text-primary-600">
                      {(item.visibility_rate * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600">Total Mentions</p>
                    <p className="text-lg font-semibold text-slate-900">{item.mentions}</p>
                  </div>
                </div>
                {item.domain === result.winner && (
                  <div className="mt-3 text-sm font-medium text-green-600">
                    🏆 Top Performer
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Detailed Analysis */}
          {result.full_analysis && (
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <h2 className="text-2xl font-bold text-slate-900 mb-4">
                Shared Analysis Insights
              </h2>
              
              <div className="space-y-6">
                {/* Summary */}
                <div>
                  <h3 className="font-semibold text-slate-800 mb-2">Executive Summary</h3>
                  <p className="text-slate-700 whitespace-pre-line">{result.full_analysis.summary}</p>
                </div>
                
                {/* Key Findings */}
                {result.full_analysis.hypotheses && result.full_analysis.hypotheses.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-slate-800 mb-3">Key Findings</h3>
                    <div className="space-y-3">
                      {result.full_analysis.hypotheses.map((hyp, idx) => (
                        <div key={idx} className="border border-slate-200 rounded-lg p-4 bg-slate-50">
                          <div className="flex items-center justify-between mb-2">
                            <h4 className="font-medium text-slate-900">{hyp.title}</h4>
                            <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                              {(hyp.confidence * 100).toFixed(0)}% confidence
                            </span>
                          </div>
                          <p className="text-sm text-slate-700">{hyp.explanation}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {/* Recommendations */}
                {result.full_analysis.recommendations && result.full_analysis.recommendations.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-slate-800 mb-3">Recommendations</h3>
                    <div className="space-y-3">
                      {result.full_analysis.recommendations.slice(0, 3).map((rec, idx) => (
                        <div key={idx} className="border border-slate-200 rounded-lg p-4 bg-slate-50">
                          <div className="flex items-center justify-between mb-2">
                            <h4 className="font-medium text-slate-900">{rec.title}</h4>
                            <span className={`text-xs px-2 py-1 rounded ${
                              rec.priority === 'high' ? 'bg-red-100 text-red-700' :
                              rec.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-green-100 text-green-700'
                            }`}>
                              {rec.priority.toUpperCase()}
                            </span>
                          </div>
                          <p className="text-sm text-slate-700 mb-2">{rec.description}</p>
                          <div className="flex gap-3 text-xs text-slate-600">
                            <span>Impact: {rec.impact_score}/10</span>
                            <span>Effort: {rec.effort_score}/10</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function BrandDetailCard({ brand, isWinner }) {
  const [expandedSection, setExpandedSection] = useState(null)

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? null : section)
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-6 ${
      isWinner ? 'border-green-500 ring-2 ring-green-200' : 'border-slate-200'
    }`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-slate-900">{brand.domain}</h3>
        {isWinner && (
          <span className="text-sm font-medium text-green-600 bg-green-50 px-3 py-1 rounded-full">
            🏆 Top Performer
          </span>
        )}
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        <div className="bg-slate-50 rounded-lg p-3">
          <p className="text-xs text-slate-600 mb-1">Visibility Rate</p>
          <p className="text-xl font-bold text-primary-600">
            {(brand.visibility_rate * 100).toFixed(1)}%
          </p>
        </div>
        <div className="bg-slate-50 rounded-lg p-3">
          <p className="text-xs text-slate-600 mb-1">Total Mentions</p>
          <p className="text-xl font-bold text-slate-900">{brand.mentions}</p>
        </div>
        <div className="bg-slate-50 rounded-lg p-3">
          <p className="text-xs text-slate-600 mb-1">Citations</p>
          <p className="text-xl font-bold text-slate-900">{brand.citations?.length || 0}</p>
        </div>
        <div className="bg-slate-50 rounded-lg p-3">
          <p className="text-xs text-slate-600 mb-1">Platforms</p>
          <p className="text-sm font-semibold text-slate-900">{brand.platforms?.join(', ') || 'N/A'}</p>
        </div>
      </div>

      {/* Citations Section */}
      <CollapsibleSection
        title={`Citations (${brand.citations?.length || 0})`}
        isExpanded={expandedSection === 'citations'}
        onToggle={() => toggleSection('citations')}
      >
        <div className="space-y-3">
          {brand.citations && brand.citations.map((citation, idx) => {
            // Combine brand and competitors for display
            const mentionedDomains = [
              ...(citation.brand_mentioned ? [brand.domain] : []),
              ...(citation.competitors_mentioned || [])
            ]
            
            return (
              <div key={idx} className="border border-slate-200 rounded-lg p-4 bg-slate-50">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-slate-600 bg-white px-2 py-1 rounded">
                    {citation.platform}
                  </span>
                  <span className="text-xs text-slate-500">{citation.query}</span>
                </div>
                <p className="text-sm text-slate-700 mb-2">{citation.raw_response}</p>
                {citation.context && (
                  <p className="text-xs text-slate-600 italic mb-2">Context: {citation.context}</p>
                )}
                {mentionedDomains.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    <span className="text-xs text-slate-600 mr-2">Mentioned:</span>
                    {mentionedDomains.map((domain, i) => (
                      <span key={i} className={`text-xs px-2 py-1 rounded ${
                        domain === brand.domain 
                          ? 'bg-green-100 text-green-700 font-semibold' 
                          : 'bg-primary-100 text-primary-700'
                      }`}>
                        {domain}
                      </span>
                    ))}
                  </div>
                )}
                {citation.citation_position && (
                  <div className="mt-2 text-xs text-slate-600">
                    Position: #{citation.citation_position}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </CollapsibleSection>

      {/* Hypotheses Section */}
      <CollapsibleSection
        title={`Key Findings (${brand.hypotheses?.length || 0})`}
        isExpanded={expandedSection === 'hypotheses'}
        onToggle={() => toggleSection('hypotheses')}
      >
        <div className="space-y-3">
          {brand.hypotheses && brand.hypotheses.map((hypothesis, idx) => (
            <div key={idx} className="border border-slate-200 rounded-lg p-4">
              <div className="flex items-start justify-between mb-2">
                <h4 className="font-semibold text-slate-900">{hypothesis.title}</h4>
                <span className="text-sm text-slate-600 whitespace-nowrap ml-2">
                  {(hypothesis.confidence * 100).toFixed(0)}% confidence
                </span>
              </div>
              <p className="text-slate-700 mb-3">{hypothesis.explanation}</p>
              {hypothesis.supporting_evidence && hypothesis.supporting_evidence.length > 0 && (
                <div className="mt-2">
                  <p className="text-sm font-medium text-slate-700 mb-1">Evidence:</p>
                  <ul className="text-sm text-slate-600 space-y-1">
                    {hypothesis.supporting_evidence.map((evidence, i) => (
                      <li key={i} className="flex items-start">
                        <CheckCircle className="h-4 w-4 text-green-600 mr-2 flex-shrink-0 mt-0.5" />
                        {evidence}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </CollapsibleSection>

      {/* Recommendations Section */}
      <CollapsibleSection
        title={`Recommendations (${brand.recommendations?.length || 0})`}
        isExpanded={expandedSection === 'recommendations'}
        onToggle={() => toggleSection('recommendations')}
      >
        <div className="space-y-3">
          {brand.recommendations && brand.recommendations.map((rec, idx) => (
            <div key={idx} className="border border-slate-200 rounded-lg p-4">
              <div className="flex items-start justify-between mb-2">
                <h4 className="font-semibold text-slate-900">{rec.title}</h4>
                <span className={`text-xs px-2 py-1 rounded ${
                  rec.priority === 'high' ? 'bg-red-100 text-red-800' :
                  rec.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>
                  {rec.priority?.toUpperCase()}
                </span>
              </div>
              <p className="text-slate-700 mb-3">{rec.description}</p>
              
              <div className="flex gap-4 mb-3 text-sm">
                <div className="flex items-center">
                  <TrendingUp className="h-4 w-4 text-green-600 mr-1" />
                  <span className="text-slate-600">Impact: {rec.impact_score}/10</span>
                </div>
                <div className="flex items-center">
                  <span className="text-slate-600">Effort: {rec.effort_score}/10</span>
                </div>
                <div className="flex items-center">
                  <span className="text-slate-600">ROI: {(rec.impact_score / Math.max(rec.effort_score, 1)).toFixed(2)}</span>
                </div>
              </div>

              {rec.action_items && rec.action_items.length > 0 && (
                <div className="bg-slate-50 rounded p-3">
                  <p className="text-sm font-medium text-slate-700 mb-2">Action Items:</p>
                  <ul className="text-sm text-slate-600 space-y-1">
                    {rec.action_items.map((item, i) => (
                      <li key={i}>• {item}</li>
                    ))}
                  </ul>
                </div>
              )}

              {rec.expected_outcome && (
                <div className="mt-3 pt-3 border-t border-slate-200">
                  <p className="text-sm text-slate-700">
                    <span className="font-medium">Expected Outcome:</span> {rec.expected_outcome}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </CollapsibleSection>

      {/* Summary Section */}
      {brand.summary && (
        <CollapsibleSection
          title="Analysis Summary"
          isExpanded={expandedSection === 'summary'}
          onToggle={() => toggleSection('summary')}
        >
          <div className="prose max-w-none text-slate-700 whitespace-pre-line">
            {brand.summary}
          </div>
        </CollapsibleSection>
      )}
    </div>
  )
}

function CollapsibleSection({ title, isExpanded, onToggle, children }) {
  return (
    <div className="mb-4">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between py-3 px-4 bg-slate-50 hover:bg-slate-100 rounded-lg transition-colors"
      >
        <h4 className="font-semibold text-slate-900">{title}</h4>
        {isExpanded ? (
          <ChevronUp className="h-5 w-5 text-slate-600" />
        ) : (
          <ChevronDown className="h-5 w-5 text-slate-600" />
        )}
      </button>
      {isExpanded && (
        <div className="mt-3 px-2">
          {children}
        </div>
      )}
    </div>
  )
}

export default ComparePage



