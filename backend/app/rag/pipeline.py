"""RAG (Retrieval-Augmented Generation) pipeline."""

from typing import Any, Dict, List, Optional
from pathlib import Path
import hashlib


class DocumentUploader:
    """
    Handle document uploads for RAG system.
    """
    
    # Allowed file types
    ALLOWED_TYPES = {".txt", ".pdf", ".md", ".json", ".csv"}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    def __init__(self, storage_dir: Optional[str] = None):
        """Initialize uploader."""
        self.storage_dir = Path(storage_dir) if storage_dir else Path("./documents")
        self.storage_dir.mkdir(exist_ok=True)
        self.uploaded_files: Dict[str, Dict[str, Any]] = {}
    
    async def upload(
        self,
        file_path: str,
        document_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Upload a document.
        
        Args:
            file_path: Path to file
            document_type: Type of document
            
        Returns:
            Upload metadata
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                return {"success": False, "error": "File not found"}
            
            if path.suffix.lower() not in self.ALLOWED_TYPES:
                return {"success": False, "error": "File type not allowed"}
            
            if path.stat().st_size > self.MAX_FILE_SIZE:
                return {"success": False, "error": "File too large"}
            
            # Generate document ID
            doc_id = hashlib.md5(f"{path.name}{path.stat().st_size}".encode()).hexdigest()
            
            # Store metadata
            self.uploaded_files[doc_id] = {
                "file_name": path.name,
                "file_path": str(path),
                "document_type": document_type,
                "size": path.stat().st_size,
                "doc_id": doc_id
            }
            
            return {
                "success": True,
                "doc_id": doc_id,
                "file_name": path.name
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get document metadata."""
        return self.uploaded_files.get(doc_id)
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all uploaded documents."""
        return list(self.uploaded_files.values())


class TextChunker:
    """
    Split text into chunks for embeddings.
    """
    
    def __init__(
        self,
        chunk_size: int = 512,
        overlap: int = 50
    ):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Size of chunks
            overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Split text into chunks.
        
        Args:
            text: Text to chunk
            metadata: Optional metadata
            
        Returns:
            List of chunks with metadata
        """
        chunks = []
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        current_chunk = ""
        chunk_num = 0
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunk_num += 1
                    chunks.append({
                        "text": current_chunk.strip(),
                        "chunk_id": f"chunk-{chunk_num}",
                        "metadata": metadata or {}
                    })
                current_chunk = para + "\n\n"
        
        # Add last chunk
        if current_chunk:
            chunk_num += 1
            chunks.append({
                "text": current_chunk.strip(),
                "chunk_id": f"chunk-{chunk_num}",
                "metadata": metadata or {}
            })
        
        return chunks


class EmbeddingGenerator:
    """
    Generate embeddings for text chunks.
    """
    
    def __init__(self, model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding generator.
        
        Args:
            model: Embedding model name
        """
        self.model = model
        # Placeholder - real implementation would load actual model
        self.dimension = 384
    
    async def generate(
        self,
        text: str
    ) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        # Placeholder implementation
        # Real implementation would use transformer model
        
        # Create a simple deterministic "embedding" based on text
        # In production, use actual embedding model
        import hashlib
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert hash to normalized vector
        embedding = []
        for i in range(self.dimension):
            byte_val = hash_bytes[i % len(hash_bytes)]
            embedding.append((byte_val / 255.0) * 2 - 1)
        
        return embedding
    
    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self.dimension


class RAGRetrieval:
    """
    Retrieval-Augmented Generation retrieval engine.
    """
    
    def __init__(self):
        """Initialize RAG retrieval."""
        self.documents: Dict[str, List[Dict[str, Any]]] = {}
    
    async def index_document(
        self,
        doc_id: str,
        chunks: List[Dict[str, Any]],
        embeddings: List[List[float]]
    ) -> bool:
        """
        Index document chunks with embeddings.
        
        Args:
            doc_id: Document ID
            chunks: Text chunks
            embeddings: Chunk embeddings
            
        Returns:
            Success status
        """
        if len(chunks) != len(embeddings):
            return False
        
        indexed_chunks = []
        for chunk, embedding in zip(chunks, embeddings):
            indexed_chunks.append({
                "text": chunk["text"],
                "chunk_id": chunk["chunk_id"],
                "embedding": embedding,
                "metadata": chunk["metadata"]
            })
        
        self.documents[doc_id] = indexed_chunks
        return True
    
    async def retrieve(
        self,
        query_embedding: List[float],
        limit: int = 5,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks.
        
        Args:
            query_embedding: Query embedding
            limit: Max results
            threshold: Similarity threshold
            
        Returns:
            Retrieved chunks
        """
        results = []
        
        for doc_id, chunks in self.documents.items():
            for chunk in chunks:
                similarity = self._cosine_similarity(
                    query_embedding,
                    chunk["embedding"]
                )
                
                if similarity >= threshold:
                    results.append({
                        "text": chunk["text"],
                        "doc_id": doc_id,
                        "similarity": similarity,
                        "metadata": chunk["metadata"]
                    })
        
        # Sort by similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:limit]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity."""
        if not vec1 or not vec2:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a ** 2 for a in vec1) ** 0.5
        norm2 = sum(b ** 2 for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


# Global instances
_uploader: Optional[DocumentUploader] = None
_chunker: Optional[TextChunker] = None
_embedder: Optional[EmbeddingGenerator] = None
_retrieval: Optional[RAGRetrieval] = None


def get_uploader() -> DocumentUploader:
    """Get or create document uploader."""
    global _uploader
    if _uploader is None:
        _uploader = DocumentUploader()
    return _uploader


def get_chunker() -> TextChunker:
    """Get or create text chunker."""
    global _chunker
    if _chunker is None:
        _chunker = TextChunker()
    return _chunker


def get_embedder() -> EmbeddingGenerator:
    """Get or create embedding generator."""
    global _embedder
    if _embedder is None:
        _embedder = EmbeddingGenerator()
    return _embedder


def get_rag_retrieval() -> RAGRetrieval:
    """Get or create RAG retrieval."""
    global _retrieval
    if _retrieval is None:
        _retrieval = RAGRetrieval()
    return _retrieval
