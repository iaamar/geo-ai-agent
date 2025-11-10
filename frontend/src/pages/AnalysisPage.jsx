import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Loader2, Search, AlertCircle, CheckCircle, TrendingUp, Shuffle } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import ReasoningDisplay from '../components/ReasoningDisplay'
import RealTimeProgress from '../components/RealTimeProgress'
import EvaluationDisplay from '../components/EvaluationDisplay'
import { useAnalysisProgress } from '../hooks/useAnalysisProgress'

// Real-world GEO analysis examples
const REAL_WORLD_EXAMPLES = [
  {
    name: "AI Project Management Tools",
    query: "best AI project management software 2024",
    brand_domain: "monday.com",
    competitors: "asana.com, clickup.com, notion.so, linear.app",
    description: "Analyze visibility for AI-powered project management platforms"
  },
  {
    name: "CRM Software Comparison",
    query: "best CRM software for small business",
    brand_domain: "hubspot.com",
    competitors: "salesforce.com, zoho.com, pipedrive.com, freshsales.io",
    description: "Compare CRM platform visibility in AI recommendations"
  },
  {
    name: "Marketing Automation Tools",
    query: "best marketing automation platform",
    brand_domain: "mailchimp.com",
    competitors: "hubspot.com, activecampaign.com, klaviyo.com, constant-contact.com",
    description: "Track marketing automation tool visibility"
  },
  {
    name: "Cloud Storage Solutions",
    query: "best cloud storage for businesses",
    brand_domain: "dropbox.com",
    competitors: "box.com, google.com/drive, onedrive.com, sync.com",
    description: "Analyze cloud storage provider visibility"
  },
  {
    name: "E-commerce Platforms",
    query: "best e-commerce platform for startups",
    brand_domain: "shopify.com",
    competitors: "woocommerce.com, bigcommerce.com, wix.com, squarespace.com",
    description: "Compare e-commerce platform recommendations"
  }
]

