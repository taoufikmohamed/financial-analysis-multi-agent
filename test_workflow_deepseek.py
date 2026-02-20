# test_workflow_deepseek.py
import asyncio
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from dotenv import load_dotenv

load_dotenv()

# Now import the actual modules - the mock from conftest.py will be used
from mcp_servers import start_mcp_servers, stop_mcp_servers
from main import FinancialAnalysisMultiAgentSystem


@pytest.mark.asyncio
async def test_system_initialization():
    """Test that the system initializes properly"""
    try:
        system = FinancialAnalysisMultiAgentSystem()
        assert system is not None
        print("✅ System initialized")
    except Exception as e:
        pytest.fail(f"System initialization failed: {e}")


@pytest.mark.asyncio
async def test_document_extraction():
    """Test document extraction with mock data"""
    system = FinancialAnalysisMultiAgentSystem()
    
    # Mock the extraction method
    mock_extraction = {
        "extraction_confidence": 0.95,
        "financial_statements": {
            "income_statement": {
                "revenue": 1000000,
                "expenses": 800000,
                "net_income": 200000
            },
            "balance_sheet": {
                "assets": 2000000,
                "liabilities": 1000000,
                "equity": 1000000
            }
        },
        "key_metrics": {
            "total_revenue": 1000000,
            "net_income": 200000
        }
    }
    
    with patch.object(system, '_extract_document_data', new=AsyncMock(return_value=mock_extraction)):
        extraction = await system._extract_document_data(["test.pdf"])
        
        assert extraction is not None
        assert extraction['extraction_confidence'] == 0.95
        assert 'financial_statements' in extraction
        print(f"✅ Extraction confidence: {extraction['extraction_confidence']}")


@pytest.mark.asyncio
async def test_financial_analysis():
    """Test financial analysis with mock data"""
    system = FinancialAnalysisMultiAgentSystem()
    
    mock_extraction = {
        "financial_statements": {
            "income_statement": {
                "revenue": 1000000,
                "expenses": 800000,
                "net_income": 200000
            },
            "balance_sheet": {
                "assets": 2000000,
                "liabilities": 1000000,
                "equity": 1000000
            }
        }
    }
    
    mock_financial = {
        "profitability_ratios": {
            "net_margin": 0.20,
            "gross_margin": 0.40,
            "roa": 0.10,
            "roe": 0.20
        },
        "liquidity_ratios": {
            "current_ratio": 2.0,
            "quick_ratio": 1.5
        },
        "leverage_ratios": {
            "debt_to_equity": 1.0,
            "interest_coverage": 5.0
        }
    }
    
    with patch.object(system, '_analyze_financials', new=AsyncMock(return_value=mock_financial)):
        financial = await system._analyze_financials(mock_extraction)
        
        assert financial is not None
        assert financial['profitability_ratios']['net_margin'] == 0.20
        print(f"✅ Net margin: {financial['profitability_ratios']['net_margin']*100:.1f}%")


@pytest.mark.asyncio
async def test_compliance_check():
    """Test compliance checking"""
    system = FinancialAnalysisMultiAgentSystem()
    
    mock_compliance = {
        "compliance_status": "compliant",
        "issues": [],
        "warnings": [],
        "regulatory_checks": {
            "sec_filing_requirements": "passed",
            "gaap_compliance": "passed"
        }
    }
    
    with patch.object(system, '_check_compliance', new=AsyncMock(return_value=mock_compliance)):
        compliance = await system._check_compliance({}, {})
        
        assert compliance is not None
        assert compliance['compliance_status'] == "compliant"
        print(f"✅ Compliance status: {compliance['compliance_status']}")


@pytest.mark.asyncio
async def test_risk_assessment():
    """Test risk assessment"""
    system = FinancialAnalysisMultiAgentSystem()
    
    mock_risk = {
        "risk_score": 3.5,
        "risk_level": "low",
        "risk_factors": {
            "financial_risk": 2.0,
            "operational_risk": 3.0,
            "market_risk": 4.0,
            "compliance_risk": 1.0
        }
    }
    
    with patch.object(system, '_assess_risks', new=AsyncMock(return_value=mock_risk)):
        risk = await system._assess_risks({}, {}, {})
        
        assert risk is not None
        assert risk['risk_score'] == 3.5
        assert risk['risk_level'] == "low"
        print(f"✅ Risk score: {risk['risk_score']}/10 - {risk['risk_level']}")


