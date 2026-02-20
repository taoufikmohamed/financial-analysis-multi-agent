# test_diagnostic.py
import sys
import traceback

def test_import_diagnostic():
    """Diagnose import issues"""
    print("\n🔍 DIAGNOSTIC INFORMATION")
    print("=" * 50)
    
    # Check Python path
    print("\n📂 Python Path:")
    for path in sys.path:
        print(f"  - {path}")
    
    # Try to import modules one by one
    print("\n📦 Testing imports:")
    
    # Test mcp_servers
    try:
        import mcp_servers
        print("  ✅ mcp_servers imported successfully")
        print(f"     Contents: {dir(mcp_servers)}")
    except Exception as e:
        print(f"  ❌ mcp_servers import failed: {e}")
        traceback.print_exc()
    
    # Test main
    try:
        import main
        print("  ✅ main imported successfully")
        print(f"     Contents: {dir(main)}")
    except Exception as e:
        print(f"  ❌ main import failed: {e}")
        traceback.print_exc()
    
    # Check if FinancialAnalysisMultiAgentSystem exists
    try:
        from main import FinancialAnalysisMultiAgentSystem
        print("  ✅ FinancialAnalysisMultiAgentSystem imported successfully")
    except Exception as e:
        print(f"  ❌ FinancialAnalysisMultiAgentSystem import failed: {e}")
        traceback.print_exc()
    
    print("\n" + "=" * 50)
