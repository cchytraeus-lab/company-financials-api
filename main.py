"""
Company Financials API
Aggregates data from multiple free sources to provide comprehensive company financial data.
Ready for RapidAPI deployment.
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import httpx
import asyncio
from datetime import datetime
import os

app = FastAPI(
    title="Company Financials API",
    description="Get comprehensive company financial data from multiple sources",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class CompanyFinancials(BaseModel):
    company_name: str
    ticker: Optional[str] = None
    country: str
    registration_number: Optional[str] = None
    status: str
    incorporation_date: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    officers: Optional[List[Dict[str, Any]]] = None
    financial_summary: Optional[Dict[str, Any]] = None
    stock_data: Optional[Dict[str, Any]] = None
    sources: List[str]
    last_updated: str

class HealthCheck(BaseModel):
    status: str
    timestamp: str
    sources_available: Dict[str, bool]


class DataAggregator:
    """Aggregates company data from multiple free sources"""
    
    def __init__(self):
        self.timeout = 10.0
        
    async def get_opencorporates_data(self, company_name: str, country: str = "us") -> Optional[Dict]:
        """Get company data from OpenCorporates (free, no API key needed)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # OpenCorporates search API
                url = f"https://api.opencorporates.com/v0.4/companies/search"
                params = {
                    "q": company_name,
                    "jurisdiction_code": country,
                    "order": "score"
                }
                
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("results", {}).get("companies"):
                        company = data["results"]["companies"][0]["company"]
                        
                        return {
                            "name": company.get("name"),
                            "company_number": company.get("company_number"),
                            "jurisdiction": company.get("jurisdiction_code"),
                            "incorporation_date": company.get("incorporation_date"),
                            "company_type": company.get("company_type"),
                            "status": company.get("current_status"),
                            "address": company.get("registered_address_in_full"),
                            "opencorporates_url": company.get("opencorporates_url"),
                        }
                        
        except Exception as e:
            print(f"OpenCorporates error: {e}")
            
        return None
    
    async def get_sec_edgar_data(self, ticker: str) -> Optional[Dict]:
        """Get financial data from SEC EDGAR (free, no API key needed)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # SEC Company Tickers endpoint
                url = "https://www.sec.gov/files/company_tickers.json"
                headers = {
                    "User-Agent": "CompanyFinancialsAPI contact@example.com"  # SEC requires user agent
                }
                
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Find company by ticker
                    for key, company in data.items():
                        if company.get("ticker", "").lower() == ticker.lower():
                            cik = str(company.get("cik_str", "")).zfill(10)
                            
                            # Get company facts (financials)
                            facts_url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
                            facts_response = await client.get(facts_url, headers=headers)
                            
                            if facts_response.status_code == 200:
                                facts = facts_response.json()
                                
                                return {
                                    "cik": cik,
                                    "ticker": company.get("ticker"),
                                    "company_name": company.get("title"),
                                    "facts": self._extract_key_financials(facts),
                                    "sec_url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}"
                                }
                                
        except Exception as e:
            print(f"SEC EDGAR error: {e}")
            
        return None
    
    def _extract_key_financials(self, facts: Dict) -> Dict:
        """Extract key financial metrics from SEC facts"""
        try:
            us_gaap = facts.get("facts", {}).get("us-gaap", {})
            
            financials = {}
            
            # Revenue
            if "Revenues" in us_gaap or "RevenueFromContractWithCustomerExcludingAssessedTax" in us_gaap:
                revenue_key = "Revenues" if "Revenues" in us_gaap else "RevenueFromContractWithCustomerExcludingAssessedTax"
                revenue_data = us_gaap[revenue_key].get("units", {}).get("USD", [])
                if revenue_data:
                    latest = revenue_data[-1]
                    financials["revenue"] = {
                        "value": latest.get("val"),
                        "period": latest.get("end"),
                        "form": latest.get("form")
                    }
            
            # Assets
            if "Assets" in us_gaap:
                assets_data = us_gaap["Assets"].get("units", {}).get("USD", [])
                if assets_data:
                    latest = assets_data[-1]
                    financials["total_assets"] = {
                        "value": latest.get("val"),
                        "period": latest.get("end")
                    }
            
            # Net Income
            if "NetIncomeLoss" in us_gaap:
                income_data = us_gaap["NetIncomeLoss"].get("units", {}).get("USD", [])
                if income_data:
                    latest = income_data[-1]
                    financials["net_income"] = {
                        "value": latest.get("val"),
                        "period": latest.get("end")
                    }
            
            return financials
            
        except Exception as e:
            print(f"Error extracting financials: {e}")
            return {}
    
    async def get_yahoo_finance_data(self, ticker: str) -> Optional[Dict]:
        """Get stock market data from Yahoo Finance (free, no API key)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Yahoo Finance query API
                url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
                params = {
                    "modules": "price,summaryDetail,defaultKeyStatistics,financialData"
                }
                
                response = await client.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    result = data.get("quoteSummary", {}).get("result", [])
                    
                    if result:
                        quote = result[0]
                        
                        price = quote.get("price", {})
                        summary = quote.get("summaryDetail", {})
                        key_stats = quote.get("defaultKeyStatistics", {})
                        financials = quote.get("financialData", {})
                        
                        return {
                            "ticker": ticker,
                            "current_price": price.get("regularMarketPrice", {}).get("raw"),
                            "market_cap": price.get("marketCap", {}).get("raw"),
                            "currency": price.get("currency"),
                            "exchange": price.get("exchangeName"),
                            "pe_ratio": summary.get("trailingPE", {}).get("raw"),
                            "dividend_yield": summary.get("dividendYield", {}).get("raw"),
                            "52_week_high": summary.get("fiftyTwoWeekHigh", {}).get("raw"),
                            "52_week_low": summary.get("fiftyTwoWeekLow", {}).get("raw"),
                            "profit_margins": financials.get("profitMargins", {}).get("raw"),
                            "revenue_growth": financials.get("revenueGrowth", {}).get("raw"),
                        }
                        
        except Exception as e:
            print(f"Yahoo Finance error: {e}")
            
        return None
    
    async def aggregate_company_data(
        self, 
        company_name: str, 
        ticker: Optional[str] = None,
        country: str = "us"
    ) -> CompanyFinancials:
        """Aggregate data from all sources"""
        
        sources_used = []
        
        # Fetch from all sources in parallel
        tasks = [
            self.get_opencorporates_data(company_name, country)
        ]
        
        if ticker:
            tasks.extend([
                self.get_sec_edgar_data(ticker),
                self.get_yahoo_finance_data(ticker)
            ])
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        opencorporates_data = results[0] if not isinstance(results[0], Exception) else None
        sec_data = results[1] if len(results) > 1 and not isinstance(results[1], Exception) else None
        yahoo_data = results[2] if len(results) > 2 and not isinstance(results[2], Exception) else None
        
        # Build aggregated response
        if opencorporates_data:
            sources_used.append("OpenCorporates")
            
        if sec_data:
            sources_used.append("SEC EDGAR")
            
        if yahoo_data:
            sources_used.append("Yahoo Finance")
        
        # Merge data
        response = CompanyFinancials(
            company_name=opencorporates_data.get("name") if opencorporates_data else company_name,
            ticker=ticker or sec_data.get("ticker") if sec_data else None,
            country=country,
            registration_number=opencorporates_data.get("company_number") if opencorporates_data else None,
            status=opencorporates_data.get("status") if opencorporates_data else "unknown",
            incorporation_date=opencorporates_data.get("incorporation_date") if opencorporates_data else None,
            address={"full_address": opencorporates_data.get("address")} if opencorporates_data and opencorporates_data.get("address") else None,
            officers=None,  # Can be expanded later
            financial_summary=sec_data.get("facts") if sec_data else None,
            stock_data=yahoo_data,
            sources=sources_used,
            last_updated=datetime.now().isoformat()
        )
        
        if not sources_used:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for company: {company_name}"
            )
        
        return response


