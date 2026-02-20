"""
mcp_servers.py — MCP Server Ecosystem for Financial Analysis
=============================================================
Defines four FastMCP-compatible HTTP servers, each exposing domain-specific
tools via the Model Context Protocol (MCP):

  Port 8001  DocumentProcessingMCPServer  — PDF/OCR extraction
  Port 8002  ComplianceDatabaseMCPServer  — SEC/SOX/IFRS/GAAP checks
  Port 8003  MarketDataMCPServer          — prices, sector, macro data
  Port 8004  ReportingMCPServer           — HTML/TXT/JSON report writer

All servers simulate real-world behaviour with realistic mock data so the
system can run fully offline / in testing mode without external API calls.

Usage:
    servers = await start_mcp_servers()
    ...
    await stop_mcp_servers(servers)
"""

import asyncio
import os
import json
import random
from datetime import datetime

# ---------------------------------------------------------------------------
# Local MCPServer stub

# ---------------------------------------------------------------------------
# The four servers in this file are simulation/mock implementations that do
# not need (and cannot use) the published `mcp` library's MCPServer class,
# because that class does not exist in the installable package.
# This lightweight base class provides the same interface so the rest of the
# file works unchanged.

class MCPServer:
    """Minimal base class for mock MCP servers used in testing."""

    def __init__(self, server_name: str, version: str, port: int, tools: list):
        self.server_name = server_name
        self.version = version
        self.port = port
        self.tools = tools

    async def handle_tool_call(self, tool_name: str, parameters: dict) -> dict:
        raise NotImplementedError


from typing import Dict, Any, List
import traceback


class DocumentProcessingMCPServer(MCPServer):
    """
    MCP Server — Document Processor (port 8001).

    Exposed tools:
      extract_financial_data  — Parses PDF/image files via OCR and returns
                                 structured income, balance, and cash-flow
                                 statements as JSON.
      health_check            — Returns server liveness status.
    """
    
    def __init__(self, port=8001):
        super().__init__(
            server_name="document_processor",
            version="1.0.0",
            port=port,
            tools=[
                {
                    "name": "extract_financial_data",
                    "description": "Extract financial data from documents",
                    "parameters": {
                        "file_paths": {"type": "array", "items": {"type": "string"}},
                        "extract_tables": {"type": "boolean"},
                        "ocr_enabled": {"type": "boolean"},
                        "language": {"type": "string"}
                    }
                },
                {
                    "name": "health_check",
                    "description": "Check server health",
                    "parameters": {}
                }
            ]
        )
        print(f"✅ Document Processing MCP Server initialized on port {port}")
    
    async def handle_tool_call(self, tool_name: str, parameters: dict) -> dict:
        """Handle tool calls from clients"""
        print(f"📄 Document MCP: Processing {tool_name}")
        
        if tool_name == "extract_financial_data":
            try:
                # Simulate document processing
                await asyncio.sleep(1)
                
                # Mock extracted data
                return {
                    "status": "success",
                    "statements": {
                        "income": {
                            "revenue": 10500000,
                            "cost_of_goods": 4200000,
                            "gross_profit": 6300000,
                            "operating_expenses": 2800000,
                            "operating_income": 3500000,
                            "net_income": 2600000
                        },
                        "balance": {
                            "assets": 15200000,
                            "liabilities": 7000000,
                            "equity": 8200000,
                            "cash": 2500000,
                            "receivables": 1800000
                        },
                        "cash_flow": {
                            "operating": 2770000,
                            "investing": -1200000,
                            "financing": -300000
                        }
                    },
                    "disclosures": [
                        "Note 1: Accounting Policies - Company uses accrual accounting",
                        "Note 2: Revenue Recognition - Recognized upon delivery",
                        "Note 3: Risk Factors - Market competition and regulatory changes"
                    ],
                    "metadata": {
                        "pages": 45,
                        "language": parameters.get("language", "en"),
                        "processed_date": datetime.now().isoformat(),
                        "document_count": len(parameters.get("file_paths", []))
                    },
                    "confidence": 0.96,
                    "processing_time_ms": 1234
                }
            except Exception as e:
                return {"status": "error", "error": str(e)}
        
        elif tool_name == "health_check":
            return {
                "status": "healthy", 
                "timestamp": datetime.now().isoformat(),
                "server": "document_processor"
            }
        
        return {"status": "error", "error": "Unknown tool"}


