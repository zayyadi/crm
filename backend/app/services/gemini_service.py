import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from app.models.models import User, Customer, Invoice, Payment, Subscription
from app.core.database import db
from sqlalchemy.future import select
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        
        
        
        
    async def get_customer_context(self, customer_id: str) -> Dict[str, Any]:
        """Retrieve customer context for the AI"""
        try:
            
            customer_query = select(Customer).where(Customer.id == customer_id)
            customer_result = await db.execute(customer_query)
            customer = customer_result.scalar_one_or_none()
            
            if not customer:
                return {}
            
            context = {
                "customer": {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "phone": customer.phone,
                    "address": customer.address
                }
            }
            
            
            invoice_query = select(Invoice).where(Invoice.customer_id == customer_id)
            invoice_result = await db.execute(invoice_query)
            invoices = invoice_result.scalars().all()
            
            context["invoices"] = [
                {
                    "id": inv.id,
                    "amount": inv.amount,
                    "currency": inv.currency,
                    "status": inv.status,
                    "due_date": inv.due_date.isoformat() if inv.due_date else None,
                    "issued_date": inv.issued_date.isoformat() if inv.issued_date else None,
                    "description": inv.description
                }
                for inv in invoices
            ]
            
            
            payment_query = select(Payment).where(Payment.invoice_id.in_([inv.id for inv in invoices]))
            payment_result = await db.execute(payment_query)
            payments = payment_result.scalars().all()
            
            context["payments"] = [
                {
                    "id": pay.id,
                    "invoice_id": pay.invoice_id,
                    "amount": pay.amount,
                    "currency": pay.currency,
                    "payment_method": pay.payment_method,
                    "status": pay.status,
                    "transaction_id": pay.transaction_id,
                    "payment_date": pay.payment_date.isoformat() if pay.payment_date else None
                }
                for pay in payments
            ]
            
            
            subscription_query = select(Subscription).where(Subscription.customer_id == customer_id)
            subscription_result = await db.execute(subscription_query)
            subscriptions = subscription_result.scalars().all()
            
            context["subscriptions"] = [
                {
                    "id": sub.id,
                    "plan_name": sub.plan_name,
                    "amount": sub.amount,
                    "currency": sub.currency,
                    "status": sub.status,
                    "start_date": sub.start_date.isoformat() if sub.start_date else None,
                    "end_date": sub.end_date.isoformat() if sub.end_date else None,
                    "billing_cycle": sub.billing_cycle
                }
                for sub in subscriptions
            ]
            
            return context
        except Exception as e:
            logger.error(f"Error retrieving customer context: {str(e)}")
            return {}
    
    async def generate_response(self, user_message: str, customer_id: Optional[str] = None) -> str:
        """Generate an AI response using Gemini"""
        try:
            
            context_parts = []
            
            
            if customer_id:
                customer_context = await self.get_customer_context(customer_id)
                if customer_context:
                    context_parts.append(f"Customer Context: {customer_context}")
            
            
            system_instructions = """
            You are an AI assistant for a CRM (Customer Relationship Management) system. 
            You help customers with inquiries about their accounts, invoices, payments, and subscriptions.
            
            When responding:
            1. Be professional and helpful
            2. If you don't have specific information, acknowledge that and suggest contacting support
            3. Never share sensitive information like passwords or payment details
            4. If asked about topics outside your knowledge, politely explain your limitations
            5. Use the provided context to give accurate, personalized responses
            """
            
            
            prompt_parts = [system_instructions]
            if context_parts:
                prompt_parts.extend(context_parts)
            prompt_parts.append(f"User Message: {user_message}")
            
            prompt = "\n\n".join(prompt_parts)
            
            
            response = await self.model.generate_content_async(prompt)
            
            
            if response.text:
                return response.text.strip()
            else:
                return "I apologize, but I couldn't generate a response at the moment. Please try again later."
                
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            return "I'm sorry, but I encountered an error while processing your request. Please try again later."


gemini_service = GeminiService()
