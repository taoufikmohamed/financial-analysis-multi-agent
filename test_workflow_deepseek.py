"""
Test script for the Financial Analysis Multi-Agent System
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Import system components
from mcp_servers import start_mcp_servers, stop_mcp_servers
from main import FinancialAnalysisMultiAgentSystem


async def test_all_components():
    """Test all system components"""
    
    print("🧪 TESTING MULTI-AGENT SYSTEM")
    print("="*60)
    
    # Start servers
    print("\n1️⃣ Starting MCP servers...")
    servers = await start_mcp_servers()
    await asyncio.sleep(2)
    
    # Initialize system
    print("\n2️⃣ Initializing system...")
    try:
        system = FinancialAnalysisMultiAgentSystem()
        print("✅ System initialized")
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        return False
    
    # Test individual components
    print("\n3️⃣ Testing individual agents...")
    
    # Test document extraction
    print("\n  📄 Testing Document Extraction...")
    docs = ["test.pdf"]
    extraction = await system._extract_document_data(docs)
    if extraction and 'extraction_confidence' in extraction:
        print(f"  ✅ Extraction confidence: {extraction['extraction_confidence']}")
    else:
        print("  ❌ Extraction failed")
    
    # Test financial analysis
    print("\n  📊 Testing Financial Analysis...")
    financial = await system._analyze_financials(extraction)
    if financial and 'profitability_ratios' in financial:
        print(f"  ✅ Net margin: {financial['profitability_ratios']['net_margin']*100:.1f}%")
    else:
        print("  ❌ Financial analysis failed")
    
    # Test compliance
    print("\n  ⚖️ Testing Compliance Check...")
    compliance = await system._check_compliance(extraction, financial)
    if compliance and 'compliance_status' in compliance:
        print(f"  ✅ Compliance status: {compliance['compliance_status']}")
    else:
        print("  ❌ Compliance check failed")
    
    # Test market analysis
    print("\n  📈 Testing Market Analysis...")
    company = {"name": "Test Corp", "tickers": ["TEST"], "sector": "Technology"}
    market = await system._analyze_market_context(company)
    if market and 'market_data' in market:
        print(f"  ✅ Market sentiment: {market['market_data'].get('sentiment', 'unknown')}")
    else:
        print("  ❌ Market analysis failed")
    
    # Test risk assessment
    print("\n  ⚠️ Testing Risk Assessment...")
    risk = await system._assess_risks(financial, compliance, market)
    if risk and 'risk_score' in risk:
        print(f"  ✅ Risk score: {risk['risk_score']}/10 - {risk['risk_level']}")
    else:
        print("  ❌ Risk assessment failed")
    
    # Test quality control
    print("\n  ✅ Testing Quality Control...")
    all_outputs = {
        'extraction': extraction,
        'financial_analysis': financial,
        'compliance': compliance