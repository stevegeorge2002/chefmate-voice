"""
ChefMate Voice - Conversation Context Manager
Maintains conversation history and context across languages
"""

from datetime import datetime
from typing import Dict, List, Optional

class ConversationManager:
    """Manage kitchen conversations with context"""
    
    def __init__(self):
        self.conversations = []
        self.current_context = {}
        
    def add_message(self, speaker: str, message: str, language: str, intent: Dict = None):
        """Add message to conversation history"""
        
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "message": message,
            "language": language,
            "intent": intent,
            "context": dict(self.current_context)
        }
        
        self.conversations.append(conversation_entry)
        
        # Update context
        if intent:
            self._update_context(intent)
        
        return conversation_entry
    
    def _update_context(self, intent: Dict):
        """Update conversation context from intent"""
        
        # Remember last mentioned table
        if "table_number" in intent and intent["table_number"]:
            self.current_context["last_table"] = intent["table_number"]
        
        # Remember last mentioned dish
        if "items" in intent and intent["items"]:
            self.current_context["last_dish"] = intent["items"][0].get("dish")
            self.current_context["last_order_items"] = intent["items"]
        
        # Remember action
        if "action" in intent:
            self.current_context["last_action"] = intent["action"]
    
    def resolve_context(self, message: str, parsed_intent: Dict) -> Dict:
        """Resolve pronouns and context references"""
        
        message_lower = message.lower()
        
        # Handle "that" or "it" references
        if ("that" in message_lower or "it" in message_lower) and not parsed_intent.get("table_number"):
            # Use last mentioned table
            if "last_table" in self.current_context:
                parsed_intent["table_number"] = self.current_context["last_table"]
        
        # Handle implicit dish references
        if not parsed_intent.get("items") and "ready" in message_lower:
            # "Is it ready?" → referring to last dish
            if "last_order_items" in self.current_context:
                parsed_intent["items"] = self.current_context["last_order_items"]
        
        return parsed_intent
    
    def get_recent_conversation(self, count: int = 5) -> List[Dict]:
        """Get recent conversation messages"""
        return self.conversations[-count:] if self.conversations else []
    
    def get_conversation_summary(self) -> str:
        """Generate summary of current kitchen state from conversation"""
        
        summary_parts = []
        
        if "last_table" in self.current_context:
            summary_parts.append(f"Last mentioned: Table {self.current_context['last_table']}")
        
        if "last_action" in self.current_context:
            summary_parts.append(f"Last action: {self.current_context['last_action']}")
        
        summary_parts.append(f"Total messages: {len(self.conversations)}")
        
        return " | ".join(summary_parts)