# import os
# import chromadb
# from chromadb.config import Settings
# from sentence_transformers import SentenceTransformer
# from typing import List, Dict, Any, Optional
# import uuid
# import json
# from datetime import datetime
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class RAGService:
#     def __init__(self):
#         # Initialize the embedding model
#         self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
#         # Initialize ChromaDB client
#         self.chroma_client = chromadb.Client(Settings(
#             persist_directory="./chroma_db",
#             is_persistent=True
#         ))
        
#         # Get or create the collection
#         self.collection = self.chroma_client.get_or_create_collection(
#             name="crm_knowledge_base"
#         )
        
#         # Initialize with some base knowledge
#         self._initialize_knowledge_base()
    
#     def _initialize_knowledge_base(self):
#         """Initialize the knowledge base with common CRM information"""
#         base_knowledge = [
#             {
#                 "id": "kb_001",
#                 "content": "Invoices are documents that request payment for goods or services provided. They include details like amount, due date, and payment instructions.",
#                 "metadata": {
#                     "category": "billing",
#                     "type": "definition"
#                 }
#             },
#             {
#                 "id": "kb_002",
#                 "content": "Payments can be made using various methods including credit card, bank transfer, or PayPal. Payment status can be pending, completed, or failed.",
#                 "metadata": {
#                     "category": "billing",
#                     "type": "definition"
#                 }
#             },
#             {
#                 "id": "kb_003",
#                 "content": "Subscriptions are recurring billing arrangements where customers pay regularly for ongoing services. Subscriptions can be monthly or yearly.",
#                 "metadata": {
#                     "category": "billing",
#                     "type": "definition"
#                 }
#             },
#             {
#                 "id": "kb_004",
#                 "content": "To create an invoice, navigate to the billing section and select 'Create Invoice'. Fill in the customer details, amount, and due date.",
#                 "metadata": {
#                     "category": "how-to",
#                     "type": "instruction"
#                 }
#             },
#             {
#                 "id": "kb_005",
#                 "content": "To check your payment history, go to the billing section and view your payment records. You can filter by date range or payment status.",
#                 "metadata": {
#                     "category": "how-to",
#                     "type": "instruction"
#                 }
#             },
#             {
#                 "id": "kb_006",
#                 "content": "If you need to cancel a subscription, go to the billing section, find your subscription, and select the cancel option. Note that cancellations may take effect at the end of the current billing period.",
#                 "metadata": {
#                     "category": "how-to",
#                     "type": "instruction"
#                 }
#             },
#             {
#                 "id": "kb_007",
#                 "content": "For billing inquiries, contact our support team at billing@company.com or call +1-800-BILLING. Our billing hours are Monday-Friday, 9AM-6PM EST.",
#                 "metadata": {
#                     "category": "support",
#                     "type": "contact"
#                 }
#             },
#             {
#                 "id": "kb_008",
#                 "content": "Late payments may result in service interruption or additional fees. We recommend setting up automatic payments to avoid any disruptions.",
#                 "metadata": {
#                     "category": "policy",
#                     "type": "information"
#                 }
#             }
#         ]
        
#         # Add base knowledge to the collection if it's empty
#         if self.collection.count() == 0:
#             self.add_documents(base_knowledge)
    
#     def add_documents(self, documents: List[Dict[str, Any]]):
#         """Add documents to the knowledge base"""
#         try:
#             ids = []
#             contents = []
#             metadatas = []
            
#             for doc in documents:
#                 ids.append(doc["id"])
#                 contents.append(doc["content"])
#                 metadatas.append(doc.get("metadata", {}))
            
#             self.collection.add(
#                 ids=ids,
#                 documents=contents,
#                 metadatas=metadatas
#             )
            
#             logger.info(f"Added {len(documents)} documents to knowledge base")
#         except Exception as e:
#             logger.error(f"Error adding documents to knowledge base: {str(e)}")
    
#     def add_crm_data(self, crm_data: List[Dict[str, Any]]):
#         """Add CRM data to the knowledge base"""
#         try:
#             documents = []
            
#             for item in crm_data:
#                 # Convert CRM data to text format
#                 content = self._format_crm_item(item)
#                 if content:
#                     documents.append({
#                         "id": f"crm_{uuid.uuid4()}",
#                         "content": content,
#                         "metadata": {
#                             "category": "crm_data",
#                             "type": item.get("type", "unknown"),
#                             "timestamp": datetime.now().isoformat()
#                         }
#                     })
            
#             if documents:
#                 self.add_documents(documents)
#                 logger.info(f"Added {len(documents)} CRM data items to knowledge base")
#         except Exception as e:
#             logger.error(f"Error adding CRM data to knowledge base: {str(e)}")
    
#     def _format_crm_item(self, item: Dict[str, Any]) -> Optional[str]:
#         """Format a CRM data item as text"""
#         try:
#             item_type = item.get("type", "")
            
#             if item_type == "customer":
#                 return f"Customer: {item.get('name', 'N/A')}, Email: {item.get('email', 'N/A')}, Phone: {item.get('phone', 'N/A')}"
#             elif item_type == "invoice":
#                 return f"Invoice ID: {item.get('id', 'N/A')}, Amount: {item.get('amount', 'N/A')} {item.get('currency', 'USD')}, Status: {item.get('status', 'N/A')}, Due Date: {item.get('due_date', 'N/A')}"
#             elif item_type == "payment":
#                 return f"Payment ID: {item.get('id', 'N/A')}, Amount: {item.get('amount', 'N/A')} {item.get('currency', 'USD')}, Method: {item.get('payment_method', 'N/A')}, Status: {item.get('status', 'N/A')}"
#             elif item_type == "subscription":
#                 return f"Subscription ID: {item.get('id', 'N/A')}, Plan: {item.get('plan_name', 'N/A')}, Amount: {item.get('amount', 'N/A')} {item.get('currency', 'USD')}, Status: {item.get('status', 'N/A')}"
#             else:
#                 # Generic formatting for other types
#                 return json.dumps(item, default=str)
#         except Exception as e:
#             logger.error(f"Error formatting CRM item: {str(e)}")
#             return None
    
#     def search_relevant_documents(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
#         """Search for relevant documents in the knowledge base"""
#         try:
#             results = self.collection.query(
#                 query_texts=[query],
#                 n_results=n_results
#             )
            
#             # Format results
#             formatted_results = []
#             for i in range(len(results['ids'][0])):
#                 formatted_results.append({
#                     "id": results['ids'][0][i],
#                     "content": results['documents'][0][i],
#                     "metadata": results['metadatas'][0][i] if results['metadatas'][0][i] else {},
#                     "distance": results['distances'][0][i] if 'distances' in results and results['distances'][0][i] else None
#                 })
            
#             return formatted_results
#         except Exception as e:
#             logger.error(f"Error searching knowledge base: {str(e)}")
#             return []
    
#     def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
#         """Generate embeddings for a list of texts"""
#         try:
#             embeddings = self.embedding_model.encode(texts)
#             return embeddings.tolist()
#         except Exception as e:
#             logger.error(f"Error generating embeddings: {str(e)}")
#             return []

# # Global instance of the RAG service
# rag_service = RAGService()
