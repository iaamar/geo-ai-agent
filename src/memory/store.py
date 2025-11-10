"""Vector store and memory management using ChromaDB"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from src.config import settings
from src.models.schemas import AnalysisResult


class MemoryStore:
    """
    Vector store for storing and retrieving historical GEO analyses
    """
    
    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory=settings.chroma_db_path,
            anonymized_telemetry=False
        ))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="geo_analyses",
            metadata={"description": "Historical GEO analysis results"}
        )
    
    def save_analysis(self, analysis: AnalysisResult) -> str:
        """
        Save analysis to vector store
        
        Args:
            analysis: Analysis result to save
            
        Returns:
            Saved document ID
        """
        # Create searchable text
        doc_text = self._create_searchable_text(analysis)
        
        # Create metadata
        metadata = {
            "analysis_id": analysis.id,
            "timestamp": analysis.timestamp.isoformat(),
            "query": analysis.request.query,
            "brand": analysis.request.brand_domain,
            "visibility_rate": analysis.visibility_scores.brand_score.mention_rate,
            "num_hypotheses": len(analysis.hypotheses),
            "num_recommendations": len(analysis.recommendations)
        }
        
        # Save to ChromaDB
        self.collection.add(
            documents=[doc_text],
            metadatas=[metadata],
            ids=[analysis.id]
        )
        
        return analysis.id
    
    def search_similar_analyses(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar historical analyses
        
        Args:
            query: Search query
            limit: Number of results
            
        Returns:
            List of similar analyses
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        
        similar = []
        if results["metadatas"]:
            for metadata, distance in zip(results["metadatas"][0], results["distances"][0]):
                similar.append({
                    "analysis_id": metadata["analysis_id"],
                    "query": metadata["query"],
                    "brand": metadata["brand"],
                    "visibility_rate": metadata["visibility_rate"],
                    "similarity_score": 1 - distance,  # Convert distance to similarity
                    "timestamp": metadata["timestamp"]
                })
        
        return similar
    
    def get_analysis(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific analysis by ID
        
        Args:
            analysis_id: Analysis ID
            
        Returns:
            Analysis metadata or None
        """
        try:
            result = self.collection.get(
                ids=[analysis_id],
                include=["metadatas", "documents"]
            )
            
            if result["metadatas"]:
                return {
                    "id": analysis_id,
                    "metadata": result["metadatas"][0],
                    "content": result["documents"][0]
                }
            
            return None
            
        except Exception as e:
            print(f"Error retrieving analysis: {e}")
            return None
    
    def get_recent_analyses(
        self,
        brand: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent analyses, optionally filtered by brand
        
        Args:
            brand: Optional brand filter
            limit: Number of results
            
        Returns:
            List of recent analyses
        """
        where_filter = {"brand": brand} if brand else None
        
        try:
            results = self.collection.get(
                where=where_filter,
                limit=limit,
                include=["metadatas"]
            )
            
            analyses = []
            if results["metadatas"]:
                for metadata in results["metadatas"]:
                    analyses.append(metadata)
            
            # Sort by timestamp
            analyses.sort(key=lambda x: x["timestamp"], reverse=True)
            
            return analyses[:limit]
            
        except Exception as e:
            print(f"Error getting recent analyses: {e}")
            return []
    
    def _create_searchable_text(self, analysis: AnalysisResult) -> str:
        """
        Create searchable text representation of analysis
        
        Args:
            analysis: Analysis result
            
        Returns:
            Searchable text
        """
        parts = [
            f"Query: {analysis.request.query}",
            f"Brand: {analysis.request.brand_domain}",
            f"Visibility: {analysis.visibility_scores.brand_score.mention_rate * 100:.1f}%",
            "Hypotheses:",
            *[f"- {h.title}: {h.explanation}" for h in analysis.hypotheses],
            "Recommendations:",
            *[f"- {r.title}: {r.description}" for r in analysis.recommendations],
            f"Summary: {analysis.summary}"
        ]
        
        return "\n".join(parts)
    
    def clear_collection(self):
        """Clear all data from collection (use with caution)"""
        self.client.delete_collection("geo_analyses")
        self.collection = self.client.get_or_create_collection(
            name="geo_analyses",
            metadata={"description": "Historical GEO analysis results"}
        )



