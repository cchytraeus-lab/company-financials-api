# Company Financials API 💰

**Passive income API that aggregates free data sources and sells access on RapidAPI.**

## What It Does

Provides comprehensive company financial data by combining:
- ✅ SEC EDGAR (financial statements)
- ✅ Yahoo Finance (stock prices)
- ✅ OpenCorporates (registration data)

**Your cost:** $0 (all sources free)  
**Market price:** $200-1000/month  
**Your price:** $50-200/month  
**Profit margin:** 100%

## Quick Start (Local Testing)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python main.py
```

API runs at: `http://localhost:8000`

## Test It

```bash
# Get Apple Inc. financials
curl "http://localhost:8000/company?name=Apple&ticker=AAPL"

# Get Tesla by ticker
curl "http://localhost:8000/ticker/TSLA"

# Health check
curl "http://localhost:8000/"
```

## Deploy & Monetize

**See [RAPIDAPI_GUIDE.md](RAPIDAPI_GUIDE.md) for complete instructions.**

Quick version:
1. Push to GitHub
2. Deploy to Railway (free, 10 min)
3. Publish on RapidAPI (free, 10 min)
4. Start earning passively

## Example Response

```json
{
  "company_name": "Apple Inc.",
  "ticker": "AAPL",
  "country": "us",
  "status": "active",
  "incorporation_date": "1977-01-03",
  "financial_summary": {
    "revenue": {
      "value": 394328000000,
      "period": "2023-09-30"
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
    "current_price": 189.95,
    "market_cap": 2950000000000,
    "pe_ratio": 31.2,
    "52_week_high": 199.62,
    "52_week_low": 164.08
  },
  "sources": ["OpenCorporates", "SEC EDGAR", "Yahoo Finance"],
  "last_updated": "2026-05-19T22:15:30.123456"
}
```

## API Endpoints

### GET /company
Get company data by name
- `name` (required) - Company name
- `ticker` (optional) - Stock ticker for more data
- `country` (optional) - Country code, default "us"

### GET /ticker/{ticker}
Get company data by stock ticker
- `ticker` (required) - Stock ticker symbol (AAPL, TSLA, etc)

### GET /
Health check

## Revenue Potential

**100 calls/day** at $0.01/call = **$365/year**  
**1,000 calls/day** = **$3,650/year**  
**10,000 calls/day** = **$36,500/year**

Zero customer support. RapidAPI handles everything.

## Scale Strategy

1. Launch this API on RapidAPI
2. Use `api_opportunity_finder.py` to find next opportunity
3. Build next API (Email Verification is easiest)
4. Repeat until you have 10-20 APIs
5. Each earning $500-2000/month passively

**Total passive income target: $10k-30k/month**

## Next APIs to Build

Priority order (from opportunity finder):
1. Email Verification API - 1-2 days, easy
2. Social Media Data API - 3-7 days
3. SERP/Search Results API - 3-7 days

## Tech Stack

- FastAPI (Python web framework)
- httpx (async HTTP client)
- Pydantic (data validation)
- Docker (containerization)

## Legal

All data sources are public and free to use. No Terms of Service violations.

## Questions?

Read the full [RAPIDAPI_GUIDE.md](RAPIDAPI_GUIDE.md) for step-by-step deployment and monetization.
