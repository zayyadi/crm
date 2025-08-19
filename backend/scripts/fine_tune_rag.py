#!/usr/bin/env python3
"""
Script to fine-tune the RAG model with CRM data and chat logs
"""

import os
import sys
import asyncio
import json
from datetime import datetime
from typing import List, Dict, Any
import logging

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.rag_service import rag_service
from app.services.gemini_service import gemini_service
from app.models.models import Customer, Invoice, Payment, Subscription
from app.core.database import db
from sqlalchemy.future import select

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGFineTuner:
    def __init__(self):
        self.rag_service = rag_service
        self.gemini_service = gemini_service
    
    async def collect_crm_data(self) -> List[Dict[str, Any]]:
        """Collect CRM data to add to the knowledge base"""
        try:
            crm_data = []
            
            # Collect customers
            customer_query = select(Customer)
            customer_result = await db.execute(customer_query)
            customers = customer_result.scalars().all()
            
            for customer in customers:
                crm_data.append({
                    "type": "customer",
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "phone": customer.phone,
                    "address": customer.address
                })
            
            # Collect invoices
            invoice_query = select(Invoice)
            invoice_result = await db.execute(invoice_query)
            invoices = invoice_result.scalars().all()
            
            for invoice in invoices:
                crm_data.append({
                    "type": "invoice",
                    "id": invoice.id,
                    "customer_id": invoice.customer_id,
                    "amount": invoice.amount,
                    "currency": invoice.currency,
                    "status": invoice.status,
                    "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
                    "issued_date": invoice.issued_date.isoformat() if invoice.issued_date else None,
                    "description": invoice.description
                })
            
            # Collect payments
            payment_query = select(Payment)
            payment_result = await db.execute(payment_query)
            payments = payment_result.scalars().all()
            
            for payment in payments:
                crm_data.append({
                    "type": "payment",
                    "id": payment.id,
                    "invoice_id": payment.invoice_id,
                    "amount": payment.amount,
                    "currency": payment.currency,
                    "payment_method": payment.payment_method,
                    "status": payment.status,
                    "transaction_id": payment.transaction_id,
                    "payment_date": payment.payment_date.isoformat() if payment.payment_date else None
                })
            
            # Collect subscriptions
            subscription_query = select(Subscription)
            subscription_result = await db.execute(subscription_query)
            subscriptions = subscription_result.scalars().all()
            
            for subscription in subscriptions:
                crm_data.append({
                    "type": "subscription",
                    "id": subscription.id,
                    "customer_id": subscription.customer_id,
                    "plan_name": subscription.plan_name,
                    "amount": subscription.amount,
                    "currency": subscription.currency,
                    "status": subscription.status,
                    "start_date": subscription.start_date.isoformat() if subscription.start_date else None,
                    "end_date": subscription.end_date.isoformat() if subscription.end_date else None,
                    "billing_cycle": subscription.billing_cycle
                })
            
            logger.info(f"Collected {len(crm_data)} CRM data items")
            return crm_data
        except Exception as e:
            logger.error(f"Error collecting CRM data: {str(e)}")
            return []
    
    async def collect_chat_logs(self, log_file_path: str) -> List[Dict[str, Any]]:
        """Collect chat logs for training"""
        try:
            if not os.path.exists(log_file_path):
                logger.warning(f"Chat log file not found: {log_file_path}")
                return []
            
            with open(log_file_path, 'r') as f:
                chat_logs = json.load(f)
            
            logger.info(f"Collected {len(chat_logs)} chat log entries")
            return chat_logs
        except Exception as e:
            logger.error(f"Error collecting chat logs: {str(e)}")
            return []
    
    async def generate_training_data(self, crm_data: List[Dict[str, Any]], chat_logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate training data for fine-tuning"""
        try:
            training_data = []
            
            # Add CRM data as training examples
            for item in crm_data:
                if item["type"] == "customer":
                    training_data.append({
                        "input": f"What is the contact information for customer {item['name']}?",
                        "output": f"Customer {item['name']} can be reached at email: {item['email']}, phone: {item['phone']}, address: {item['address']}"
                    })
                elif item["type"] == "invoice":
                    training_data.append({
                        "input": f"What is the status of invoice {item['id']}?",
                        "output": f"Invoice {item['id']} for {item['amount']/100:.2f} {item['currency']} is currently {item['status']}. It was issued on {item['issued_date']} and is due on {item['due_date']}."
                    })
                elif item["type"] == "payment":
                    training_data.append({
                        "input": f"What is the payment status for payment {item['id']}?",
                        "output": f"Payment {item['id']} for {item['amount']/100:.2f} {item['currency']} via {item['payment_method']} is {item['status']}. Transaction ID: {item['transaction_id']}."
                    })
                elif item["type"] == "subscription":
                    training_data.append({
                        "input": f"What is the subscription status for {item['plan_name']}?",
                        "output": f"Subscription {item['id']} for {item['plan_name']} is {item['status']}. It costs {item['amount']/100:.2f} {item['currency']} per {item['billing_cycle']}. Started on {item['start_date']} and ends on {item['end_date']}."
                    })
            
            # Add chat logs as training examples
            for log in chat_logs:
                training_data.append({
                    "input": log.get("user_message", ""),
                    "output": log.get("ai_response", "")
                })
            
            logger.info(f"Generated {len(training_data)} training examples")
            return training_data
        except Exception as e:
            logger.error(f"Error generating training data: {str(e)}")
            return []
    
    async def update_knowledge_base(self, crm_data: List[Dict[str, Any]]):
        """Update the RAG knowledge base with CRM data"""
        try:
            self.rag_service.add_crm_data(crm_data)
            logger.info("Knowledge base updated successfully")
        except Exception as e:
            logger.error(f"Error updating knowledge base: {str(e)}")
    
    async def evaluate_model(self, test_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate the model performance"""
        try:
            correct_responses = 0
            total_responses = len(test_data)
            
            for item in test_data:
                # Generate response using the model
                response = await self.gemini_service.generate_response(
                    item["input"], 
                    item.get("customer_id")
                )
                
                # Simple keyword matching for evaluation
                # In a real scenario, you would use more sophisticated evaluation metrics
                if item["expected_keywords"] in response.lower():
                    correct_responses += 1
            
            accuracy = correct_responses / total_responses if total_responses > 0 else 0
            
            evaluation_result = {
                "accuracy": accuracy,
                "correct_responses": correct_responses,
                "total_responses": total_responses
            }
            
            logger.info(f"Model evaluation completed. Accuracy: {accuracy:.2%}")
            return evaluation_result
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            return {"accuracy": 0, "correct_responses": 0, "total_responses": 0}
    
    async def run_fine_tuning(self, chat_log_path: str = "chat_logs.json"):
        """Run the complete fine-tuning workflow"""
        try:
            logger.info("Starting RAG fine-tuning process...")
            
            # 1. Collect CRM data
            logger.info("Collecting CRM data...")
            crm_data = await self.collect_crm_data()
            
            # 2. Collect chat logs
            logger.info("Collecting chat logs...")
            chat_logs = await self.collect_chat_logs(chat_log_path)
            
            # 3. Generate training data
            logger.info("Generating training data...")
            training_data = await self.generate_training_data(crm_data, chat_logs)
            
            # 4. Update knowledge base
            logger.info("Updating knowledge base...")
            await self.update_knowledge_base(crm_data)
            
            # 5. For demonstration, we'll save training data to a file
            # In a real scenario, you would use this data to fine-tune the model
            with open("training_data.json", "w") as f:
                json.dump(training_data, f, indent=2)
            
            logger.info("Fine-tuning process completed successfully!")
            logger.info(f"Generated {len(training_data)} training examples")
            
            return training_data
        except Exception as e:
            logger.error(f"Error in fine-tuning process: {str(e)}")
            raise

# Main execution
async def main():
    # Initialize the fine-tuner
    fine_tuner = RAGFineTuner()
    
    # Run the fine-tuning process
    try:
        training_data = await fine_tuner.run_fine_tuning()
        print(f"Fine-tuning completed successfully! Generated {len(training_data)} training examples.")
        print("Training data saved to 'training_data.json'")
    except Exception as e:
        print(f"Fine-tuning failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Initialize database
    db.init()
    
    # Run the async main function
    asyncio.run(main())
