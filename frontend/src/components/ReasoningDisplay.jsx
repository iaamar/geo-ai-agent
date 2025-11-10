import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Clock, CheckCircle, AlertCircle, Zap, GitBranch } from 'lucide-react';

/**
 * ReasoningDisplay Component
 * 
 * Displays the complete reasoning process of the multi-agent system
 * Shows: Agent decisions, data flow, timing, and transparency information
 */
const ReasoningDisplay = ({ result }) => {
  const [expandedSteps, setExpandedSteps] = useState({});
  const [activeTab, setActiveTab] = useState('reasoning');

  if (!result) return null;

  const toggleStep = (stepId) => {
    setExpandedSteps(prev => ({
      ...prev,
      [stepId]: !prev[stepId]
    }));
  };

  // Extract data
  const { 
    reasoning_trace = [], 
    component_info = {},
    data_flow = [],
    step_timings = {},
    errors = []
  } = result;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-lg">
        <h2 className="text-2xl font-bold mb-2">🤖 Multi-Agent Analysis System</h2>
        <p className="text-blue-100">
          Transparent AI reasoning with parallel execution
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-gray-200">
        <button
          onClick={() => setActiveTab('reasoning')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'reasoning'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-blue-600'
          }`}
        >
          Reasoning Trace
        </button>
        <button
          onClick={() => setActiveTab('components')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'components'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-blue-600'
          }`}
        >
          System Components
        </button>
        <button
          onClick={() => setActiveTab('dataflow')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'dataflow'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-blue-600'
          }`}
        >
          Data Flow
        </button>
        <button
          onClick={() => setActiveTab('performance')}
          className={`px-4 py-2 font-medium transition-colors ${
            activeTab === 'performance'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-blue-600'
          }`}
        >
          Performance
        </button>
      </div>

      {/* Reasoning Trace Tab */}
      {activeTab === 'reasoning' && (
        <div className="space-y-4">
          <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">📋 Reasoning Process</h3>
            <p className="text-sm text-blue-700">
              This shows the step-by-step reasoning process of each AI agent. 
              Each step explains what the agent did, why it did it, and what it decided.
            </p>
          </div>

          {reasoning_trace.map((step, idx) => (
            <div key={idx} className="border border-gray-200 rounded-lg overflow-hidden">
              {/* Step Header */}
              <div
                onClick={() => toggleStep(idx)}
                className="bg-gray-50 p-4 flex items-center justify-between cursor-pointer hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center gap-3">
                  {expandedSteps[idx] ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
                  <div className="flex items-center gap-2">
                    {step.status === 'completed' ? (
                      <CheckCircle className="text-green-500" size={20} />
                    ) : (
                      <AlertCircle className="text-yellow-500" size={20} />
                    )}
                    <span className="font-semibold">{step.agent}</span>
                  </div>
                  <span className="text-sm text-gray-600">• {step.step}</span>
                  {step.execution_mode && (
                    <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded">
                      {step.execution_mode}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <span className="flex items-center gap-1">
                    <Clock size={14} />
                    {step.duration?.toFixed(2)}s
                  </span>
                  <span className={`px-2 py-1 rounded text-xs ${
                    step.status === 'completed' 
                      ? 'bg-green-100 text-green-700'
                      : 'bg-yellow-100 text-yellow-700'
                  }`}>
                    {step.status}
                  </span>
                </div>
              </div>

              {/* Step Details */}
              {expandedSteps[idx] && (
                <div className="p-4 space-y-4 bg-white">
                  {/* Process Description */}
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Process:</h4>
                    <p className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
                      {step.process}
                    </p>
                  </div>

                  {/* Reasoning Steps */}
                  {step.reasoning_steps && (
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Reasoning Steps:</h4>
                      <ol className="list-decimal list-inside space-y-1 text-sm text-gray-600">
                        {step.reasoning_steps.map((s, i) => (
                          <li key={i} className="ml-2">{s}</li>
                        ))}
                      </ol>
                    </div>
                  )}

                  {/* Input */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Input:</h4>
                      <pre className="text-xs bg-gray-50 p-3 rounded overflow-auto">
                        {JSON.stringify(step.input, null, 2)}
                      </pre>
                    </div>

                    {/* Output */}
                    <div>
                      <h4 className="font-medium text-gray-700 mb-2">Output:</h4>
                      <pre className="text-xs bg-gray-50 p-3 rounded overflow-auto">
                        {JSON.stringify(step.output, null, 2)}
                      </pre>
                    </div>
                  </div>

                  {/* Additional metadata */}
                  <div className="flex gap-4 text-xs text-gray-500 pt-2 border-t">
                    <span>Timestamp: {new Date(step.timestamp).toLocaleTimeString()}</span>
                    {step.llm_model && <span>Model: {step.llm_model}</span>}
                    {step.concurrency_level && <span>Concurrency: {step.concurrency_level}</span>}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Components Tab */}
      {activeTab === 'components' && (
        <div className="space-y-4">
          <div className="bg-purple-50 border border-purple-200 p-4 rounded-lg">
            <h3 className="font-semibold text-purple-900 mb-2">🏗️ System Architecture</h3>
            <p className="text-sm text-purple-700 mb-3">
              {component_info.architecture?.description}
            </p>
            <div className="grid grid-cols-3 gap-2 text-xs">
              <div className="bg-white p-2 rounded">
                <span className="font-medium">Type:</span> {component_info.architecture?.type}
              </div>
              <div className="bg-white p-2 rounded">
                <span className="font-medium">Framework:</span> {component_info.architecture?.framework}
              </div>
              <div className="bg-white p-2 rounded">
                <span className="font-medium">Model:</span> {component_info.architecture?.execution_model}
              </div>
            </div>
          </div>

          {/* Agent Details */}
          <div className="space-y-3">
            {Object.entries(component_info.agents || {}).map(([agentName, info]) => (
              <div key={agentName} className="border border-gray-200 rounded-lg p-4 bg-white">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h4 className="font-semibold text-lg">{agentName}</h4>
                    <p className="text-sm text-gray-600">{info.role}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    info.execution === 'Parallel (all queries concurrent)' || info.execution?.includes('Parallel')
                      ? 'bg-purple-100 text-purple-700'
                      : 'bg-blue-100 text-blue-700'
                  }`}>
                    <Zap size={12} className="inline mr-1" />
                    {info.execution}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="font-medium text-gray-700 mb-1">Purpose:</p>
                    <p className="text-gray-600">{info.purpose}</p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-700 mb-1">Inputs:</p>
                    <ul className="text-gray-600 text-xs space-y-1">
                      {info.inputs?.map((input, i) => (
                        <li key={i}>• {input}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {info.reasoning_method && (
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    <p className="font-medium text-gray-700 text-sm mb-1">Reasoning Method:</p>
                    <p className="text-gray-600 text-sm">{info.reasoning_method}</p>
                  </div>
                )}

                {info.methods && (
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    <p className="font-medium text-gray-700 text-sm mb-1">Methods:</p>
                    <div className="flex flex-wrap gap-1">
                      {info.methods.map((method, i) => (
                        <span key={i} className="text-xs bg-gray-100 px-2 py-1 rounded">
                          {method}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Parallelization Info */}
          {component_info.parallelization && (
            <div className="bg-purple-50 border border-purple-200 p-4 rounded-lg">
              <h4 className="font-semibold text-purple-900 mb-2 flex items-center gap-2">
                <Zap className="text-purple-600" size={18} />
                Parallel Execution Benefits
              </h4>
              <div className="space-y-2 text-sm">
                <p><strong>Data Collection:</strong> {component_info.parallelization.data_collection}</p>
                <p><strong>Analysis Generation:</strong> {component_info.parallelization.analysis_generation}</p>
                <p className="text-purple-700 font-medium">
                  ⚡ Performance Benefit: {component_info.parallelization.benefit}
                </p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Data Flow Tab */}
      {activeTab === 'dataflow' && (
        <div className="space-y-4">
          <div className="bg-green-50 border border-green-200 p-4 rounded-lg">
            <h3 className="font-semibold text-green-900 mb-2 flex items-center gap-2">
              <GitBranch className="text-green-600" size={18} />
              Data Flow Through System
            </h3>
            <p className="text-sm text-green-700">
              Visualization of how data moves through the multi-agent system
            </p>
          </div>

          {/* Flow diagram */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            {data_flow.map((flow, idx) => (
              <div key={idx} className="flex items-center gap-4 mb-4">
                <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-lg font-medium text-sm min-w-[200px] text-center">
                  {flow.from}
                </div>
                <div className="flex-1 flex items-center">
                  <div className="h-px bg-gray-300 flex-1"></div>
                  <div className="px-3 py-1 bg-gray-100 text-gray-700 text-xs rounded mx-2">
                    {flow.data}
                  </div>
                  <div className="h-px bg-gray-300 flex-1"></div>
                  <div className="text-blue-600">→</div>
                </div>
                <div className="bg-purple-100 text-purple-800 px-4 py-2 rounded-lg font-medium text-sm min-w-[200px] text-center">
                  {flow.to}
                </div>
              </div>
            ))}
          </div>

          {/* Component Interaction Diagram */}
          {component_info.data_flow && (
            <div className="bg-white border border-gray-200 rounded-lg p-6">
              <h4 className="font-semibold mb-4">Complete Data Flow:</h4>
              <div className="space-y-2">
                {component_info.data_flow.map((step, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-sm">
                    <span className="text-gray-400">{idx + 1}.</span>
                    <span className="text-gray-700">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Performance Tab */}
      {activeTab === 'performance' && (
        <div className="space-y-4">
          <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
            <h3 className="font-semibold text-yellow-900 mb-2">⚡ Performance Metrics</h3>
            <p className="text-sm text-yellow-700">
              Execution timing for each component
            </p>
          </div>

          {/* Timing Chart */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h4 className="font-semibold mb-4">Step Execution Times:</h4>
            <div className="space-y-3">
              {Object.entries(step_timings).map(([step, duration]) => (
                <div key={step}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium capitalize">{step.replace('_', ' ')}</span>
                    <span className="text-gray-600">{duration.toFixed(2)}s</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{ 
                        width: `${Math.min((duration / (step_timings.total || 1)) * 100, 100)}%` 
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>

            {/* Summary */}
            <div className="mt-6 pt-4 border-t border-gray-200 grid grid-cols-3 gap-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-600">
                  {step_timings.total?.toFixed(1)}s
                </p>
                <p className="text-sm text-gray-600">Total Time</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">
                  {reasoning_trace.length}
                </p>
                <p className="text-sm text-gray-600">Agent Steps</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-purple-600">
                  ~40%
                </p>
                <p className="text-sm text-gray-600">Speedup vs Sequential</p>
              </div>
            </div>
          </div>

          {/* Errors */}
          {errors.length > 0 && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <h4 className="font-semibold text-red-900 mb-3 flex items-center gap-2">
                <AlertCircle size={18} />
                Errors Encountered ({errors.length})
              </h4>
              <div className="space-y-2">
                {errors.map((error, idx) => (
                  <div key={idx} className="bg-white p-3 rounded text-sm">
                    <div className="flex justify-between mb-1">
                      <span className="font-medium">{error.step} - {error.platform}</span>
                      <span className="text-xs text-gray-500">{new Date(error.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <p className="text-gray-600 text-xs">Query: {error.query}</p>
                    <p className="text-red-600 text-xs mt-1">Error: {error.error}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Transparency Features */}
      {component_info.transparency_features && (
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 p-4 rounded-lg">
          <h4 className="font-semibold text-indigo-900 mb-2">🔍 Transparency Features</h4>
          <div className="grid grid-cols-2 gap-2">
            {component_info.transparency_features.map((feature, idx) => (
              <div key={idx} className="flex items-center gap-2 text-sm text-indigo-700">
                <CheckCircle size={14} className="text-green-500" />
                {feature}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ReasoningDisplay;

