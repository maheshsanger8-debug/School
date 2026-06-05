"""Inter-agent communication and message passing."""

from typing import Any, Dict, Optional, List, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """Message type enumeration."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    QUERY = "query"
    RESULT = "result"
    ERROR = "error"


@dataclass
class Message:
    """Inter-agent message."""
    message_id: str
    sender_id: str
    recipient_id: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime
    priority: int = 1
    requires_response: bool = False
    response_to: Optional[str] = None


class MessageBroker:
    """
    Message broker for inter-agent communication.
    """
    
    def __init__(self):
        """Initialize message broker."""
        self.messages: Dict[str, Message] = {}
        self.message_counter = 0
        self.handlers: Dict[str, List[Callable]] = {}
        self.message_history: List[Message] = []
    
    async def send_message(
        self,
        sender_id: str,
        recipient_id: str,
        message_type: MessageType,
        content: Dict[str, Any],
        priority: int = 1,
        requires_response: bool = False
    ) -> str:
        """
        Send message from one agent to another.
        
        Args:
            sender_id: Sender agent ID
            recipient_id: Recipient agent ID
            message_type: Message type
            content: Message content
            priority: Message priority
            requires_response: Whether response is needed
            
        Returns:
            Message ID
        """
        self.message_counter += 1
        message_id = f"msg-{self.message_counter}"
        
        message = Message(
            message_id=message_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            content=content,
            timestamp=datetime.utcnow(),
            priority=priority,
            requires_response=requires_response
        )
        
        self.messages[message_id] = message
        self.message_history.append(message)
        
        # Trigger handlers
        await self._trigger_handlers(recipient_id, message)
        
        logger.info(
            f"Message {message_id}: {sender_id} -> {recipient_id} "
            f"({message_type.value})"
        )
        
        return message_id
    
    async def send_response(
        self,
        original_message_id: str,
        sender_id: str,
        response_content: Dict[str, Any]
    ) -> str:
        """
        Send response to a message.
        
        Args:
            original_message_id: ID of message being responded to
            sender_id: Sender (responder) ID
            response_content: Response content
            
        Returns:
            Response message ID
        """
        original_msg = self.messages.get(original_message_id)
        if not original_msg:
            raise ValueError(f"Message {original_message_id} not found")
        
        response_id = await self.send_message(
            sender_id=sender_id,
            recipient_id=original_msg.sender_id,
            message_type=MessageType.RESPONSE,
            content=response_content,
            priority=original_msg.priority,
            requires_response=False
        )
        
        self.messages[response_id].response_to = original_message_id
        return response_id
    
    def register_handler(
        self,
        agent_id: str,
        handler: Callable
    ) -> None:
        """
        Register message handler for agent.
        
        Args:
            agent_id: Agent ID
            handler: Callable handler function
        """
        if agent_id not in self.handlers:
            self.handlers[agent_id] = []
        self.handlers[agent_id].append(handler)
    
    async def _trigger_handlers(self, agent_id: str, message: Message) -> None:
        """Trigger registered handlers for agent."""
        if agent_id in self.handlers:
            for handler in self.handlers[agent_id]:
                try:
                    await handler(message) if callable(handler) else None
                except Exception as e:
                    logger.error(f"Handler error for {agent_id}: {str(e)}")
    
    def get_message(self, message_id: str) -> Optional[Message]:
        """Get message by ID."""
        return self.messages.get(message_id)
    
    def get_agent_messages(
        self,
        agent_id: str,
        direction: str = "received"
    ) -> List[Message]:
        """
        Get messages for agent.
        
        Args:
            agent_id: Agent ID
            direction: "sent" or "received"
            
        Returns:
            List of messages
        """
        if direction == "sent":
            return [m for m in self.message_history if m.sender_id == agent_id]
        else:
            return [m for m in self.message_history if m.recipient_id == agent_id]
    
    def get_broker_stats(self) -> Dict[str, Any]:
        """Get broker statistics."""
        return {
            "total_messages": len(self.messages),
            "message_types": self._count_by_type(),
            "active_agents": len(self.handlers)
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """Count messages by type."""
        counts = {}
        for msg in self.message_history:
            msg_type = msg.message_type.value
            counts[msg_type] = counts.get(msg_type, 0) + 1
        return counts


# Global message broker instance
_broker: Optional[MessageBroker] = None


def get_message_broker() -> MessageBroker:
    """Get or create message broker."""
    global _broker
    if _broker is None:
        _broker = MessageBroker()
    return _broker