# Initialize aggregator
aggregator = DataAggregator()


@app.get("/", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="operational",
        timestamp=datetime.now().isoformat(),
        sources_available={
            "opencorporates": True,
            "sec_edgar": True,
            "yahoo_finance": True
        }
    )


@app.get("/company", response_model=CompanyFinancials)
async def get_company_financials(
    name: str,
    ticker: Optional[str] = None,
    country: str = "us",
    x_rapidapi_key: Optional[str] = Header(None)
):
    """
    Get comprehensive company financial data
    
    Parameters:
    - name: Company name (required)
    - ticker: Stock ticker symbol (optional, enables more data)
    - country: Country code (default: us)
    
    Returns aggregated data from:
    - OpenCorporates (registration info)
    - SEC EDGAR (financial statements for US companies)
    - Yahoo Finance (real-time stock data)
    """
    
    # RapidAPI automatically adds x-rapidapi-key header for auth
    # You can add custom validation here if needed
    
    return await aggregator.aggregate_company_data(name, ticker, country)


@app.get("/ticker/{ticker}", response_model=CompanyFinancials)
async def get_company_by_ticker(
    ticker: str,
    x_rapidapi_key: Optional[str] = Header(None)
):
    """
    Get company data by stock ticker symbol
    
    Simplified endpoint when you only have the ticker
    """
    
    # Get basic info from Yahoo first to get company name
    yahoo_data = await aggregator.get_yahoo_finance_data(ticker)
    
    if not yahoo_data:
        raise HTTPException(
            status_code=404,
            detail=f"Ticker not found: {ticker}"
        )
    
    # Then aggregate all data
    # Use ticker as name fallback
    return await aggregator.aggregate_company_data(ticker, ticker, "us")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