function AnalysisPage() {
  const getRandomExample = () => {
    const randomIndex = Math.floor(Math.random() * REAL_WORLD_EXAMPLES.length)
    return REAL_WORLD_EXAMPLES[randomIndex]
  }

  const [currentExample, setCurrentExample] = useState(getRandomExample())
  const [formData, setFormData] = useState({
    query: currentExample.query,
    brand_domain: currentExample.brand_domain,
    competitors: currentExample.competitors,
    platforms: ['chatgpt', 'perplexity'],
    num_queries: 5
  })
  
  // Auto-fill with random example on component mount
  useEffect(() => {
    const example = getRandomExample()
    setCurrentExample(example)
    setFormData(prev => ({
      ...prev,
      query: example.query,
      brand_domain: example.brand_domain,
      competitors: example.competitors
    }))
  }, [])  // Empty dependency array = runs once on mount
  
  const loadRandomExample = () => {
    const example = getRandomExample()
    setCurrentExample(example)
    setFormData(prev => ({
      ...prev,
      query: example.query,
      brand_domain: example.brand_domain,
      competitors: example.competitors
    }))
  }
  
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  
  // Real-time progress tracking
  const { steps, isAnalyzing, startAnalysis, completeAnalysis, updateStep, addQueryResult } = useAnalysisProgress()

  const simulateProgress = async (payload) => {
    // Step 1: Planning
    updateStep('planning', { status: 'running' })
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Step 2: Data Collection
    updateStep('planning', { 
      status: 'completed', 
      duration: 0.5,
      llm_output: 'Strategy created: Testing ' + payload.num_queries + ' query variations across ' + payload.platforms.length + ' platforms'
    })
    updateStep('data_collection', { status: 'running' })
    
    // This will be populated as the backend returns data
    // For now, we update after full response
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    startAnalysis()

    try {
      const payload = {
        query: formData.query,
        brand_domain: formData.brand_domain,
        competitors: formData.competitors.split(',').map(c => c.trim()).filter(Boolean),
        platforms: formData.platforms,
        num_queries: parseInt(formData.num_queries)
      }

      // Simulate progress during analysis
      simulateProgress(payload)

      const response = await axios.post('/api/analyze', payload)
      
      // Update progress with actual data
      updateStepsWithRealData(response.data)
      
      setResult(response.data)
      completeAnalysis()
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed')
      completeAnalysis()
    } finally {
      setLoading(false)
    }
  }

  const updateStepsWithRealData = (data) => {
    // Map backend steps to frontend step IDs
    const stepMapping = {
      'planning': 'planning',
      'data_collection': 'data_collection',
      'analysis': 'analysis',
      'hypothesis_generation': 'hypothesis',
      'recommendation_generation': 'recommendations',
      'evaluation': 'evaluation',
      'synthesis': 'synthesis'
    }
    
    // Update each step with actual data from response
    if (data.reasoning_trace) {
      data.reasoning_trace.forEach(trace => {
        const stepId = stepMapping[trace.step] || trace.step
        
        const updates = {
          status: trace.status || 'completed',
          duration: trace.duration,
          llm_output: trace.llm_output || (trace.reasoning_steps ? trace.reasoning_steps.join('\n') : null),
          results: trace.output
        }
        
        // Add specific data for each step type
        if (trace.step === 'data_collection' && trace.queries_detail) {
          updates.queries_detail = trace.queries_detail
        }
        
        if (trace.step === 'hypothesis_generation' && trace.hypotheses_detail) {
          updates.hypotheses_detail = trace.hypotheses_detail
        }
        
        if (trace.step === 'recommendation_generation' && trace.recommendations_detail) {
          updates.recommendations_detail = trace.recommendations_detail
        }
        
        if (trace.step === 'evaluation') {
          updates.evaluation_results = trace.output
        }
        
        updateStep(stepId, updates)
      })
      
      // Mark all remaining steps as completed
      setTimeout(() => {
        Object.keys(stepMapping).forEach(backendStep => {
          const frontendId = stepMapping[backendStep]
          updateStep(frontendId, { status: 'completed' })
        })
      }, 500)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handlePlatformToggle = (platform) => {
    setFormData(prev => ({
      ...prev,
      platforms: prev.platforms.includes(platform)
        ? prev.platforms.filter(p => p !== platform)
        : [...prev.platforms, platform]
    }))
  }

  return (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-slate-900 mb-2">
          GEO Visibility Analysis
        </h1>
        <p className="text-lg text-slate-600">
          Analyze your brand's visibility across AI platforms
        </p>
        
        {/* Current Example Badge */}
        <div className="mt-4 inline-flex items-center gap-2 bg-blue-50 border border-blue-200 px-4 py-2 rounded-lg">
          <span className="text-sm font-medium text-blue-900">Example:</span>
          <span className="text-sm text-blue-700">{currentExample.name}</span>
          <button
            onClick={loadRandomExample}
            className="ml-2 p-1 hover:bg-blue-100 rounded transition-colors"
            title="Load another example"
          >
            <Shuffle size={16} className="text-blue-600" />
          </button>
        </div>
        <p className="text-xs text-slate-500 mt-2">{currentExample.description}</p>
      </div>

      {/* Analysis Form */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
        {/* Example Selector */}
        <div className="mb-6 pb-4 border-b border-slate-200">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-slate-700">Real-World Examples</h3>
            <button
              type="button"
              onClick={loadRandomExample}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center gap-1"
            >
              <Shuffle size={14} />
              Load Random Example
            </button>
          </div>
          <div className="grid grid-cols-5 gap-2">
            {REAL_WORLD_EXAMPLES.map((example, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => {
                  setCurrentExample(example)
                  setFormData(prev => ({
                    ...prev,
                    query: example.query,
                    brand_domain: example.brand_domain,
                    competitors: example.competitors
                  }))
                }}
                className={`text-xs px-3 py-2 rounded border transition-colors ${
                  currentExample.name === example.name
                    ? 'bg-blue-600 text-white border-blue-600'
                    : 'bg-white text-slate-700 border-slate-300 hover:border-blue-400'
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
              name="query"
              value={formData.query}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="e.g., best AI productivity tools"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Your Brand Domain
              </label>
              <input
                type="text"
                name="brand_domain"
                value={formData.brand_domain}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                placeholder="e.g., acme.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">
                Number of Queries
              </label>
              <input
                type="number"
                name="num_queries"
                value={formData.num_queries}
                onChange={handleInputChange}
                min="1"
                max="10"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Competitor Domains (comma-separated)
            </label>
            <input
              type="text"
              name="competitors"
              value={formData.competitors}
              onChange={handleInputChange}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="e.g., notion.so, asana.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Platforms
            </label>
            <div className="flex gap-4">
              {['chatgpt', 'perplexity'].map(platform => (
                <label key={platform} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.platforms.includes(platform)}
                    onChange={() => handlePlatformToggle(platform)}
                    className="mr-2 h-4 w-4 text-primary-600 border-slate-300 rounded focus:ring-primary-500"
                  />
                  <span className="text-sm text-slate-700 capitalize">{platform}</span>
                </label>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || formData.platforms.length === 0}
            className="w-full inline-flex items-center justify-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin mr-2 h-5 w-5" />
                Analyzing...
              </>
            ) : (
              <>
                <Search className="mr-2 h-5 w-5" />
                Run Analysis
              </>
            )}
          </button>
        </form>
      </div>

      {/* Real-Time Progress Display */}
      {(loading || steps.length > 0) && (
        <RealTimeProgress steps={steps} isAnalyzing={isAnalyzing} />
      )}

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
          <AlertCircle className="h-5 w-5 text-red-600 mr-3 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-red-900">Analysis Error</h3>
            <p className="text-sm text-red-700 mt-1">{error}</p>
          </div>
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div className="space-y-6">
          {/* Self-Critique Evaluation Results - NEW! */}
          {result.evaluation_metrics && result.evaluation_metrics.evaluation_performed && (
            <EvaluationDisplay evaluationMetrics={result.evaluation_metrics} />
          )}

          {/* Reasoning & Transparency Section */}
          {result.reasoning_trace && result.reasoning_trace.length > 0 && (
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <ReasoningDisplay result={result} />
            </div>
          )}

          {/* Summary */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">
              Analysis Summary
            </h2>
            <div className="prose max-w-none text-slate-700 whitespace-pre-line">
              {result.summary}
            </div>
          </div>

          {/* Visibility Scores */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">
              Visibility Comparison
            </h2>
            <VisibilityChart data={result.visibility_scores} />
          </div>

          {/* Hypotheses */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">
              Key Findings
            </h2>
            <div className="space-y-4">
              {result.hypotheses.map((hypothesis, idx) => (
                <HypothesisCard key={idx} hypothesis={hypothesis} />
              ))}
            </div>
          </div>

          {/* Recommendations */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-2xl font-bold text-slate-900 mb-4">
              Recommendations
            </h2>
            <div className="space-y-4">
              {result.recommendations.map((rec, idx) => (
                <RecommendationCard key={idx} recommendation={rec} />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function VisibilityChart({ data }) {
  const chartData = [
    {
      name: data.brand_score.domain,
      'Mention Rate': (data.brand_score.mention_rate * 100).toFixed(1),
      type: 'brand'
    },
    ...data.competitor_scores.map(score => ({
      name: score.domain,
      'Mention Rate': (score.mention_rate * 100).toFixed(1),
      type: 'competitor'
    }))
  ]

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis label={{ value: 'Mention Rate (%)', angle: -90, position: 'insideLeft' }} />
        <Tooltip />
        <Legend />
        <Bar dataKey="Mention Rate" fill="#0ea5e9" />
      </BarChart>
    </ResponsiveContainer>
  )
}

function HypothesisCard({ hypothesis }) {
  return (
    <div className="border border-slate-200 rounded-lg p-4">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold text-slate-900">{hypothesis.title}</h3>
        <span className="text-sm text-slate-600">
          {(hypothesis.confidence * 100).toFixed(0)}% confidence
        </span>
      </div>
      <p className="text-slate-700 mb-3">{hypothesis.explanation}</p>
      {hypothesis.supporting_evidence.length > 0 && (
        <div className="mt-2">
          <p className="text-sm font-medium text-slate-700 mb-1">Evidence:</p>
          <ul className="text-sm text-slate-600 space-y-1">
            {hypothesis.supporting_evidence.map((evidence, idx) => (
              <li key={idx} className="flex items-start">
                <CheckCircle className="h-4 w-4 text-green-600 mr-2 flex-shrink-0 mt-0.5" />
                {evidence}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

function RecommendationCard({ recommendation }) {
  const priorityColors = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  }

  return (
    <div className="border border-slate-200 rounded-lg p-4">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold text-slate-900">{recommendation.title}</h3>
        <span className={`text-xs px-2 py-1 rounded ${priorityColors[recommendation.priority]}`}>
          {recommendation.priority.toUpperCase()}
        </span>
      </div>
      <p className="text-slate-700 mb-3">{recommendation.description}</p>
      
      <div className="flex gap-4 mb-3 text-sm">
        <div className="flex items-center">
          <TrendingUp className="h-4 w-4 text-green-600 mr-1" />
          <span className="text-slate-600">Impact: {recommendation.impact_score}/10</span>
        </div>
        <div className="flex items-center">
          <span className="text-slate-600">Effort: {recommendation.effort_score}/10</span>
        </div>
      </div>

      <div className="bg-slate-50 rounded p-3">
        <p className="text-sm font-medium text-slate-700 mb-2">Action Items:</p>
        <ul className="text-sm text-slate-600 space-y-1">
          {recommendation.action_items.map((item, idx) => (
            <li key={idx}>• {item}</li>
          ))}
        </ul>
      </div>

      <div className="mt-3 pt-3 border-t border-slate-200">
        <p className="text-sm text-slate-700">
          <span className="font-medium">Expected Outcome:</span> {recommendation.expected_outcome}
        </p>
      </div>
    </div>
  )
}

export default AnalysisPage



