"""Short-term memory management (session-based)."""

from typing import Any, Dict, List, Optional
from datetime import datetime
from collections import defaultdict
import json


class ShortTermMemory:
    """
    Session-based short-term memory.
    
    Stores:
    - Conversation history
    - Recent interactions
    - Current context
    - Temporary data
    """
    
    def __init__(self, max_messages: int = 100):
        """Initialize short-term memory."""
        self.memory: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.max_messages = max_messages
    
    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a message to session memory.
        
        Args:
            session_id: Session identifier
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        self.memory[session_id].append(message)
        
        # Trim if exceeds max
        if len(self.memory[session_id]) > self.max_messages:
            self.memory[session_id] = self.memory[session_id][-self.max_messages:]
    
    def get_history(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session identifier
            limit: Optional limit on number of messages
            
        Returns:
            List of messages
        """
        history = self.memory.get(session_id, [])
        
        if limit:
            return history[-limit:]
        
        return history
    
    def clear_session(self, session_id: str) -> None:
        """Clear all messages for a session."""
        if session_id in self.memory:
            del self.memory[session_id]
    
    def get_context(
        self,
        session_id: str,
        window_size: int = 10
    ) -> Dict[str, Any]:
        """
        Get conversation context window.
        
        Args:
            session_id: Session identifier
            window_size: Number of recent messages
            
        Returns:
            Context dictionary
        """
        history = self.get_history(session_id, limit=window_size)
        
        return {
            "session_id": session_id,
            "messages": history,
            "message_count": len(history),
            "created_at": history[0]["timestamp"] if history else None,
            "last_updated": history[-1]["timestamp"] if history else None
        }
    
    def summarize_session(self, session_id: str) -> Dict[str, Any]:
        """Get summary of session memory."""
        history = self.memory.get(session_id, [])
        
        return {
            "session_id": session_id,
            "total_messages": len(history),
            "roles": self._count_roles(history),
            "time_span": self._get_time_span(history)
        }
    
    def _count_roles(self, messages: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count messages by role."""
        counts = defaultdict(int)
        for msg in messages:
            counts[msg["role"]] += 1
        return dict(counts)
    
    def _get_time_span(self, messages: List[Dict[str, Any]]) -> Dict[str, str]:
        """Get time span of messages."""
        if not messages:
            return {"start": None, "end": None}
        
        return {
            "start": messages[0]["timestamp"],
            "end": messages[-1]["timestamp"]
        }


# Global short-term memory instance
_short_term_memory: Optional[ShortTermMemory] = None


def get_short_term_memory() -> ShortTermMemory:
    """Get or create global short-term memory."""
    global _short_term_memory
    if _short_term_memory is None:
        _short_term_memory = ShortTermMemory()
    return _short_term_memory
