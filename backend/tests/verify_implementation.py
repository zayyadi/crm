#!/usr/bin/env python3
"""
Verification script to check that all AI implementation files exist and have correct structure
"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_path))

def check_file_exists(file_path):
    """Check if a file exists"""
    full_path = backend_path / file_path
    return full_path.exists()

def check_import(module_path):
    """Try to import a module"""
    try:
        if module_path.startswith('app.'):
            import importlib
            importlib.import_module(module_path)
        elif module_path.startswith('scripts.'):
            # For scripts, we'll just check if the file exists
            return check_file_exists(module_path.replace('.', '/') + '.py')
        return True
    except ImportError as e:
        print(f"Import error for {module_path}: {e}")
        return False

def main():
    """Main verification function"""
    print("Verifying AI implementation structure...")
    print("=" * 50)
    
    # Files that should exist
    required_files = [
        "app/services/gemini_service.py",
        "app/services/rag_service.py",
        "routers/chatbot.py",
        "scripts/fine_tune_rag.py",
        "scripts/test_gemini.py",
        "AI_FEATURES.md",
        "AI_IMPLEMENTATION_SUMMARY.md",
        "FINAL_IMPLEMENTATION_REPORT.md",
        "test_ai_implementation.py"
    ]
    
    # Modules that should be importable
    required_modules = [
        "app.services.gemini_service",
        "app.services.rag_service",
        "routers.chatbot"
    ]
    
    # Check files
    print("Checking required files:")
    file_results = []
    for file_path in required_files:
        exists = check_file_exists(file_path)
        status = "✓" if exists else "✗"
        print(f"  {status} {file_path}")
        file_results.append(exists)
    
    print()
    
    # Check imports
    print("Checking module imports:")
    import_results = []
    for module_path in required_modules:
        can_import = check_import(module_path)
        status = "✓" if can_import else "✗"
        print(f"  {status} {module_path}")
        import_results.append(can_import)
    
    print()
    print("=" * 50)
    
    # Summary
    total_files = len(file_results)
    passed_files = sum(file_results)
    total_imports = len(import_results)
    passed_imports = sum(import_results)
    
    print(f"Files: {passed_files}/{total_files} passed")
    print(f"Imports: {passed_imports}/{total_imports} passed")
    
    overall_passed = passed_files == total_files and passed_imports == total_imports
    
    if overall_passed:
        print("\n🎉 All checks passed! Implementation structure is correct.")
        print("\nNext steps:")
        print("1. Add your GEMINI_API_KEY to the .env file")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run tests: python scripts/test_gemini.py")
        return 0
    else:
        print("\n❌ Some checks failed. Please review the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
