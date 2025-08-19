
"""
Script to test the Gemini AI integration
"""

import os
import sys
import asyncio
import logging


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.gemini_service import gemini_service


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_gemini_service():
    """Test the Gemini service"""
    try:
        logger.info("Testing Gemini AI service...")
        
        
        test_message = "Hello, how can you help me with my CRM system?"
        response = await gemini_service.generate_response(test_message)
        
        logger.info(f"Input: {test_message}")
        logger.info(f"Response: {response}")
        
        
        test_message_with_context = "What are my current invoices?"
        response_with_context = await gemini_service.generate_response(
            test_message_with_context, 
            "dummy_customer_id"
        )
        
        logger.info(f"Input with context: {test_message_with_context}")
        logger.info(f"Response with context: {response_with_context}")
        
        logger.info("Gemini AI service test completed successfully!")
        return True
    except Exception as e:
        logger.error(f"Error testing Gemini AI service: {str(e)}")
        return False

async def main():
    """Main function to run the tests"""
    try:
        success = await test_gemini_service()
        if success:
            print("All tests passed!")
            sys.exit(0)
        else:
            print("Some tests failed!")
            sys.exit(1)
    except Exception as e:
        print(f"Test execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
