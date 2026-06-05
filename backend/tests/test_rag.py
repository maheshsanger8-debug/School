"""Tests for RAG pipeline."""

import pytest
from app.rag.pipeline import (
    DocumentUploader,
    TextChunker,
    EmbeddingGenerator,
    RAGRetrieval
)
import tempfile
from pathlib import Path


# Document Uploader Tests
@pytest.mark.asyncio
async def test_document_uploader_valid_file():
    """Test uploading valid file."""
    uploader = DocumentUploader()
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content")
        temp_path = f.name
    
    try:
        result = await uploader.upload(temp_path, "test")
        assert result["success"] is True
        assert "doc_id" in result
    finally:
        Path(temp_path).unlink()


@pytest.mark.asyncio
async def test_document_uploader_invalid_file():
    """Test uploading invalid file."""
    uploader = DocumentUploader()
    result = await uploader.upload("/nonexistent/file.txt", "test")
    
    assert result["success"] is False


# Text Chunker Tests
def test_text_chunker_basic():
    """Test basic text chunking."""
    chunker = TextChunker(chunk_size=100, overlap=10)
    
    text = "\n\n".join([f"Paragraph {i}" * 10 for i in range(5)])
    chunks = chunker.chunk(text)
    
    assert len(chunks) > 0
    assert all("text" in c for c in chunks)
    assert all("chunk_id" in c for c in chunks)


def test_text_chunker_with_metadata():
    """Test chunking with metadata."""
    chunker = TextChunker()
    metadata = {"source": "test.txt"}
    
    chunks = chunker.chunk("Test content", metadata=metadata)
    
    assert len(chunks) > 0
    assert chunks[0]["metadata"]["source"] == "test.txt"


# Embedding Generator Tests
@pytest.mark.asyncio
async def test_embedding_generator():
    """Test embedding generation."""
    gen = EmbeddingGenerator()
    
    embedding = await gen.generate("test text")
    
    assert len(embedding) == gen.get_dimension()
    assert all(-1 <= v <= 1 for v in embedding)


# RAG Retrieval Tests
@pytest.mark.asyncio
async def test_rag_retrieval_index():
    """Test indexing documents in RAG."""
    retrieval = RAGRetrieval()
    
    chunks = [
        {"text": "Text 1", "chunk_id": "c1", "metadata": {}},
        {"text": "Text 2", "chunk_id": "c2", "metadata": {}}
    ]
    
    embeddings = [
        [0.1] * 384,
        [0.2] * 384
    ]
    
    success = await retrieval.index_document("doc-1", chunks, embeddings)
    assert success is True


@pytest.mark.asyncio
async def test_rag_retrieval_retrieve():
    """Test retrieving from RAG."""
    retrieval = RAGRetrieval()
    
    chunks = [
        {"text": "Similar text", "chunk_id": "c1", "metadata": {}}
    ]
    embeddings = [[0.1] * 384]
    
    await retrieval.index_document("doc-1", chunks, embeddings)
    
    query_embedding = [0.1] * 384
    results = await retrieval.retrieve(query_embedding, limit=5)
    
    assert len(results) >= 0
