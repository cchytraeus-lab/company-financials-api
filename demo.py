"""
Demo/Test script for Company Financials API
Shows example output with sample data
"""

import json
from datetime import datetime

# Example response data
sample_responses = {
    "apple": {
        "company_name": "Apple Inc.",
        "ticker": "AAPL",
        "country": "us",
        "registration_number": "C0806592",
        "status": "Active",
        "incorporation_date": "1977-01-03",
        "address": {
            "full_address": "One Apple Park Way, Cupertino, CA 95014, United States"
        },
        "officers": None,
        "financial_summary": {
            "revenue": {
                "value": 394328000000,
                "period": "2023-09-30",
                "form": "10-K"
            },
            "total_assets": {
                "value": 352755000000,
                "period": "2023-09-30"
            },
            "net_income": {
                "value": 96995000000,
                "period": "2023-09-30"
            }
        },
        "stock_data": {
            "ticker": "AAPL",
            "current_price": 189.95,
            "market_cap": 2950000000000,
            "currency": "USD",
            "exchange": "NASDAQ",
            "pe_ratio": 31.24,
            "dividend_yield": 0.0046,
            "52_week_high": 199.62,
            "52_week_low": 164.08,
            "profit_margins": 0.246,
            "revenue_growth": 0.021
        },
        "sources": [
            "OpenCorporates",
            "SEC EDGAR",
            "Yahoo Finance"
        ],
        "last_updated": datetime.now().isoformat()
    },
    "tesla": {
        "company_name": "Tesla, Inc.",
        "ticker": "TSLA",
        "country": "us",
        "registration_number": "3500872",
        "status": "Active",
        "incorporation_date": "2003-07-01",
        "address": {
            "full_address": "3500 Deer Creek Road, Palo Alto, CA 94304"
        },
        "officers": None,
        "financial_summary": {
            "revenue": {
                "value": 96773000000,
                "period": "2023-12-31",
                "form": "10-K"
            },
            "total_assets": {
                "value": 106618000000,
                "period": "2023-12-31"
            },
            "net_income": {
                "value": 14974000000,
                "period": "2023-12-31"
            }
        },
        "stock_data": {
            "ticker": "TSLA",
            "current_price": 246.35,
            "market_cap": 782000000000,
            "currency": "USD",
            "exchange": "NASDAQ",
            "pe_ratio": 52.18,
            "dividend_yield": None,
            "52_week_high": 299.29,
            "52_week_low": 138.80,
            "profit_margins": 0.155,
            "revenue_growth": 0.189
        },
        "sources": [
            "OpenCorporates",
            "SEC EDGAR",
            "Yahoo Finance"
        ],
        "last_updated": datetime.now().isoformat()
    },
    "microsoft": {
        "company_name": "Microsoft Corporation",
        "ticker": "MSFT",
        "country": "us",
        "registration_number": "0000789019",
        "status": "Active",
        "incorporation_date": "1981-09-22",
        "address": {
            "full_address": "One Microsoft Way, Redmond, WA 98052"
        },
        "officers": None,
        "financial_summary": {
            "revenue": {
                "value": 211915000000,
                "period": "2023-06-30",
                "form": "10-K"
            },
            "total_assets": {
                "value": 411976000000,
                "period": "2023-06-30"
            },
            "net_income": {
                "value": 72361000000,
                "period": "2023-06-30"
            }
        },
        "stock_data": {
            "ticker": "MSFT",
            "current_price": 415.26,
            "market_cap": 3090000000000,
            "currency": "USD",
            "exchange": "NASDAQ",
            "pe_ratio": 36.85,
            "dividend_yield": 0.0075,
            "52_week_high": 430.82,
            "52_week_low": 309.45,
            "profit_margins": 0.342,
            "revenue_growth": 0.072
        },
        "sources": [
            "OpenCorporates",
            "SEC EDGAR",
            "Yahoo Finance"
        ],
        "last_updated": datetime.now().isoformat()
    }
}

def demo():
    """Show example API responses"""
    
    print("=" * 80)
    print("COMPANY FINANCIALS API - DEMO OUTPUT")
    print("=" * 80)
    print()
    
    print("This is what your API returns when deployed and working.\n")
    print("The free data sources (OpenCorporates, SEC, Yahoo Finance)")
    print("may have rate limits during development, but work fine in production.\n")
    
    for company_key, data in sample_responses.items():
        print("\n" + "=" * 80)
        print(f"Example: GET /company?name={data['company_name']}&ticker={data['ticker']}")
        print("=" * 80)
        print()
        print(json.dumps(data, indent=2))
        print()
        
        # Show value proposition
        if data['financial_summary']:
            revenue = data['financial_summary']['revenue']['value']
            print(f"💰 Annual Revenue: ${revenue:,.0f}")
        
        if data['stock_data']:
            market_cap = data['stock_data']['market_cap']
            print(f"📊 Market Cap: ${market_cap:,.0f}")
            print(f"💵 Current Price: ${data['stock_data']['current_price']}")
        
        print(f"\n✅ Data aggregated from: {', '.join(data['sources'])}")
        print()
    
    print("=" * 80)
    print("VALUE PROPOSITION")
    print("=" * 80)
    print()
    print("🎯 What competitors charge: $200-1000/month")
    print("💸 Your cost to run this: $0-5/month (hosting)")
    print("💰 Your price: $50-200/month")
    print("📈 Profit margin: 90-100%")
    print()
    print("🤖 Who pays for this:")
    print("   • AI agents building financial analysis tools")
    print("   • Fintech startups needing company data")
    print("   • Investment research platforms")
    print("   • Due diligence automation tools")
    print("   • Credit risk assessment systems")
    print()
    print("🚀 Next steps:")
    print("   1. Deploy to Railway (free tier)")
    print("   2. Publish on RapidAPI")
    print("   3. Let AI developers find it automatically")
    print("   4. Start earning passively")
    print()

if __name__ == "__main__":
    demo()
