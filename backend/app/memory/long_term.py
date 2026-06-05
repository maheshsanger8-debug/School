"""Long-term memory management (database-based)."""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta


class LongTermMemory:
    """
    Long-term memory using persistent storage.
    
    Stores:
    - Execution history
    - Learned facts
    - User preferences
    - Analysis results
    """
    
    def __init__(self):
        """Initialize long-term memory."""
        # This is a placeholder - real implementation would use database
        self.memory: Dict[str, Any] = {}
    
    def save(
        self,
        key: str,
        value: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Save data to long-term memory.
        
        Args:
            key: Unique key
            value: Data to save
            metadata: Optional metadata
        """
        self.memory[key] = {
            "value": value,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
    
    def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve data from long-term memory.
        
        Args:
            key: Key to retrieve
            
        Returns:
            Stored value or None
        """
        if key in self.memory:
            return self.memory[key]["value"]
        return None
    
    def search(
        self,
        pattern: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search memory by key pattern.
        
        Args:
            pattern: Search pattern
            limit: Max results
            
        Returns:
            List of matching entries
        """
        results = []
        for key, value in self.memory.items():
            if pattern.lower() in key.lower():
                results.append({
                    "key": key,
                    "value": value["value"],
                    "timestamp": value["timestamp"]
                })
                if len(results) >= limit:
                    break
        
        return results
    
    def delete(self, key: str) -> bool:
        """
        Delete entry from memory.
        
        Args:
            key: Key to delete
            
        Returns:
            True if deleted, False if not found
        """
        if key in self.memory:
            del self.memory[key]
            return True
        return False
    
    def cleanup_old(self, days: int = 30) -> int:
        """
        Remove entries older than specified days.
        
        Args:
            days: Age threshold
            
        Returns:
            Number of entries deleted
        """
        threshold = datetime.utcnow() - timedelta(days=days)
        keys_to_delete = []
        
        for key, value in self.memory.items():
            timestamp = datetime.fromisoformat(value["timestamp"])
            if timestamp < threshold:
                keys_to_delete.append(key)
        
        for key in keys_to_delete:
            del self.memory[key]
        
        return len(keys_to_delete)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            "total_entries": len(self.memory),
            "keys": list(self.memory.keys()),
            "memory_size_estimate": sum(
                len(str(v["value"])) for v in self.memory.values()
            )
        }


# Global long-term memory instance
_long_term_memory: Optional[LongTermMemory] = None


def get_long_term_memory() -> LongTermMemory:
    """Get or create global long-term memory."""
    global _long_term_memory
    if _long_term_memory is None:
        _long_term_memory = LongTermMemory()
    return _long_term_memory
