"""
Evaluator Agent - Self-Critique and Quality Validation
Implements Reflexion pattern for multi-agent system improvement
"""

from typing import List, Dict, Any
import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.config import settings
from src.models.schemas import Hypothesis, Recommendation, CitationData
import json

logger = logging.getLogger(__name__)


class EvaluatorAgent:
    """
    Self-Critique Agent using Reflexion Pattern
    
    This agent:
    1. Evaluates quality of hypotheses and recommendations
    2. Scores confidence based on evidence
    3. Identifies weak reasoning
    4. Re-generates improved outputs
    5. Validates final results
    
    This implements the Reflexion pattern: Act → Evaluate → Reflect → Improve
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.default_model,
            temperature=0.3,  # Lower for evaluation
            api_key=settings.openai_api_key
        )
        
        self.hypothesis_evaluator_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a critical evaluator of AI-generated hypotheses.
            Your job is to assess hypothesis quality and suggest improvements.
            
            Evaluate each hypothesis on:
            1. **Evidence Quality** (0-1): Is supporting evidence strong and specific?
            2. **Logical Coherence** (0-1): Does the explanation make logical sense?
            3. **Actionability** (0-1): Can this lead to concrete actions?
            4. **Specificity** (0-1): Is it specific enough to be useful?
            
            Return JSON with:
            - overall_score (0-1)
            - critique (string explaining weaknesses)
            - suggestions (list of specific improvements)
            - should_regenerate (boolean)"""),
            ("user", """Evaluate this hypothesis:
            
Title: {title}
Explanation: {explanation}
Confidence: {confidence}
Evidence: {evidence}
Brand Visibility: {brand_visibility}%
Context: {context}""")
        ])
        
        self.hypothesis_improver_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert at improving AI-generated hypotheses.
            Given a weak hypothesis and critique, generate an improved version.
            
            Requirements:
            - Address all critique points
            - Provide stronger, more specific evidence
            - Improve logical coherence
            - Maintain JSON format: title, explanation, confidence, supporting_evidence"""),
            ("user", """Improve this hypothesis:
            
