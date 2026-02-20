#!/usr/bin/env python3
"""
Main execution script for the Financial Analysis Multi-Agent System
"""

import asyncio
import os
import sys
import signal
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from mcp_servers import start_mcp_servers, stop_mcp_servers
from main import FinancialAnalysisMultiAgentSystem, test_mcp_connections


def print_banner():
    """Print system banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║     🤖 DEEPSEEK MULTI-AGENT FINANCIAL ANALYSIS SYSTEM    ║
    ║              with MCP Server Architecture                 ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_api_key():
    """Check if DeepSeek API key is set"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("\n❌ ERROR: DEEPSEEK_API_KEY not found in .env file")
        print("\nPlease add your DeepSeek API key to the .env file:")
        print('echo "DEEPSEEK_API_KEY=your-key-here" > .env')
        print("\nGet your API key from: https://platform.deepseek.com/")
        return False
    
    # Show masked key
    masked_key = f"{api_key[:8]}...{api_key[-4:]}"
    print(f"\n✅ DeepSeek API Key found: {masked_key}")
    return True


def setup_directories():
    """Create necessary directories"""
    dirs = ["./generated_reports", "./logs", "./data"]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created directory: {dir_path}")
    return True


async def main():
    """Main execution function"""
    print_banner()
    
    # Check prerequisites
    if not check_api_key():
        return 1
    
    print("\n" + "="*60)
    print("📁 SETTING UP ENVIRONMENT")
    print("="*60)
    setup_directories()
    
    # Test data
    test_documents = [
        "financial_statements_2023.pdf",
        "balance_sheet_q4.pdf",
        "cash_flow_statement.pdf"
    ]
    
    company_info = {
        "name": "TechCorp AI Solutions Inc.",
        "tickers": ["TCAI", "TECH"],
        "sector": "Technology",
        "industry": "AI Software",
        "fiscal_year_end": "2023-12-31",
        "headquarters": "San Francisco, CA",
        "employees": 2500
    }
    
    print(f"\n📋 Analysis Target:")
    print(f"  • Company: {company_info['name']}")
    print(f"  • Sector: {company_info['sector']}")
    print(f"  • Tickers: {', '.join(company_info['tickers'])}")
    print(f"  • Documents: {len(test_documents)} files")
    
    # Start MCP servers
    servers = await start_mcp_servers()
    await asyncio.sleep(2)  # Give servers time to initialize
    
    # Test connections
    print("\n🔌 Testing MCP connections...")
    connections_ok = await test_mcp_connections()
    if not connections_ok:
        print("\n⚠️ Some MCP connections failed - continuing with mock data...")
    
    # Initialize and run the system
    try:
        print("\n" + "="*60)
        print("🤖 INITIALIZING MULTI-AGENT SYSTEM")
        print("="*60)
        
        system = FinancialAnalysisMultiAgentSystem()
        
        # Execute workflow
        results = await system.execute_workflow(test_documents, company_info)
        
        # Display results
        print("\n" + "="*60)
        print("📊 FINAL RESULTS")
        print("="*60)
        
        print(f"\n✅ Workflow ID: {results['workflow_id']}")
        print(f"📈 Status: {results['status'].upper()}")
        print(f"⏱️ Execution Time: {results.get('execution_time_seconds', 0)} seconds")
        print(f"🤖 AI Model: {results.get('ai_model', 'deepseek-chat')}")
        
        if results['status'] == 'completed':
            print("\n🔍 Key Findings:")
            
            risk = results['results'].get('risk', {})
            compliance = results['results'].get('compliance', {})
            quality = results['results'].get('quality', {})
            
            print(f"  • Risk Score: {risk.get('risk_score', 'N/A')}/10")
            print(f"  • Risk Level: {risk.get('risk_level', 'N/A')}")
            print(f"  • Compliance Status: {compliance.get('compliance_status', 'Unknown').upper()}")
            print(f"  • Confidence Score: {quality.get('confidence_score', 0)*100:.1f}%")
            
            # Report location
            report_url = results['results'].get('report', 'N/A')
            if report_url and report_url != 'N/A':
                print(f"\n📑 Report: {report_url}")
                
                # Check if files were actually created
                reports_dir = "./generated_reports"
                if os.path.exists(reports_dir):
                    files = os.listdir(reports_dir)
                    if files:
                        print(f"\n📁 Reports saved in: {os.path.abspath(reports_dir)}")
                        print("Recent files:")
                        for f in sorted(files, reverse=True)[:5]:
                            file_path = os.path.join(reports_dir, f)
                            size = os.path.getsize(file_path)
                            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                            print(f"  • {f} ({size} bytes) - {mod_time.strftime('%H:%M:%S')}")
        
        else:
            print(f"\n❌ Workflow failed: {results.get('error', 'Unknown error')}")
        
        print("\n" + "="*60)
        print("🟢 SYSTEM IS RUNNING - Press Ctrl+C to stop servers")
        print("="*60)
        print("\n📊 You can:")
        print("  • View reports in ./generated_reports/")
        print("  • Open HTML files in your browser")
        print("  • Press Ctrl+C to shutdown gracefully")
        
        # Keep running until user interrupts
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down...")
            await stop_mcp_servers(servers)
            print("\n✅ System shutdown complete")
            print("📁 Your reports are still available in ./generated_reports/")
        
    except Exception as e:
        print(f"\n❌ System error: {e}")
        await stop_mcp_servers(servers)
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)