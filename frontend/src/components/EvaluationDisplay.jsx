import React, { useState } from 'react';
import { CheckCircle2, AlertTriangle, RefreshCw, TrendingUp, Award } from 'lucide-react';

/**
 * EvaluationDisplay Component
 * Shows self-critique and quality validation results (Reflexion pattern)
 */
const EvaluationDisplay = ({ evaluationMetrics }) => {
  if (!evaluationMetrics || !evaluationMetrics.evaluation_performed) {
    return null;
  }

  const { hypotheses, recommendations, reflexion_stats } = evaluationMetrics;

  return (
    <div className="bg-gradient-to-r from-purple-50 to-indigo-50 border-2 border-purple-300 rounded-lg p-6 space-y-4">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 bg-purple-600 rounded-lg">
          <RefreshCw className="text-white" size={24} />
        </div>
        <div>
          <h3 className="text-xl font-bold text-purple-900">
            🔍 Self-Critique & Quality Validation
          </h3>
          <p className="text-sm text-purple-700">
            AI system evaluated and improved its own outputs using Reflexion pattern
          </p>
        </div>
      </div>

      {/* Reflexion Stats Summary */}
      <div className="grid grid-cols-4 gap-4">
        <div className="bg-white rounded-lg p-4 border border-purple-200">
          <div className="flex items-center gap-2 mb-2">
            <Award className="text-purple-600" size={18} />
            <span className="text-sm font-medium text-purple-900">Quality Score</span>
          </div>
          <div className="text-2xl font-bold text-purple-600">
            {(hypotheses.average_quality_score * 100).toFixed(0)}%
          </div>
          <p className="text-xs text-purple-700 mt-1">Hypothesis Quality</p>
        </div>

        <div className="bg-white rounded-lg p-4 border border-purple-200">
          <div className="flex items-center gap-2 mb-2">
            <RefreshCw className="text-indigo-600" size={18} />
            <span className="text-sm font-medium text-indigo-900">Improvements</span>
          </div>
          <div className="text-2xl font-bold text-indigo-600">
            {hypotheses.improvements_made}
          </div>
          <p className="text-xs text-indigo-700 mt-1">
            {hypotheses.improvements_made === 0 ? 'All Passed First Time' : 'Hypotheses Regenerated'}
          </p>
        </div>

        <div className="bg-white rounded-lg p-4 border border-purple-200">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="text-green-600" size={18} />
            <span className="text-sm font-medium text-green-900">Iterations</span>
          </div>
          <div className="text-2xl font-bold text-green-600">
            {reflexion_stats.total_iterations}
          </div>
          <p className="text-xs text-green-700 mt-1">Reflexion Cycles</p>
        </div>

        <div className="bg-white rounded-lg p-4 border border-purple-200">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle2 className="text-blue-600" size={18} />
            <span className="text-sm font-medium text-blue-900">Status</span>
          </div>
          <div className="text-lg font-bold text-blue-600">
            {hypotheses.all_passed ? '✓ Validated' : '⚠ Improved'}
          </div>
          <p className="text-xs text-blue-700 mt-1">Final Quality</p>
        </div>
      </div>

      {/* Detailed Evaluation */}
      <div className="bg-white rounded-lg p-4 border border-purple-200">
        <h4 className="font-semibold text-purple-900 mb-3">Evaluation Details:</h4>
        
        <div className="grid grid-cols-2 gap-4">
          {/* Hypotheses */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-700">Hypotheses Evaluated</span>
              <span className="text-sm font-bold">{hypotheses.total_evaluated}</span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-700">Quality Threshold</span>
              <span className="text-sm font-bold">{(hypotheses.threshold_used * 100).toFixed(0)}%</span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-700">Improvements Made</span>
              <span className={`text-sm font-bold ${
                hypotheses.improvements_made > 0 ? 'text-orange-600' : 'text-green-600'
              }`}>
                {hypotheses.improvements_made} {hypotheses.improvements_made === 0 && '(Perfect!)'}
              </span>
            </div>
          </div>

          {/* Recommendations */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-700">Recommendations Evaluated</span>
              <span className="text-sm font-bold">{recommendations.total_evaluated}</span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-700">Avg Quality Score</span>
              <span className="text-sm font-bold text-green-600">
                {(recommendations.average_quality_score * 100).toFixed(0)}%
              </span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-slate-700">All Actionable</span>
              <span className={`text-sm font-bold ${
                recommendations.all_actionable ? 'text-green-600' : 'text-yellow-600'
              }`}>
                {recommendations.all_actionable ? '✓ Yes' : '⚠ Needs Review'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Reflexion Process Info */}
      <div className="bg-purple-100 border border-purple-300 rounded-lg p-4">
        <h4 className="font-semibold text-purple-900 mb-2 flex items-center gap-2">
          <RefreshCw size={16} />
          Reflexion Pattern Applied
        </h4>
        <div className="text-sm text-purple-800 space-y-2">
          <p><strong>Method:</strong> {reflexion_stats.validation_method}</p>
          <p><strong>Process:</strong> {reflexion_stats.quality_improvement}</p>
          <p className="text-xs mt-2 text-purple-700">
            <strong>What is Reflexion?</strong> An AI technique where the system evaluates 
            its own outputs, identifies weaknesses, and regenerates improved versions. 
            This creates self-improving AI that learns from its mistakes.
          </p>
        </div>
      </div>

      {/* Quality Badge */}
      {hypotheses.all_passed && recommendations.all_actionable && (
        <div className="bg-green-50 border border-green-300 rounded-lg p-3 flex items-center gap-2">
          <CheckCircle2 className="text-green-600" size={20} />
          <span className="text-sm font-medium text-green-800">
            All outputs passed quality validation on first generation - High quality analysis!
          </span>
        </div>
      )}

      {hypotheses.improvements_made > 0 && (
        <div className="bg-orange-50 border border-orange-300 rounded-lg p-3 flex items-center gap-2">
          <AlertTriangle className="text-orange-600" size={20} />
          <span className="text-sm font-medium text-orange-800">
            {hypotheses.improvements_made} hypothesis(es) were below quality threshold and regenerated for better accuracy
          </span>
        </div>
      )}
    </div>
  );
};

export default EvaluationDisplay;

