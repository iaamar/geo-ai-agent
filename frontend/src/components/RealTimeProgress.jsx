import React, { useState, useEffect } from 'react';
import { ChevronDown, ChevronRight, Clock, CheckCircle2, Loader2, Brain, Search, Lightbulb, ListChecks, FileText } from 'lucide-react';

/**
 * RealTimeProgress Component
 * Shows live progress of analysis with collapsible sections for each step
 * Displays all LLM-generated content in real-time
 */
const RealTimeProgress = ({ steps, isAnalyzing }) => {
  const [expandedSteps, setExpandedSteps] = useState({});

  // Auto-expand the currently executing step
  useEffect(() => {
    const runningStep = steps.find(s => s.status === 'running');
    if (runningStep) {
      setExpandedSteps(prev => ({ ...prev, [runningStep.id]: true }));
    }
  }, [steps]);

  const toggleStep = (stepId) => {
    setExpandedSteps(prev => ({
      ...prev,
      [stepId]: !prev[stepId]
    }));
  };

  if (!steps || steps.length === 0) return null;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 space-y-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-slate-900">
          🔄 Real-Time Analysis Progress
        </h2>
        {isAnalyzing && (
          <div className="flex items-center gap-2 text-blue-600">
            <Loader2 className="animate-spin" size={18} />
            <span className="text-sm font-medium">Analyzing...</span>
          </div>
        )}
      </div>

      <div className="space-y-3">
        {steps.map((step, idx) => (
          <StepCard
            key={step.id}
            step={step}
            stepNumber={idx + 1}
            isExpanded={expandedSteps[step.id]}
            onToggle={() => toggleStep(step.id)}
          />
        ))}
      </div>
    </div>
  );
};

