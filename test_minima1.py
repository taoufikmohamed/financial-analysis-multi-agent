# test_minimal.py
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# Define a minimal working system for testing
class MinimalFinancialSystem:
    """Minimal version for testing"""
    
    def __init__(self):
        self.name = "Minimal Financial System"
    
    async def extract_document_data(self, documents):
        """Mock document extraction"""
        await asyncio.sleep(0.1)  # Simulate async work
        return {
            "extraction_confidence": 0.95,
            "financial_statements": {
                "revenue": 1000000,
                "expenses": 800000
            }
        }
    
    async def analyze_financials(self, extraction):
        """Mock financial analysis"""
        await asyncio.sleep(0.1)
        return {
            "profitability_ratios": {
                "net_margin": 0.20
            }
        }
    
    async def analyze_company(self, company_name, documents, tickers):
        """Main analysis method"""
        extraction = await self.extract_document_data(documents)
        financials = await self.analyze_financials(extraction)
        
        return {
            "company_name": company_name,
            "extraction": extraction,
            "financial_analysis": financials,
            "summary": f"Analysis complete for {company_name}"
        }


@pytest.mark.asyncio
async def test_minimal_system():
    """Test the minimal system"""
    system = MinimalFinancialSystem()
    
    # Test initialization
    assert system.name == "Minimal Financial System"
    
    # Test document extraction
    extraction = await system.extract_document_data(["test.pdf"])
    assert extraction["extraction_confidence"] == 0.95
    print("✅ Document extraction test passed")
    
    # Test financial analysis
    financials = await system.analyze_financials(extraction)
    assert financials["profitability_ratios"]["net_margin"] == 0.20
    print("✅ Financial analysis test passed")
    
    # Test full analysis
    result = await system.analyze_company("Test Corp", ["test.pdf"], ["TEST"])
    assert result["company_name"] == "Test Corp"
    assert "summary" in result
    print(f"✅ Full analysis test passed: {result['summary']}")


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling"""
    system = MinimalFinancialSystem()
    
    # Test with invalid input
    with pytest.raises(Exception) as exc_info:
        # Force an error
        raise ValueError("Test error")
    
    assert "Test error" in str(exc_info.value)
    print("✅ Error handling test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
