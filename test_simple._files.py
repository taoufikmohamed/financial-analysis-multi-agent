# test_simple_files.py
import os
import glob

def test_check_files_simple():
    """Simple file check without chardet"""
    print("\n" + "="*60)
    print("📁 FILE SYSTEM CHECK")
    print("="*60)
    
    # List all files
    print("\n📄 All files in current directory:")
    files = sorted(glob.glob("*"))
    for f in files:
        size = os.path.getsize(f) if os.path.isfile(f) else 0
        f_type = "DIR" if os.path.isdir(f) else "FILE"
        print(f"  [{f_type}] {f} ({size} bytes)")
    
    # Check for important files
    print("\n🔍 Checking for required files:")
    required_files = ['main.py', 'mcp_servers.py']
    for req_file in required_files:
        if os.path.exists(req_file):
            print(f"  ✅ {req_file} found")
            # Try to read first few lines without encoding issues
            try:
                with open(req_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    print(f"     - {len(lines)} lines total")
                    print(f"     - First 3 lines:")
                    for i, line in enumerate(lines[:3]):
                        print(f"       {i+1}: {line.rstrip()[:50]}...")
            except Exception as e:
                print(f"     - Could not read file: {e}")
        else:
            print(f"  ❌ {req_file} NOT found")
    
    print("\n" + "="*60)