const StepCard = ({ step, stepNumber, isExpanded, onToggle }) => {
  const getIcon = (type) => {
    switch(type) {
      case 'planning': return <Brain size={18} />;
      case 'data_collection': return <Search size={18} />;
      case 'analysis': return <FileText size={18} />;
      case 'hypothesis': return <Lightbulb size={18} />;
      case 'recommendations': return <ListChecks size={18} />;
      case 'evaluation': return <CheckCircle2 size={18} className="text-purple-600" />;
      case 'synthesis': return <FileText size={18} />;
      default: return <CheckCircle2 size={18} />;
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'completed': return 'text-green-600 bg-green-50';
      case 'running': return 'text-blue-600 bg-blue-50 animate-pulse';
      case 'pending': return 'text-gray-400 bg-gray-50';
      case 'error': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className={`border rounded-lg overflow-hidden transition-all ${
      step.status === 'running' ? 'border-blue-400 shadow-md' : 'border-slate-200'
    }`}>
      {/* Header */}
      <button
        onClick={onToggle}
        className={`w-full px-4 py-3 flex items-center justify-between transition-colors ${
          step.status === 'running' ? 'bg-blue-50' : 'bg-slate-50 hover:bg-slate-100'
        }`}
      >
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded ${getStatusColor(step.status)}`}>
            {step.status === 'running' ? <Loader2 className="animate-spin" size={18} /> : getIcon(step.type)}
          </div>
          <div className="text-left">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-slate-900">
                Step {stepNumber}: {step.title}
              </span>
              {step.status === 'completed' && <CheckCircle2 className="text-green-500" size={16} />}
            </div>
            {step.subtitle && (
              <p className="text-xs text-slate-600">{step.subtitle}</p>
            )}
          </div>
        </div>
        <div className="flex items-center gap-3">
          {step.duration && (
            <span className="text-sm text-slate-600 flex items-center gap-1">
              <Clock size={14} />
              {step.duration.toFixed(2)}s
            </span>
          )}
          {isExpanded ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
        </div>
      </button>

      {/* Expandable Content */}
      {isExpanded && (
        <div className="p-4 bg-white space-y-4 border-t border-slate-200">
          {/* Description */}
          {step.description && (
            <div className="bg-blue-50 border border-blue-200 p-3 rounded">
              <p className="text-sm text-blue-900">{step.description}</p>
            </div>
          )}

          {/* Platform Queries (for data collection) */}
          {step.queries_detail && step.queries_detail.length > 0 && (
            <div>
              <h4 className="font-semibold text-slate-900 mb-3 flex items-center gap-2">
                <Search size={18} className="text-blue-600" />
                Platform Queries ({step.queries_detail.length}):
              </h4>
              <div className="space-y-3">
                {step.queries_detail.map((query, idx) => (
                  <PlatformQueryCard key={idx} query={query} />
                ))}
              </div>
            </div>
          )}
          
          {/* Hypotheses Detail */}
          {step.hypotheses_detail && step.hypotheses_detail.length > 0 && (
            <div>
              <h4 className="font-semibold text-slate-900 mb-3 flex items-center gap-2">
                <Lightbulb size={18} className="text-yellow-600" />
                Generated Hypotheses ({step.hypotheses_detail.length}):
              </h4>
              <div className="space-y-2">
                {step.hypotheses_detail.map((hyp, idx) => (
                  <div key={idx} className="border border-slate-200 rounded-lg p-3 bg-slate-50">
                    <div className="flex items-center justify-between mb-2">
                      <h5 className="font-medium text-slate-900">{hyp.title}</h5>
                      <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                        {(hyp.confidence * 100).toFixed(0)}% confidence
                      </span>
                    </div>
                    <p className="text-sm text-slate-700 mb-2">{hyp.explanation}</p>
                    {hyp.evidence && hyp.evidence.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-slate-200">
                        <p className="text-xs font-medium text-slate-600 mb-1">Evidence:</p>
                        <ul className="text-xs text-slate-600 space-y-1">
                          {hyp.evidence.map((e, i) => (
                            <li key={i}>• {e}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Recommendations Detail */}
          {step.recommendations_detail && step.recommendations_detail.length > 0 && (
            <div>
              <h4 className="font-semibold text-slate-900 mb-3 flex items-center gap-2">
                <ListChecks size={18} className="text-purple-600" />
                Generated Recommendations ({step.recommendations_detail.length}):
              </h4>
              <div className="space-y-2">
                {step.recommendations_detail.map((rec, idx) => (
                  <div key={idx} className="border border-slate-200 rounded-lg p-3 bg-slate-50">
                    <div className="flex items-center justify-between mb-2">
                      <h5 className="font-medium text-slate-900">{rec.title}</h5>
                      <div className="flex items-center gap-2">
                        <span className={`text-xs px-2 py-1 rounded ${
                          rec.priority === 'high' ? 'bg-red-100 text-red-700' :
                          rec.priority === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-green-100 text-green-700'
                        }`}>
                          {rec.priority.toUpperCase()}
                        </span>
                      </div>
                    </div>
                    <p className="text-sm text-slate-700 mb-2">{rec.description}</p>
                    <div className="flex gap-3 text-xs text-slate-600 mb-2">
                      <span>Impact: {rec.impact_score}/10</span>
                      <span>Effort: {rec.effort_score}/10</span>
                      <span>ROI: {(rec.impact_score / Math.max(rec.effort_score, 1)).toFixed(2)}</span>
                    </div>
                    {rec.action_items && rec.action_items.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-slate-200">
                        <p className="text-xs font-medium text-slate-600 mb-1">Action Items:</p>
                        <ul className="text-xs text-slate-600 space-y-1">
                          {rec.action_items.map((item, i) => (
                            <li key={i}>• {item}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Evaluation Results */}
          {step.evaluation_results && (
            <div>
              <h4 className="font-semibold text-slate-900 mb-3 flex items-center gap-2">
                <CheckCircle2 size={18} className="text-purple-600" />
                Reflexion Self-Critique Results:
              </h4>
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 space-y-3">
                <div className="grid grid-cols-3 gap-3">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-purple-600">
                      {step.evaluation_results.hypotheses_improved || 0}
                    </div>
                    <div className="text-xs text-purple-700">Hypotheses Improved</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-indigo-600">
                      {step.evaluation_results.avg_hypothesis_quality || 'N/A'}
                    </div>
                    <div className="text-xs text-indigo-700">Avg Quality Score</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {step.evaluation_results.reflexion_iterations || 1}
                    </div>
                    <div className="text-xs text-green-700">Reflexion Iterations</div>
                  </div>
                </div>
                <div className="text-sm text-purple-800 bg-purple-100 rounded p-3">
                  <strong>Reflexion Pattern:</strong> AI evaluated its own hypotheses, identified weaknesses, 
                  and regenerated improved versions for higher quality outputs.
                </div>
              </div>
            </div>
          )}

          {/* LLM Output */}
          {step.llm_output && (
            <div>
              <h4 className="font-semibold text-slate-900 mb-2 flex items-center gap-2">
                {step.type === 'planning' && '📋'}
                {step.type === 'hypothesis' && '💡'}
                {step.type === 'recommendations' && '✨'}
                {step.agent_name} Output:
              </h4>
              <div className="bg-slate-50 border border-slate-200 rounded p-4">
                <pre className="text-sm text-slate-700 whitespace-pre-wrap font-mono">
                  {step.llm_output}
                </pre>
              </div>
            </div>
          )}

          {/* Results Summary */}
          {step.results && (
            <div className="bg-green-50 border border-green-200 p-3 rounded">
              <h4 className="font-semibold text-green-900 mb-2">Results:</h4>
              <div className="text-sm text-green-800 space-y-1">
                {Object.entries(step.results).map(([key, value]) => (
                  <div key={key} className="flex justify-between">
                    <span className="capitalize">{key.replace(/_/g, ' ')}:</span>
                    <span className="font-medium">{JSON.stringify(value)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Errors */}
          {step.errors && step.errors.length > 0 && (
            <div className="bg-red-50 border border-red-200 p-3 rounded">
              <h4 className="font-semibold text-red-900 mb-2">Issues:</h4>
              <div className="space-y-1">
                {step.errors.map((error, idx) => (
                  <p key={idx} className="text-sm text-red-700">• {error}</p>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

const PlatformQueryCard = ({ query }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getPlatformIcon = (platform) => {
    return platform === 'chatgpt' ? '💬' : '🔍';
  };

  const getPlatformName = (platform) => {
    return platform === 'chatgpt' ? 'ChatGPT' : 'Perplexity';
  };

  return (
    <div className="border border-slate-200 rounded-lg overflow-hidden">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 bg-slate-50 hover:bg-slate-100 flex items-center justify-between transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-xl">{getPlatformIcon(query.platform)}</span>
          <div className="text-left">
            <div className="font-medium text-slate-900">
              {getPlatformName(query.platform)}
            </div>
            <div className="text-xs text-slate-600">"{query.query}"</div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {query.status === 'completed' && <CheckCircle2 className="text-green-500" size={16} />}
          {query.status === 'running' && <Loader2 className="animate-spin text-blue-500" size={16} />}
          {isExpanded ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
        </div>
      </button>

      {isExpanded && query.response && (
        <div className="p-4 bg-white space-y-3">
          {/* Response Content */}
          <div>
            <h5 className="text-sm font-semibold text-slate-700 mb-2">
              {query.platform === 'chatgpt' ? '💬 OpenAI Response:' : '🔍 Perplexity Search Result:'}
            </h5>
            <div className="bg-slate-50 border border-slate-200 rounded p-3">
              <p className="text-sm text-slate-700 whitespace-pre-wrap">
                {query.response}
              </p>
            </div>
          </div>

          {/* Citations (for Perplexity) */}
          {query.citations && query.citations.length > 0 && (
            <div>
              <h5 className="text-sm font-semibold text-slate-700 mb-2">
                📚 Sources ({query.citations.length}):
              </h5>
              <div className="bg-purple-50 border border-purple-200 rounded p-3">
                <ul className="space-y-1">
                  {query.citations.slice(0, 5).map((cite, idx) => (
                    <li key={idx} className="text-xs text-purple-800">
                      {idx + 1}. <a href={cite} target="_blank" rel="noopener noreferrer" className="hover:underline">
                        {cite}
                      </a>
                    </li>
                  ))}
                  {query.citations.length > 5 && (
                    <li className="text-xs text-purple-600 font-medium">
                      ... and {query.citations.length - 5} more sources
                    </li>
                  )}
                </ul>
              </div>
            </div>
          )}

          {/* Brand Detection */}
          {query.brand_mentioned !== undefined && (
            <div className="flex items-center gap-4 text-sm">
              <div className={`px-3 py-1 rounded ${
                query.brand_mentioned 
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-600'
              }`}>
                Brand: {query.brand_mentioned ? '✓ Mentioned' : '✗ Not Mentioned'}
              </div>
              {query.competitors_mentioned && query.competitors_mentioned.length > 0 && (
                <div className="px-3 py-1 bg-blue-100 text-blue-700 rounded">
                  Competitors: {query.competitors_mentioned.join(', ')}
                </div>
              )}
            </div>
          )}

          {/* Timing */}
          {query.duration && (
            <div className="text-xs text-slate-500 flex items-center gap-1">
              <Clock size={12} />
              Completed in {query.duration.toFixed(2)}s
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RealTimeProgress;

