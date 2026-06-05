"""Tests for memory systems."""

import pytest
from app.memory.short_term import ShortTermMemory, get_short_term_memory
from app.memory.long_term import LongTermMemory, get_long_term_memory
from app.memory.vector_store import VectorStore, get_vector_store
from app.memory.semantic_search import SemanticSearch, get_semantic_search


# Short-term Memory Tests
def test_short_term_memory_add_message():
    """Test adding message to short-term memory."""
    memory = ShortTermMemory()
    memory.add_message("session-1", "user", "Hello")
    
    history = memory.get_history("session-1")
    assert len(history) == 1
    assert history[0]["content"] == "Hello"


def test_short_term_memory_history():
    """Test getting conversation history."""
    memory = ShortTermMemory()
    
    for i in range(5):
        memory.add_message("session-1", "user", f"Message {i}")
    
    history = memory.get_history("session-1")
    assert len(history) == 5


def test_short_term_memory_limit():
    """Test max message limit."""
    memory = ShortTermMemory(max_messages=3)
    
    for i in range(5):
        memory.add_message("session-1", "user", f"Message {i}")
    
    history = memory.get_history("session-1")
    assert len(history) == 3


def test_short_term_memory_clear():
    """Test clearing session."""
    memory = ShortTermMemory()
    memory.add_message("session-1", "user", "Hello")
    memory.clear_session("session-1")
    
    history = memory.get_history("session-1")
    assert len(history) == 0


# Long-term Memory Tests
def test_long_term_memory_save_retrieve():
    """Test saving and retrieving from long-term memory."""
    memory = LongTermMemory()
    memory.save("key-1", {"data": "value"})
    
    value = memory.retrieve("key-1")
    assert value["data"] == "value"


def test_long_term_memory_search():
    """Test searching long-term memory."""
    memory = LongTermMemory()
    memory.save("user-profile-1", {"name": "Alice"})
    memory.save("user-profile-2", {"name": "Bob"})
    
    results = memory.search("user-profile", limit=10)
    assert len(results) == 2


def test_long_term_memory_delete():
    """Test deleting from long-term memory."""
    memory = LongTermMemory()
    memory.save("key-1", "value")
    
    deleted = memory.delete("key-1")
    assert deleted is True
    
    value = memory.retrieve("key-1")
    assert value is None


# Vector Store Tests
def test_vector_store_add_vector():
    """Test adding vector to store."""
    store = VectorStore(dimension=384)
    embedding = [0.1] * 384
    
    vector_id = store.add("test text", embedding)
    assert vector_id is not None


def test_vector_store_search():
    """Test searching vector store."""
    store = VectorStore(dimension=384)
    embedding1 = [0.1] * 384
    embedding2 = [0.9] * 384
    
    store.add("similar text 1", embedding1)
    store.add("different text", embedding2)
    
    query = [0.1] * 384
    results = store.search(query, limit=5, threshold=0.5)
    
    assert len(results) > 0


def test_vector_store_dimension_validation():
    """Test dimension validation."""
    store = VectorStore(dimension=384)
    
    with pytest.raises(ValueError):
        store.add("test", [0.1] * 100)  # Wrong dimension


# Semantic Search Tests
def test_semantic_search_index():
    """Test indexing with semantic search."""
    search = SemanticSearch()
    embedding = [0.1] * 384
    
    doc_id = search.index("test document", embedding)
    assert doc_id is not None


def test_semantic_search_search():
    """Test semantic search."""
    search = SemanticSearch()
    embedding = [0.1] * 384
    
    search.index("test document", embedding)
    
    query = [0.1] * 384
    results = search.search(query, limit=5)
    
    assert len(results) > 0
