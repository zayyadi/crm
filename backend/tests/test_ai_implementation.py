#!/usr/bin/env python3
"""
Test file to verify the AI implementation structure
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_gemini_service_structure():
    """Test that the Gemini service can be imported without errors"""
    try:
        from app.services.gemini_service import GeminiService
        print("✓ GeminiService class can be imported")
        return True
    except ImportError as e:
        print(f"✗ Failed to import GeminiService: {e}")
        return False

def test_rag_service_structure():
    """Test that the RAG service can be imported without errors"""
    try:
        from app.services.rag_service import RAGService
        print("✓ RAGService class can be imported")
        return True
    except ImportError as e:
        print(f"✗ Failed to import RAGService: {e}")
        return False

def test_chatbot_router_structure():
    """Test that the chatbot router can be imported without errors"""
    try:
        import routers.chatbot
        print("✓ Chatbot router can be imported")
        return True
    except ImportError as e:
        print(f"✗ Failed to import chatbot router: {e}")
        return False

def test_fine_tune_script_structure():
    """Test that the fine-tune script can be imported without errors"""
    try:
        import scripts.fine_tune_rag
        print("✓ Fine-tune script can be imported")
        return True
    except ImportError as e:
        print(f"✗ Failed to import fine-tune script: {e}")
        return False

def test_test_script_structure():
    """Test that the test script can be imported without errors"""
    try:
        import scripts.test_gemini
        print("✓ Test script can be imported")
        return True
    except ImportError as e:
        print(f"✗ Failed to import test script: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing AI implementation structure...")
    print("=" * 50)
    
    tests = [
        test_gemini_service_structure,
        test_rag_service_structure,
        test_chatbot_router_structure,
        test_fine_tune_script_structure,
        test_test_script_structure
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("All tests passed! The AI implementation structure is correct.")
        return 0
    else:
        print("Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
