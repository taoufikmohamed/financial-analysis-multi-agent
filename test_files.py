# test_files.py
import os
import glob

def test_check_files():
    """Check what files are available"""
    print("\n📁 Current directory contents:")
    for file in sorted(glob.glob("*")):
        print(f"  - {file}")
    
    print("\n📁 Python files:")
    for file in sorted(glob.glob("*.py")):
        print(f"  - {file}")
    
    # Check if main.py exists and read its content
    if os.path.exists("main.py"):
        print("\n📄 main.py first 10 lines:")
        with open("main.py", "r") as f:
            for i, line in enumerate(f):
                if i < 10:
                    print(f"    {i+1}: {line.rstrip()}")
                else:
                    break
    
    # Check if mcp_servers.py exists
    if os.path.exists("mcp_servers.py"):
        print("\n📄 mcp_servers.py first 10 lines:")
        with open("mcp_servers.py", "r") as f:
            for i, line in enumerate(f):
                if i < 10:
                    print(f"    {i+1}: {line.rstrip()}")
                else:
                    break