class ComplianceDatabaseMCPServer(MCPServer):
    """
    MCP Server — Compliance Database (port 8002).

    Exposed tools:
      check_regulatory_compliance — Validates financial data against
        SEC, SOX, IFRS, and GAAP frameworks. Returns a compliance_score
        (0-1), list of hard violations, and advisory warnings.
        Warnings are probabilistic to simulate real-world variance.
    """
    
    def __init__(self, port=8002):
        super().__init__(
            server_name="compliance_database",
            version="1.0.0",
            port=port,
            tools=[
                {
                    "name": "check_regulatory_compliance",
                    "description": "Check documents against regulations",
                    "parameters": {
                        "document_data": {"type": "object"},
                        "analysis_results": {"type": "object"},
                        "regulations": {"type": "array"},
                        "jurisdiction": {"type": "string"}
                    }
                }
            ]
        )
        print(f"✅ Compliance MCP Server initialized on port {port}")
    
    async def handle_tool_call(self, tool_name: str, parameters: dict) -> dict:
        """Handle compliance checks"""
        print(f"⚖️ Compliance MCP: Checking regulations")
        
        if tool_name == "check_regulatory_compliance":
            try:
                await asyncio.sleep(1)
                
                # Mock compliance check results
                violations = []
                warnings = []
                
                # Add some realistic warnings
                if random.random() > 0.5:
                    warnings.append("Revenue recognition disclosure needs more detail")
                if random.random() > 0.6:
                    warnings.append("Related party transactions not fully disclosed")
                if random.random() > 0.7:
                    warnings.append("Risk factor section could be more comprehensive")
                
                return {
                    "status": "compliant" if len(violations) == 0 else "non_compliant",
                    "violations": violations,
                    "warnings": warnings,
                    "recommendations": [
                        "Update revenue recognition policies in disclosure notes",
                        "Add more detail to risk factors section",
                        "Enhance related party transaction disclosure"
                    ],
                    "regulations_checked": parameters.get("regulations", ["SEC", "SOX", "IFRS"]),
                    "compliance_score": 0.95 - (len(warnings) * 0.05),
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                return {"status": "error", "error": str(e)}
        
        return {"status": "error", "error": "Unknown tool"}


class MarketDataMCPServer(MCPServer):
    """
    MCP Server — Market Data (port 8003).

    Exposed tools:
      get_market_context — Returns simulated real-time stock prices,
        sector benchmarks (avg P/E, YTD performance), competitor market
        shares, and macro-economic indicators (interest rate, inflation,
        GDP, unemployment). Sentiment is randomised to reflect market
        volatility in testing.
    """
    
    def __init__(self, port=8003):
        super().__init__(
            server_name="market_data",
            version="1.0.0",
            port=port,
            tools=[
                {
                    "name": "get_market_context",
                    "description": "Get real-time market data",
                    "parameters": {
                        "symbols": {"type": "array"},
                        "sector": {"type": "string"},
                        "timeframe": {"type": "string"}
                    }
                }
            ]
        )
        print(f"✅ Market Data MCP Server initialized on port {port}")
    
    async def handle_tool_call(self, tool_name: str, parameters: dict) -> dict:
        """Fetch market data"""
        print(f"📈 Market MCP: Fetching data for {parameters.get('symbols', [])}")
        
        if tool_name == "get_market_context":
            try:
                await asyncio.sleep(1)
                
                symbols = parameters.get("symbols", ["TECH"])
                
                return {
                    "status": "success",
                    "price_data": {
                        symbol: {
                            "current_price": round(random.uniform(100, 500), 2),
                            "daily_change": round(random.uniform(-5, 5), 2),
                            "volume": random.randint(1000000, 5000000),
                            "pe_ratio": round(random.uniform(15, 30), 2),
                            "market_cap": random.randint(1000000000, 10000000000)
                        } for symbol in symbols
                    },
                    "sector_data": {
                        "sector": parameters.get("sector", "Technology"),
                        "avg_pe": 22.5,
                        "sector_growth": 0.15,
                        "market_cap": "5.2T",
                        "ytd_performance": 0.12
                    },
                    "competitors": [
                        {"name": "Competitor A", "market_share": 0.25, "stock_change": 2.3},
                        {"name": "Competitor B", "market_share": 0.20, "stock_change": -1.2},
                        {"name": "Competitor C", "market_share": 0.15, "stock_change": 3.1}
                    ],
                    "macro_indicators": {
                        "interest_rate": 0.0525,
                        "inflation": 0.031,
                        "gdp_growth": 0.024,
                        "unemployment": 0.038
                    },
                    "sentiment": random.choice(["bullish", "neutral", "bearish"]),
                    "timestamp": datetime.now().isoformat()
                }
            except Exception as e:
                return {"status": "error", "error": str(e)}
        
        return {"status": "error", "error": "Unknown tool"}


class ReportingMCPServer(MCPServer):
    """
    MCP Server — Report Generator (port 8004).

    Exposed tools:
      generate_financial_report — Writes three output files to ./generated_reports/:
          {report_id}.html  Styled dashboard with metrics, tables, and DeepSeek analysis
          {report_id}.txt   Plain-text summary for archival/email
          {report_id}.json  Full machine-readable data payload
      list_reports  — Returns metadata for the 10 most recent reports.
      health_check  — Returns server liveness + reports directory stats.
    """
    
    def __init__(self, port=8004):
        super().__init__(
            server_name="report_generator",
            version="1.0.0",
            port=port,
            tools=[
                {
                    "name": "generate_financial_report",
                    "description": "Generate formatted financial report",
                    "parameters": {
                        "analyses": {"type": "object"},
                        "executive_summary": {"type": "string"},
                        "format": {"type": "string"},
                        "template": {"type": "string"},
                        "report_id": {"type": "string"}
                    }
                },
                {
                    "name": "health_check",
                    "description": "Check server health",
                    "parameters": {}
                },
                {
                    "name": "list_reports",
                    "description": "List all generated reports",
                    "parameters": {}
                }
            ]
        )
        
        # Create reports directory
        self.reports_dir = "./generated_reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        print(f"📁 Report MCP: Files will be saved to {os.path.abspath(self.reports_dir)}")
        print(f"✅ Report MCP Server initialized on port {port}")
    
    async def handle_tool_call(self, tool_name: str, parameters: dict) -> dict:
        """Generate report and save to disk"""
        
        if tool_name == "generate_financial_report":
            return await self._generate_report(parameters)
        
        elif tool_name == "health_check":
            reports = os.listdir(self.reports_dir)
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "server": "report_generator",
                "reports_count": len(reports),
                "reports_dir": os.path.abspath(self.reports_dir)
            }
        
        elif tool_name == "list_reports":
            reports = os.listdir(self.reports_dir)
            report_details = []
            for report in sorted(reports, reverse=True)[:10]:
                path = os.path.join(self.reports_dir, report)
                size = os.path.getsize(path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(path))
                report_details.append({
                    "filename": report,
                    "size": f"{size} bytes",
                    "modified": mod_time.isoformat(),
                    "path": os.path.abspath(path)
                })
            return {
                "status": "success",
                "reports": report_details,
                "count": len(report_details)
            }
        
        return {"status": "error", "error": "Unknown tool"}
    
    async def _generate_report(self, parameters: dict) -> dict:
        """Internal method to generate and save report"""
        try:
            print(f"📑 Report MCP: Generating report...")
            
            # Get parameters
            analyses = parameters.get("analyses", {})
            executive_summary = parameters.get("executive_summary", "No summary provided")
            report_id = parameters.get("report_id", f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Extract data for report
            risk_data = analyses.get('risk', {})
            compliance_data = analyses.get('compliance', {})
            financial_data = analyses.get('financial_analysis', {})
            market_data = analyses.get('market', {})
            quality_data = analyses.get('quality', {})
            
            # Generate HTML report
            html_filename = f"{report_id}.html"
            html_path = os.path.join(self.reports_dir, html_filename)
            
            # Create HTML content
            html_content = self._generate_html_report(
                report_id, analyses, executive_summary,
                risk_data, compliance_data, financial_data,
                market_data, quality_data
            )
            
            # Save HTML file
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Generate and save text version
            txt_filename = f"{report_id}.txt"
            txt_path = os.path.join(self.reports_dir, txt_filename)
            
            txt_content = self._generate_text_report(
                report_id, analyses, executive_summary,
                risk_data, compliance_data, quality_data
            )
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(txt_content)
            
            # Generate PDF-like JSON data
            json_filename = f"{report_id}.json"
            json_path = os.path.join(self.reports_dir, json_filename)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(analyses, f, indent=2, default=str)
            
            print(f"✅ Report MCP: Files saved:")
            print(f"  • HTML: {html_path}")
            print(f"  • TXT: {txt_path}")
            print(f"  • JSON: {json_path}")
            
            return {
                "status": "success",
                "report_url": f"file://{os.path.abspath(html_path)}",
                "html_path": os.path.abspath(html_path),
                "txt_path": os.path.abspath(txt_path),
                "json_path": os.path.abspath(json_path),
                "report_id": report_id,
                "format": "html",
                "generated_at": datetime.now().isoformat(),
                "files": {
                    "html": os.path.basename(html_path),
                    "txt": os.path.basename(txt_path),
                    "json": os.path.basename(json_path)
                }
            }
            
        except Exception as e:
            print(f"❌ Report MCP Error: {str(e)}")
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "report_url": None
            }
    
    def _generate_html_report(self, report_id, analyses, summary, risk, compliance, financial, market, quality):
        """Build a self-contained HTML dashboard with inline CSS.
        Sections: executive summary, KPI cards, risk table, compliance
        detail, market context, financial ratios, and quality metrics.
        """
        
        # Determine risk color
        risk_level = risk.get('risk_level', 'MEDIUM').lower()
        risk_color = {
            'high': '#e74c3c',
            'medium': '#f39c12',
            'low': '#27ae60'
        }.get(risk_level, '#3498db')
        
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Financial Analysis Report - {report_id}</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background: #f5f5f5;
                    padding: 20px;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                    margin-bottom: 30px;
                }}
                h2 {{
                    color: #34495e;
                    margin: 25px 0 15px;
                    padding-left: 10px;
                    border-left: 4px solid #3498db;
                }}
                .section {{
                    background: #f8f9fa;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                }}
                .metric-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .metric-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                    border-top: 3px solid #3498db;
                }}
                .metric-value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #2c3e50;
                    margin: 10px 0;
                }}
                .metric-label {{
                    color: #7f8c8d;
                    font-size: 14px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                .risk-indicator {{
                    display: inline-block;
                    padding: 5px 15px;
                    border-radius: 20px;
                    font-weight: bold;
                    color: white;
                    background-color: {risk_color};
                }}
                .status-badge {{
                    display: inline-block;
                    padding: 3px 10px;
                    border-radius: 15px;
                    font-size: 12px;
                    font-weight: bold;
                }}
                .status-compliant {{ background: #27ae60; color: white; }}
                .status-warning {{ background: #f39c12; color: white; }}
                .status-error {{ background: #e74c3c; color: white; }}
                pre {{
                    background: white;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                    font-family: 'Courier New', monospace;
                    font-size: 14px;
                    border: 1px solid #e0e0e0;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #e0e0e0;
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 12px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #e0e0e0;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Financial Analysis Report</h1>
                
                <div style="margin-bottom: 30px;">
                    <p><strong>Report ID:</strong> {report_id}</p>
                    <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>AI Model:</strong> DeepSeek Chat</p>
                </div>
                
                <div class="section">
                    <h2>📋 Executive Summary</h2>
                    <div style="background: white; padding: 20px; border-radius: 5px;">
                        <p>{summary}</p>
                    </div>
                </div>
                
                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-label">Risk Score</div>
                        <div class="metric-value">{risk.get('risk_score', 'N/A')}/10</div>
                        <div><span class="risk-indicator">{risk.get('risk_level', 'N/A')}</span></div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-label">Compliance Status</div>
                        <div class="metric-value">{compliance.get('compliance_status', 'Unknown').upper()}</div>
                        <div>Violations: {len(compliance.get('violations', []))}</div>
                    </div>
                    
                    <div class="metric-card">
                        <div class="metric-label">Confidence Score</div>
                        <div class="metric-value">{quality.get('confidence_score', 0)*100:.1f}%</div>
                        <div>Issues: {len(quality.get('issues', []))}</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>⚠️ Risk Assessment Details</h2>
                    <table>
                        <tr>
                            <th>Risk Factor</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Risk Score</td>
                            <td><strong>{risk.get('risk_score', 'N/A')}/10</strong></td>
                        </tr>
                        <tr>
                            <td>Risk Level</td>
                            <td><span class="risk-indicator">{risk.get('risk_level', 'N/A')}</span></td>
                        </tr>
                        <tr>
                            <td>Compliance Issues</td>
                            <td>{risk.get('risk_factors', {{}}).get('compliance_issues', 0)}</td>
                        </tr>
                        <tr>
                            <td>Warnings Count</td>
                            <td>{risk.get('risk_factors', {{}}).get('warnings_count', 0)}</td>
                        </tr>
                    </table>
                    
                    <h3 style="margin-top: 20px;">DeepSeek Assessment</h3>
                    <pre>{risk.get('deepseek_assessment', 'No assessment available')}</pre>
                </div>
                
                <div class="section">
                    <h2>⚖️ Compliance Analysis</h2>
                    
                    <div style="margin-bottom: 15px;">
                        <span class="status-badge status-{'compliant' if compliance.get('compliance_status') == 'compliant' else 'warning'}">
                            {compliance.get('compliance_status', 'Unknown').upper()}
                        </span>
                    </div>
                    
                    <table>
                        <tr>
                            <th>Category</th>
                            <th>Count</th>
                            <th>Details</th>
                        </tr>
                        <tr>
                            <td>Violations</td>
                            <td>{len(compliance.get('violations', []))}</td>
                            <td>{', '.join(compliance.get('violations', ['None']))}</td>
                        </tr>
                        <tr>
                            <td>Warnings</td>
                            <td>{len(compliance.get('warnings', []))}</td>
                            <td>{', '.join(compliance.get('warnings', ['None']))}</td>
                        </tr>
                    </table>
                    
                    <h3>Recommendations</h3>
                    <ul>
                        {''.join([f'<li>{rec}</li>' for rec in compliance.get('recommendations', [])])}
                    </ul>
                </div>
                
                <div class="section">
                    <h2>📈 Market Context</h2>
                    <pre>{market.get('deepseek_analysis', 'No market analysis available')}</pre>
                    
                    <h3>Market Sentiment</h3>
                    <p><strong>{market.get('market_data', {{}}).get('sentiment', 'neutral').upper()}</strong></p>
                </div>
                
                <div class="section">
                    <h2>📊 Financial Analysis</h2>
                    <pre>{financial.get('deepseek_analysis', 'No financial analysis available')}</pre>
                    
                    <h3>Key Ratios</h3>
                    <table>
                        <tr>
                            <th>Ratio</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Net Margin</td>
                            <td>{financial.get('profitability_ratios', {{}}).get('net_margin', 0)*100:.1f}%</td>
                        </tr>
                        <tr>
                            <td>Debt to Equity</td>
                            <td>{financial.get('leverage_ratios', {{}}).get('debt_to_equity', 0):.2f}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="section">
                    <h2>✅ Quality Control</h2>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Confidence Score</td>
                            <td>{quality.get('confidence_score', 0)*100:.1f}%</td>
                        </tr>
                        <tr>
                            <td>Issues Found</td>
                            <td>{len(quality.get('issues', []))}</td>
                        </tr>
                    </table>
                    
                    {f'''
                    <h3>Issues</h3>
                    <ul>
                        {''.join([f'<li>{issue}</li>' for issue in quality.get('issues', [])])}
                    </ul>
                    ''' if quality.get('issues') else ''}
                </div>
                
                <div class="footer">
                    <p>Generated by DeepSeek Multi-Agent System with MCP Servers</p>
                    <p>Report files: HTML, TXT, and JSON saved in ./generated_reports/</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html
    
    def _generate_text_report(self, report_id, analyses, summary, risk, compliance, quality):
        """Plain-text version of the report for archiving or email delivery."""
        
        text = f"""
{'='*80}
FINANCIAL ANALYSIS REPORT
{'='*80}

Report ID: {report_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
AI Model: DeepSeek Chat

{'='*80}
EXECUTIVE SUMMARY
{'='*80}
{summary}

{'='*80}
KEY METRICS
{'='*80}
Risk Score: {risk.get('risk_score', 'N/A')}/10
Risk Level: {risk.get('risk_level', 'N/A')}
Compliance Status: {compliance.get('compliance_status', 'Unknown').upper()}
Confidence Score: {quality.get('confidence_score', 0)*100:.1f}%

{'='*80}
RISK ASSESSMENT
{'='*80}
Score: {risk.get('risk_score', 'N/A')}/10
Level: {risk.get('risk_level', 'N/A')}
Compliance Issues: {risk.get('risk_factors', {{}}).get('compliance_issues', 0)}
Warnings: {risk.get('risk_factors', {{}}).get('warnings_count', 0)}

DeepSeek Assessment:
{risk.get('deepseek_assessment', 'No assessment available')}

{'='*80}
COMPLIANCE DETAILS
{'='*80}
Status: {compliance.get('compliance_status', 'Unknown')}
Violations: {len(compliance.get('violations', []))}
Warnings: {len(compliance.get('warnings', []))}

Recommendations:
{chr(10).join(['- ' + r for r in compliance.get('recommendations', [])])}

{'='*80}
QUALITY METRICS
{'='*80}
Confidence Score: {quality.get('confidence_score', 0)*100:.1f}%
Issues: {len(quality.get('issues', []))}

{chr(10).join(['- ' + i for i in quality.get('issues', [])])}

{'='*80}
FILES GENERATED
{'='*80}
HTML: {report_id}.html
TXT: {report_id}.txt
JSON: {report_id}.json

Location: ./generated_reports/

{'='*80}
Report generated by DeepSeek Multi-Agent System
{'='*80}
"""
        return text


async def start_mcp_servers():
    """Start all MCP servers"""
    servers = [
        DocumentProcessingMCPServer(8001),
        ComplianceDatabaseMCPServer(8002),
        MarketDataMCPServer(8003),
        ReportingMCPServer(8004)
    ]
    
    print("\n" + "="*60)
    print("🚀 Starting MCP Servers...")
    print("="*60)
    
    for server in servers:
        try:
            await server.start()
            print(f"  ✅ {server.server_name} running on port {server.port}")
        except Exception as e:
            print(f"  ❌ Failed to start {server.server_name}: {e}")
    
    print("="*60)
    return servers


async def stop_mcp_servers(servers):
    """Stop all MCP servers"""
    print("\n🛑 Stopping MCP Servers...")
    for server in servers:
        try:
            await server.stop()
            print(f"  ✅ {server.server_name} stopped")
        except Exception as e:
            print(f"  ❌ Error stopping {server.server_name}: {e}")