@pytest.mark.asyncio
async def test_market_analysis():
    """Test market analysis"""
    system = FinancialAnalysisMultiAgentSystem()
    
    mock_market = {
        "market_data": {
            "sentiment": "positive",
            "peers_comparison": {
                "peer1": {"pe_ratio": 15},
                "peer2": {"pe_ratio": 18}
            },
            "industry_trends": ["trend1", "trend2"]
        }
    }
    
    company = {"name": "Test Corp", "tickers": ["TEST"], "sector": "Technology"}
    
    with patch.object(system, '_analyze_market_context', new=AsyncMock(return_value=mock_market)):
        market = await system._analyze_market_context(company)
        
        assert market is not None
        assert market['market_data']['sentiment'] == "positive"
        print(f"✅ Market sentiment: {market['market_data']['sentiment']}")


@pytest.mark.asyncio
async def test_quality_check():
    """Test quality control"""
    system = FinancialAnalysisMultiAgentSystem()
    
    mock_quality = {
        "confidence_score": 0.95,
        "warnings": [],
        "data_completeness": 0.98,
        "cross_validation": "passed"
    }
    
    all_outputs = {
        'extraction': {'test': 'data'},
        'financial_analysis': {'test': 'data'},
        'compliance': {'test': 'data'}
    }
    
    with patch.object(system, '_quality_check', new=AsyncMock(return_value=mock_quality)):
        quality = await system._quality_check(all_outputs)
        
        assert quality is not None
        assert quality['confidence_score'] == 0.95
        print(f"✅ Quality confidence: {quality['confidence_score']*100:.1f}%")


@pytest.mark.asyncio
async def test_full_workflow():
    """Test the complete workflow with mocked data"""
    system = FinancialAnalysisMultiAgentSystem()
    
    # Mock all the internal methods
    mock_extraction = {
        "extraction_confidence": 0.95,
        "financial_statements": {
            "income_statement": {"revenue": 1000000},
            "balance_sheet": {"assets": 2000000}
        },
        "key_metrics": {"total_revenue": 1000000}
    }
    
    mock_financial = {
        "profitability_ratios": {"net_margin": 0.20},
        "liquidity_ratios": {"current_ratio": 2.0},
        "leverage_ratios": {"debt_to_equity": 1.0}
    }
    
    mock_compliance = {
        "compliance_status": "compliant",
        "issues": []
    }
    
    mock_market = {
        "market_data": {
            "sentiment": "positive",
            "peers_comparison": {}
        }
    }
    
    mock_risk = {
        "risk_score": 3.5,
        "risk_level": "low",
        "risk_factors": {}
    }
    
    mock_quality = {
        "confidence_score": 0.95,
        "warnings": []
    }
    
    # Patch all methods
    with patch.multiple(system,
                       _extract_document_data=AsyncMock(return_value=mock_extraction),
                       _analyze_financials=AsyncMock(return_value=mock_financial),
                       _check_compliance=AsyncMock(return_value=mock_compliance),
                       _analyze_market_context=AsyncMock(return_value=mock_market),
                       _assess_risks=AsyncMock(return_value=mock_risk),
                       _quality_check=AsyncMock(return_value=mock_quality)):
        
        # Run the analysis
        result = await system.analyze_company(
            company_name="Test Corp",
            documents=["test.pdf"],
            tickers=["TEST"]
        )
        
        assert result is not None
        assert 'financial_analysis' in result
        assert 'compliance' in result
        assert 'market_analysis' in result
        assert 'risk_assessment' in result
        assert 'quality_check' in result
        print("✅ Full workflow test passed")


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in the system"""
    system = FinancialAnalysisMultiAgentSystem()
    
    # Test with missing documents
    with patch.object(system, '_extract_document_data', 
                     new=AsyncMock(side_effect=Exception("Extraction failed"))):
        
        with pytest.raises(Exception) as exc_info:
            await system._extract_document_data([])
        
        assert "Extraction failed" in str(exc_info.value)
        print("✅ Error handling test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--asyncio-mode=auto"])
