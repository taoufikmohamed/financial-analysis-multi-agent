# test_import_diagnostic.py
import sys
import os
import traceback

def test_import_main():
    """Try to import main and see what happens"""
    print("\n" + "="*60)
    print("🔍 IMPORT DIAGNOSTIC")
    print("="*60)
    
    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("\n❌ main.py does not exist in current directory")
        print(f"Current directory: {os.getcwd()}")
        print("Files:", os.listdir('.'))
        return
    
    print("\n✅ main.py exists")
    
    # Try to read main.py
    print("\n📄 Reading main.py:")
    try:
        with open('main.py', 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            print(f"  Successfully read {len(content)} characters")
            print(f"  First 200 characters:")
            print("-" * 40)
            print(content[:200])
            print("-" * 40)
            
            # Look for class definition
            if 'class FinancialAnalysisMultiAgentSystem' in content:
                print("\n✅ Found FinancialAnalysisMultiAgentSystem class")
            else:
                print("\n❌ Could not find FinancialAnalysisMultiAgentSystem class")
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
    
    # Try to import the module
    print("\n📦 Attempting to import main module:")
    try:
        import main
        print("  ✅ main imported successfully")
        print(f"  main module attributes: {dir(main)}")
        
        # Check for the class
        if hasattr(main, 'FinancialAnalysisMultiAgentSystem'):
            print("  ✅ FinancialAnalysisMultiAgentSystem found in main")
        else:
            print("  ❌ FinancialAnalysisMultiAgentSystem NOT found in main")
            
    except Exception as e:
        print(f"  ❌ Failed to import main: {e}")
        traceback.print_exc()
    
    print("\n" + "="*60)