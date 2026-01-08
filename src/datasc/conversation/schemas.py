from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ConversationInput(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ConversationOutput(BaseModel):
    response: str
    conversation_id: str
    metadata: Optional[Dict[str, Any]] = None
