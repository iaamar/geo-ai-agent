import React from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, Brain, LineChart, Target, Zap } from 'lucide-react'

function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center p-2 bg-primary-100 rounded-full mb-4">
          <Brain className="h-12 w-12 text-primary-600" />
        </div>
        <h1 className="text-5xl font-bold text-slate-900 mb-4">
          GEO Expert Agent
        </h1>
        <p className="text-xl text-slate-600 max-w-3xl mx-auto mb-8">
          AI-powered Generative Engine Optimization analysis. Understand and improve 
          your brand's visibility across ChatGPT, Perplexity, and other AI platforms.
        </p>
        <button
          onClick={() => navigate('/analyze')}
          className="inline-flex items-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
        >
          Start Analysis
          <ArrowRight className="ml-2 h-5 w-5" />
        </button>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <FeatureCard
          icon={<Target className="h-8 w-8 text-primary-600" />}
          title="Visibility Analysis"
          description="Track how often your brand appears in AI-generated answers"
        />
        <FeatureCard
          icon={<LineChart className="h-8 w-8 text-primary-600" />}
          title="Competitor Insights"
          description="Compare your visibility against competitors"
        />
        <FeatureCard
          icon={<Brain className="h-8 w-8 text-primary-600" />}
          title="AI-Powered Reasoning"
          description="Understand why patterns emerge using LLM analysis"
        />
        <FeatureCard
          icon={<Zap className="h-8 w-8 text-primary-600" />}
          title="Actionable Recommendations"
          description="Get prioritized strategies to improve visibility"
        />
      </div>

      {/* How It Works */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-8">
        <h2 className="text-3xl font-bold text-slate-900 mb-8 text-center">
          How It Works
        </h2>
        <div className="space-y-6">
          <Step
            number="1"
            title="Enter Your Query"
            description="Provide the search query you want to analyze (e.g., 'best AI productivity tools')"
          />
          <Step
            number="2"
            title="Define Competitors"
            description="Specify your brand domain and competitor domains to compare against"
          />
          <Step
            number="3"
            title="AI Analysis"
            description="Our multi-agent system queries AI platforms, analyzes patterns, and generates insights"
          />
          <Step
            number="4"
            title="Get Recommendations"
            description="Receive prioritized, actionable strategies to improve your GEO visibility"
          />
        </div>
      </div>

      {/* Architecture Overview */}
      <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg p-8">
        <h2 className="text-3xl font-bold text-slate-900 mb-6 text-center">
          Multi-Agent Architecture
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <AgentCard
            title="Planner Agent"
            description="Creates investigation strategy and query variations"
          />
          <AgentCard
            title="Data Retriever"
            description="Fetches visibility data from AI platforms"
          />
          <AgentCard
            title="Analyzer Agent"
            description="Processes patterns and calculates metrics"
          />
          <AgentCard
            title="Hypothesis Agent"
            description="Explains visibility patterns using LLM reasoning"
          />
          <AgentCard
            title="Recommender Agent"
            description="Generates actionable improvement strategies"
          />
          <AgentCard
            title="Memory Layer"
            description="Stores historical analyses with vector embeddings"
          />
        </div>
      </div>

      {/* CTA */}
      <div className="text-center py-8">
        <h2 className="text-2xl font-bold text-slate-900 mb-4">
          Ready to improve your AI visibility?
        </h2>
        <button
          onClick={() => navigate('/analyze')}
          className="inline-flex items-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
        >
          Start Your First Analysis
          <ArrowRight className="ml-2 h-5 w-5" />
        </button>
      </div>
    </div>
  )
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
      <div className="mb-4">{icon}</div>
      <h3 className="text-lg font-semibold text-slate-900 mb-2">{title}</h3>
      <p className="text-sm text-slate-600">{description}</p>
    </div>
  )
}

function Step({ number, title, description }) {
  return (
    <div className="flex items-start">
      <div className="flex-shrink-0">
        <div className="flex items-center justify-center h-10 w-10 rounded-full bg-primary-600 text-white font-bold">
          {number}
        </div>
      </div>
      <div className="ml-4">
        <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
        <p className="text-slate-600">{description}</p>
      </div>
    </div>
  )
}

function AgentCard({ title, description }) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-4">
      <h3 className="text-base font-semibold text-slate-900 mb-2">{title}</h3>
      <p className="text-sm text-slate-600">{description}</p>
    </div>
  )
}

export default HomePage



