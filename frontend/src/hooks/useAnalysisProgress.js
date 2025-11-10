import { useState, useCallback } from 'react';

/**
 * Custom hook to track real-time analysis progress
 * Simulates streaming updates from backend
 */
export const useAnalysisProgress = () => {
  const [steps, setSteps] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const initializeSteps = useCallback(() => {
    setSteps([
      {
        id: 'planning',
        type: 'planning',
        title: 'Strategic Planning',
        subtitle: 'Creating analysis strategy with AI',
        agent_name: 'Planning Agent',
        description: 'Using OpenAI to analyze query intent and create execution plan',
        status: 'pending',
        llm_output: null,
        results: null,
        duration: null
      },
      {
        id: 'data_collection',
        type: 'data_collection',
        title: 'Data Collection',
        subtitle: 'Querying ChatGPT and Perplexity in parallel',
        description: 'Executing parallel queries across AI platforms',
        status: 'pending',
        queries: [],
        results: null,
        duration: null
      },
      {
        id: 'analysis',
        type: 'analysis',
        title: 'Pattern Analysis',
        subtitle: 'Analyzing visibility patterns and competitive gaps',
        description: 'Statistical analysis of citation data',
        status: 'pending',
        results: null,
        duration: null
      },
      {
        id: 'hypothesis',
        type: 'hypothesis',
        title: 'Hypothesis Generation',
        subtitle: 'AI explaining WHY patterns exist',
        agent_name: 'Hypothesis Agent',
        description: 'Using OpenAI to generate causal explanations',
        status: 'pending',
        llm_output: null,
        results: null,
        duration: null
      },
      {
        id: 'recommendations',
        type: 'recommendations',
        title: 'Recommendations',
        subtitle: 'AI suggesting HOW to improve',
        agent_name: 'Recommender Agent',
        description: 'Using OpenAI to generate actionable recommendations',
        status: 'pending',
        llm_output: null,
        results: null,
        duration: null
      },
      {
        id: 'evaluation',
        type: 'evaluation',
        title: 'Quality Validation (Reflexion)',
        subtitle: 'AI self-critique and improvement',
        agent_name: 'Evaluator Agent',
        description: 'Evaluating output quality and improving weak hypotheses through Reflexion pattern',
        status: 'pending',
        llm_output: null,
        evaluation_results: null,
        duration: null
      },
      {
        id: 'synthesis',
        type: 'synthesis',
        title: 'Synthesis',
        subtitle: 'Combining all insights',
        description: 'Creating executive summary',
        status: 'pending',
        results: null,
        duration: null
      }
    ]);
  }, []);

  const updateStep = useCallback((stepId, updates) => {
    setSteps(prev => prev.map(step => 
      step.id === stepId ? { ...step, ...updates } : step
    ));
  }, []);

  const addQueryResult = useCallback((stepId, queryData) => {
    setSteps(prev => prev.map(step => 
      step.id === stepId 
        ? { ...step, queries: [...(step.queries || []), queryData] }
        : step
    ));
  }, []);

  const startAnalysis = useCallback(() => {
    setIsAnalyzing(true);
    initializeSteps();
  }, [initializeSteps]);

  const completeAnalysis = useCallback(() => {
    setIsAnalyzing(false);
  }, []);

  return {
    steps,
    isAnalyzing,
    startAnalysis,
    completeAnalysis,
    updateStep,
    addQueryResult
  };
};

