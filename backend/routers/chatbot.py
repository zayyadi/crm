from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
import uuid
from datetime import datetime, timezone
from app.schemas.schemas import (
    ChatMessage, ChatResponse, ChatSessionCreate, 
    ChatSessionRead, ChatSession
)
# from app.models.models import User
from routers.users import get_current_active_user
from app.services.gemini_service import gemini_service
# from app.services.rag_service import rag_service

router = APIRouter()

# In-memory storage for chat sessions (in production, you would use a database)
chat_sessions = {}

@router.post("/sessions/", response_model=ChatSessionRead, status_code=status.HTTP_201_CREATED)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user = Depends(get_current_active_user)
):
    """Create a new chat session"""
    try:
        session_id = str(uuid.uuid4())
        new_session = ChatSession(
            session_id=session_id,
            customer_id=session_data.customer_id,
            messages=[]
        )
        
        # Store session in memory (in production, store in database)
        chat_sessions[session_id] = {
            "id": session_id,
            "customer_id": session_data.customer_id,
            "messages": [],
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        return ChatSessionRead(
            id=session_id,
            session_id=session_id,
            customer_id=session_data.customer_id,
            messages=[],
            created_at=chat_sessions[session_id]["created_at"],
            updated_at=chat_sessions[session_id]["updated_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/sessions/{session_id}", response_model=ChatSessionRead)
async def get_chat_session(
    session_id: str,
    current_user = Depends(get_current_active_user)
):
    """Get a chat session by ID"""
    try:
        if session_id not in chat_sessions:
            raise HTTPException(status_code=404, detail="Chat session not found")
            
        session = chat_sessions[session_id]
        return ChatSessionRead(
            id=session_id,
            session_id=session_id,
            customer_id=session["customer_id"],
            messages=[ChatMessage(**msg) for msg in session["messages"]],
            created_at=session["created_at"],
            updated_at=session["updated_at"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sessions/{session_id}/messages", response_model=ChatResponse)
async def send_message(
    session_id: str,
    message: ChatMessage,
    current_user = Depends(get_current_active_user)
):
    """Send a message to the chatbot and get a response"""
    try:
        if session_id not in chat_sessions:
            raise HTTPException(status_code=404, detail="Chat session not found")
            
        # Add user message to session
        chat_sessions[session_id]["messages"].append({
            "message": message.message,
            "sender": message.sender
        })
        
        # Get customer ID from session if available
        customer_id = chat_sessions[session_id].get("customer_id")
        
        # Generate AI response using Gemini
        ai_response = await generate_ai_response(message.message, customer_id)
        
        # Add AI response to session
        chat_sessions[session_id]["messages"].append({
            "message": ai_response,
            "sender": "bot"
        })
        
        # Update session timestamp
        chat_sessions[session_id]["updated_at"] = datetime.now(timezone.utc)
        
        # Generate suggestions based on context
        suggestions = generate_suggestions(message.message, chat_sessions[session_id]["messages"])
        
        return ChatResponse(
            response=ai_response,
            suggestions=suggestions
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat_session(
    session_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a chat session"""
    try:
        if session_id not in chat_sessions:
            raise HTTPException(status_code=404, detail="Chat session not found")
            
        del chat_sessions[session_id]
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def generate_ai_response(user_message: str, customer_id: str = None) -> str:
    """
    Generate an AI response using Gemini AI with RAG capabilities.
    """
    try:
        # First, search for relevant documents in our knowledge base
        # relevant_docs = rag_service.search_relevant_documents(user_message, n_results=3)
        
        # Prepare context from relevant documents
        # context = "\n".join([doc["content"] for doc in relevant_docs])
        
        # Generate response using Gemini with context
        response = await gemini_service.generate_response(user_message, customer_id)
        
        return response
    except Exception as e:
        # Fallback to rule-based responses if AI fails
        user_message_lower = user_message.lower()
        
        if "hello" in user_message_lower or "hi" in user_message_lower:
            return "Hello! How can I help you today?"
        elif "invoice" in user_message_lower:
            return "I can help you with invoices. You can ask me to create a new invoice, check invoice status, or view payment history. What would you like to do?"
        elif "payment" in user_message_lower:
            return "Regarding payments, I can help you process payments, check payment status, or provide payment history. What do you need help with?"
        elif "subscription" in user_message_lower or "billing" in user_message_lower:
            return "I can assist with subscriptions and billing. You can ask about your current subscription, upgrade or downgrade plans, or check billing history."
        elif "contact" in user_message_lower:
            return "If you need to contact support, you can reach us at support@company.com or call us at +1-800-123-4567. Our support hours are Monday-Friday, 9AM-5PM EST."
        elif "thank" in user_message_lower:
            return "You're welcome! Is there anything else I can help you with?"
        elif "bye" in user_message_lower or "goodbye" in user_message_lower:
            return "Goodbye! Feel free to come back if you have any more questions."
        else:
            return "I'm currently experiencing technical difficulties with my AI capabilities. I'm an AI assistant for our CRM system. I can help with invoices, payments, subscriptions, and general customer support. Could you please provide more details about what you need help with?"

def generate_suggestions(user_message: str, conversation_history: list) -> list:
    """
    Generate contextual suggestions based on the user message and conversation history.
    """
    suggestions = []
    
    # Basic suggestions based on common CRM functions
    suggestions.append("How do I create a new invoice?")
    suggestions.append("What's my current subscription plan?")
    suggestions.append("How can I process a payment?")
    
    # Contextual suggestions based on keywords
    if "invoice" in user_message.lower():
        suggestions.append("Check invoice status")
        suggestions.append("View invoice history")
    elif "payment" in user_message.lower():
        suggestions.append("Process a payment")
        suggestions.append("Check payment status")
    elif "subscription" in user_message.lower():
        suggestions.append("Upgrade my plan")
        suggestions.append("Cancel subscription")
    
    # Return top 3 suggestions
    return suggestions[:3]

@router.get("/sessions/", response_model=List[ChatSessionRead])
async def get_all_chat_sessions(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
):
    """Get all chat sessions (with pagination)"""
    try:
        sessions = []
        session_ids = list(chat_sessions.keys())[skip:skip+limit]
        
        for session_id in session_ids:
            session = chat_sessions[session_id]
            sessions.append(ChatSessionRead(
                id=session_id,
                session_id=session_id,
                customer_id=session["customer_id"],
                messages=[ChatMessage(**msg) for msg in session["messages"]],
                created_at=session["created_at"],
                updated_at=session["updated_at"]
            ))
            
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
