"""Vector store for semantic search (Qdrant integration)."""

from typing import Any, Dict, List, Optional, Tuple
import hashlib


class VectorStore:
    """
    Vector database for semantic search.
    
    Stores and retrieves embeddings for semantic similarity.
    """
    
    def __init__(self, dimension: int = 384):
        """
        Initialize vector store.
        
        Args:
            dimension: Embedding dimension
        """
        self.dimension = dimension
        # Placeholder - real implementation uses Qdrant
        self.vectors: Dict[str, Dict[str, Any]] = {}
    
    def add(
        self,
        text: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add vector with metadata.
        
        Args:
            text: Original text
            embedding: Vector embedding
            metadata: Optional metadata
            
        Returns:
            Vector ID
        """
        # Generate ID from text hash
        vector_id = hashlib.md5(text.encode()).hexdigest()
        
        if len(embedding) != self.dimension:
            raise ValueError(
                f"Embedding dimension {len(embedding)} "
                f"does not match store dimension {self.dimension}"
            )
        
        self.vectors[vector_id] = {
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {}
        }
        
        return vector_id
    
    def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        threshold: float = 0.5
    ) -> List[Tuple[str, float]]:
        """
        Search similar vectors.
        
        Args:
            query_embedding: Query vector
            limit: Max results
            threshold: Similarity threshold
            
        Returns:
            List of (text, similarity_score) tuples
        """
        if len(query_embedding) != self.dimension:
            raise ValueError(
                f"Query embedding dimension {len(query_embedding)} "
                f"does not match store dimension {self.dimension}"
            )
        
        results = []
        
        for vector_id, vector_data in self.vectors.items():
            similarity = self._cosine_similarity(
                query_embedding,
                vector_data["embedding"]
            )
            
            if similarity >= threshold:
                results.append((
                    vector_data["text"],
                    similarity
                ))
        
        # Sort by similarity (descending) and limit
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]
    
    def delete(self, vector_id: str) -> bool:
        """
        Delete vector by ID.
        
        Args:
            vector_id: Vector ID
            
        Returns:
            True if deleted
        """
        if vector_id in self.vectors:
            del self.vectors[vector_id]
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get store statistics."""
        return {
            "total_vectors": len(self.vectors),
            "dimension": self.dimension
        }
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score (0-1)
        """
        if not vec1 or not vec2:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a ** 2 for a in vec1) ** 0.5
        norm2 = sum(b ** 2 for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


# Global vector store instance
_vector_store: Optional[VectorStore] = None


def get_vector_store(dimension: int = 384) -> VectorStore:
    """Get or create global vector store."""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore(dimension=dimension)
    return _vector_store