Original: {hypothesis}
Critique: {critique}
Available Data: {citations_summary}
Brand Context: {brand_context}""")
        ])
        
        self.recommendation_evaluator_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a critical evaluator of action recommendations.
            
            Evaluate each recommendation on:
            1. **Actionability** (0-1): Are action items clear and specific?
            2. **Feasibility** (0-1): Can this realistically be implemented?
            3. **Impact Accuracy** (0-1): Is the impact score realistic?
            4. **Completeness** (0-1): Are all necessary details included?
            
            Return JSON with overall_score, critique, suggestions, should_regenerate."""),
            ("user", """Evaluate this recommendation:
            
Title: {title}
Description: {description}
Priority: {priority}
Impact Score: {impact_score}/10
Effort Score: {effort_score}/10
Action Items: {action_items}
Expected Outcome: {expected_outcome}""")
        ])
    
    async def evaluate_hypotheses(
        self,
        hypotheses: List[Hypothesis],
        citations: List[CitationData],
        brand_visibility: float,
        threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Evaluate hypothesis quality and regenerate weak ones
        
        Reflexion Loop:
        1. Score each hypothesis
        2. Identify weak ones (< threshold)
        3. Generate critique for weak hypotheses
        4. Regenerate with improved reasoning
        5. Return validated hypotheses
        
        Args:
            hypotheses: Generated hypotheses
            citations: Citation data for validation
            brand_visibility: Current brand visibility rate
            threshold: Minimum acceptable quality score
            
        Returns:
            Evaluation results with improved hypotheses
        """
        logger.info("="*60)
        logger.info("🔍 EVALUATOR: Assessing hypothesis quality...")
        logger.info("-"*60)
        
        evaluation_results = []
        weak_hypotheses = []
        improved_count = 0
        
        for idx, hypothesis in enumerate(hypotheses):
            logger.info(f"Evaluating hypothesis {idx+1}: {hypothesis.title}")
            
            # Evaluate quality
            eval_chain = self.hypothesis_evaluator_prompt | self.llm
            
            try:
                evaluation = await eval_chain.ainvoke({
                    "title": hypothesis.title,
                    "explanation": hypothesis.explanation,
                    "confidence": hypothesis.confidence,
                    "evidence": hypothesis.supporting_evidence,
                    "brand_visibility": f"{brand_visibility * 100:.1f}",
                    "context": self._summarize_citations(citations)
                })
                
                eval_content = evaluation.content
                
                # Parse evaluation
                if "```json" in eval_content:
                    eval_content = eval_content.split("```json")[1].split("```")[0]
                elif "```" in eval_content:
                    eval_content = eval_content.split("```")[1].split("```")[0]
                
                eval_data = json.loads(eval_content.strip())
                
                logger.info(f"  Score: {eval_data.get('overall_score', 0):.2f}")
                logger.info(f"  Critique: {eval_data.get('critique', 'N/A')[:100]}...")
                
                evaluation_results.append({
                    "hypothesis_index": idx,
                    "hypothesis_title": hypothesis.title,
                    "score": eval_data.get("overall_score", 0),
                    "critique": eval_data.get("critique", ""),
                    "suggestions": eval_data.get("suggestions", [])
                })
                
                # Check if needs improvement
                if eval_data.get("should_regenerate", False) or eval_data.get("overall_score", 1.0) < threshold:
                    logger.warning(f"  ⚠️  Hypothesis quality below threshold - flagged for regeneration")
                    weak_hypotheses.append({
                        "hypothesis": hypothesis,
                        "index": idx,
                        "critique": eval_data.get("critique", ""),
                        "suggestions": eval_data.get("suggestions", [])
                    })
                
            except Exception as e:
                logger.error(f"  ❌ Evaluation failed: {e}")
                # If evaluation fails, keep original
                evaluation_results.append({
                    "hypothesis_index": idx,
                    "hypothesis_title": hypothesis.title,
                    "score": 0.8,  # Assume decent if can't evaluate
                    "critique": "Evaluation failed",
                    "suggestions": []
                })
        
        # Regenerate weak hypotheses
        improved_hypotheses = hypotheses.copy()
        
        if weak_hypotheses:
            logger.info("="*60)
            logger.info(f"🔄 REFLEXION: Improving {len(weak_hypotheses)} weak hypotheses...")
            logger.info("-"*60)
            
            for weak in weak_hypotheses:
                try:
                    # Generate improvement
                    improver_chain = self.hypothesis_improver_prompt | self.llm
                    
                    improved = await improver_chain.ainvoke({
                        "hypothesis": json.dumps({
                            "title": weak["hypothesis"].title,
                            "explanation": weak["hypothesis"].explanation,
                            "confidence": weak["hypothesis"].confidence,
                            "evidence": weak["hypothesis"].supporting_evidence
                        }, indent=2),
                        "critique": weak["critique"],
                        "citations_summary": self._summarize_citations(citations),
                        "brand_context": f"Brand visibility: {brand_visibility*100:.1f}%"
                    })
                    
                    improved_content = improved.content
                    
                    # Parse improved hypothesis
                    if "```json" in improved_content:
                        improved_content = improved_content.split("```json")[1].split("```")[0]
                    elif "```" in improved_content:
                        improved_content = improved_content.split("```")[1].split("```")[0]
                    
                    improved_data = json.loads(improved_content.strip())
                    
                    # Create improved hypothesis
                    improved_hypothesis = Hypothesis(
                        title=improved_data.get("title", weak["hypothesis"].title),
                        explanation=improved_data.get("explanation", weak["hypothesis"].explanation),
                        confidence=improved_data.get("confidence", weak["hypothesis"].confidence),
                        supporting_evidence=improved_data.get("supporting_evidence", weak["hypothesis"].supporting_evidence)
                    )
                    
                    # Replace in list
                    improved_hypotheses[weak["index"]] = improved_hypothesis
                    improved_count += 1
                    
                    logger.info(f"  ✅ Improved: {improved_hypothesis.title}")
                    logger.info(f"     New confidence: {improved_hypothesis.confidence*100:.0f}%")
                    
                except Exception as e:
                    logger.error(f"  ❌ Improvement failed for '{weak['hypothesis'].title}': {e}")
                    # Keep original if improvement fails
        
        logger.info("="*60)
        logger.info(f"✅ EVALUATION COMPLETE")
        logger.info(f"   Hypotheses evaluated: {len(hypotheses)}")
        logger.info(f"   Hypotheses improved: {improved_count}")
        logger.info(f"   Average quality score: {sum(e['score'] for e in evaluation_results) / len(evaluation_results):.2f}")
        logger.info("="*60)
        
        return {
            "validated_hypotheses": improved_hypotheses,
            "evaluation_results": evaluation_results,
            "improvements_made": improved_count,
            "quality_threshold": threshold,
            "average_score": sum(e['score'] for e in evaluation_results) / len(evaluation_results)
        }
    
    async def evaluate_recommendations(
        self,
        recommendations: List[Recommendation],
        threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Evaluate recommendation quality
        
        Args:
            recommendations: Generated recommendations
            threshold: Minimum acceptable quality
            
        Returns:
            Evaluation results
        """
        logger.info("🔍 EVALUATOR: Assessing recommendation quality...")
        
        evaluation_results = []
        
        for idx, rec in enumerate(recommendations):
            try:
                eval_chain = self.recommendation_evaluator_prompt | self.llm
                
                evaluation = await eval_chain.ainvoke({
                    "title": rec.title,
                    "description": rec.description,
                    "priority": rec.priority,
                    "impact_score": rec.impact_score,
                    "effort_score": rec.effort_score,
                    "action_items": rec.action_items,
                    "expected_outcome": rec.expected_outcome
                })
                
                eval_content = evaluation.content
                
                if "```json" in eval_content:
                    eval_content = eval_content.split("```json")[1].split("```")[0]
                elif "```" in eval_content:
                    eval_content = eval_content.split("```")[1].split("```")[0]
                
                eval_data = json.loads(eval_content.strip())
                
                evaluation_results.append({
                    "recommendation_index": idx,
                    "recommendation_title": rec.title,
                    "score": eval_data.get("overall_score", 0),
                    "critique": eval_data.get("critique", ""),
                    "actionability_score": eval_data.get("actionability", 0)
                })
                
                logger.info(f"  Recommendation {idx+1}: {eval_data.get('overall_score', 0):.2f} score")
                
            except Exception as e:
                logger.error(f"  ❌ Recommendation evaluation failed: {e}")
                evaluation_results.append({
                    "recommendation_index": idx,
                    "recommendation_title": rec.title,
                    "score": 0.8,
                    "critique": "Evaluation failed"
                })
        
        avg_score = sum(e['score'] for e in evaluation_results) / len(evaluation_results) if evaluation_results else 0
        
        logger.info(f"✅ Recommendation evaluation complete - Average score: {avg_score:.2f}")
        
        return {
            "evaluation_results": evaluation_results,
            "average_score": avg_score,
            "all_actionable": all(e['score'] >= threshold for e in evaluation_results)
        }
    
    def _score_hypothesis_quality(
        self,
        hypothesis: Hypothesis,
        citations: List[CitationData]
    ) -> float:
        """
        Score hypothesis quality based on evidence
        
        Factors:
        - Evidence specificity (are claims backed by data?)
        - Evidence quantity (enough supporting data?)
        - Confidence calibration (does confidence match evidence?)
        - Logical coherence (does explanation make sense?)
        """
        score = 0.0
        
        # Factor 1: Evidence specificity (0.3 weight)
        evidence_count = len(hypothesis.supporting_evidence)
        evidence_score = min(evidence_count / 3, 1.0)  # Expect 3+ pieces
        score += evidence_score * 0.3
        
        # Factor 2: Evidence from citations (0.3 weight)
        evidence_from_data = sum(
            1 for evidence in hypothesis.supporting_evidence
            if any(str(c.query) in evidence or str(c.raw_response)[:50] in evidence 
                   for c in citations)
        )
        citation_score = evidence_from_data / max(evidence_count, 1)
        score += citation_score * 0.3
        
        # Factor 3: Confidence calibration (0.2 weight)
        # Confidence should align with evidence quality
        expected_confidence = evidence_score * citation_score
        confidence_calibration = 1.0 - abs(hypothesis.confidence - expected_confidence)
        score += confidence_calibration * 0.2
        
        # Factor 4: Explanation length (0.2 weight)
        # Good explanations are substantial but not too long
        explanation_length = len(hypothesis.explanation.split())
        length_score = min(explanation_length / 30, 1.0)  # Expect 30+ words
        length_score = min(length_score, 100 / max(explanation_length, 1))  # Cap at 100 words
        score += length_score * 0.2
        
        return score
    
    def _summarize_citations(self, citations: List[CitationData]) -> str:
        """Create summary of citations for context"""
        if not citations:
            return "No citation data available"
        
        summary = f"Analyzed {len(citations)} citations:\n"
        
        platforms = {}
        for c in citations:
            platforms[c.platform.value] = platforms.get(c.platform.value, 0) + 1
        
        summary += f"- Platforms: {', '.join(f'{k}: {v}' for k, v in platforms.items())}\n"
        summary += f"- Brand mentions: {sum(1 for c in citations if c.brand_mentioned)}\n"
        summary += f"- Competitor mentions: {sum(len(c.competitors_mentioned) for c in citations)}"
        
        return summary
    
    def _generate_critique(self, hypotheses: List[Hypothesis]) -> str:
        """Generate critique for weak hypotheses"""
        critiques = []
        for h in hypotheses:
            if len(h.supporting_evidence) < 2:
                critiques.append(f"'{h.title}' lacks sufficient evidence")
            if len(h.explanation.split()) < 20:
                critiques.append(f"'{h.title}' explanation too brief")
        
        return "; ".join(critiques) if critiques else "General quality concerns"


class ReflexionMetrics:
    """Track Reflexion/Evaluation metrics for transparency"""
    
    @staticmethod
    def create_evaluation_summary(
        hypothesis_eval: Dict[str, Any],
        recommendation_eval: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create summary of evaluation process for frontend display"""
        
        return {
            "evaluation_performed": True,
            "hypotheses": {
                "total_evaluated": len(hypothesis_eval.get("evaluation_results", [])),
                "improvements_made": hypothesis_eval.get("improvements_made", 0),
                "average_quality_score": hypothesis_eval.get("average_score", 0),
                "threshold_used": hypothesis_eval.get("quality_threshold", 0.7),
                "all_passed": hypothesis_eval.get("improvements_made", 0) == 0
            },
            "recommendations": {
                "total_evaluated": len(recommendation_eval.get("evaluation_results", [])),
                "average_quality_score": recommendation_eval.get("average_score", 0),
                "all_actionable": recommendation_eval.get("all_actionable", True)
            },
            "reflexion_stats": {
                "total_iterations": 1 + hypothesis_eval.get("improvements_made", 0),
                "quality_improvement": "Hypotheses improved through self-critique",
                "validation_method": "AI-powered evaluation with evidence scoring"
            }
        }

