"""Semantic search using vector embeddings."""

from typing import Any, Dict, List, Optional
from app.memory.vector_store import get_vector_store


class SemanticSearch:
    """
    Semantic search engine for finding similar content.
    """
    
    def __init__(self):
        """Initialize semantic search."""
        self.vector_store = get_vector_store()
    
    def index(
        self,
        text: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Index text with embedding.
        
        Args:
            text: Text to index
            embedding: Text embedding
            metadata: Optional metadata
            
        Returns:
            Document ID
        """
        return self.vector_store.add(text, embedding, metadata)
    
    def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar content.
        
        Args:
            query_embedding: Query embedding
            limit: Max results
            threshold: Similarity threshold
            
        Returns:
            List of results with text and score
        """
        results = self.vector_store.search(
            query_embedding,
            limit=limit,
            threshold=threshold
        )
        
        return [
            {
                "text": text,
                "similarity_score": score
            }
            for text, score in results
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get search statistics."""
        return self.vector_store.get_stats()


# Global semantic search instance
_semantic_search: Optional[SemanticSearch] = None


def get_semantic_search() -> SemanticSearch:
    """Get or create global semantic search."""
    global _semantic_search
    if _semantic_search is None:
        _semantic_search = SemanticSearch()
    return _semantic_search
