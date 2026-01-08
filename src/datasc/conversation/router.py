from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from .schemas import ConversationInput, ConversationOutput
from .graph import graph

router = APIRouter(prefix="/conversation", tags=["conversation"])

@router.post("/chat", response_model=ConversationOutput)
async def chat(input_data: ConversationInput):
    try:
        # Create initial state with user message
        initial_state = {"messages": [HumanMessage(content=input_data.message)]}
        
        # Invoke the graph
        # For a simple stateless run (no thread_id persistence yet), we just invoke it.
        # If persistence is needed, we would use a checkpointer and configure it here.
        result = graph.invoke(initial_state)
        
        # Extract the last message content
        last_message = result["messages"][-1]
        response_text = last_message.content
        
        return ConversationOutput(
            response=response_text,
            conversation_id=input_data.conversation_id or "default",
            metadata={"status": "success"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
