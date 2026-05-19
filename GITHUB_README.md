# Company Financials API

Get comprehensive company financial data from multiple free sources.

## What it does

Aggregates data from:
- ✅ SEC EDGAR (financial statements)
- ✅ Yahoo Finance (stock prices)  
- ✅ OpenCorporates (registration data)

**Your cost:** $0  
**Market price:** $200-1000/month  
**Your price:** $50-200/month

## Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

Or manually:

1. Fork this repo
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repo
5. Railway auto-detects Dockerfile and deploys
6. Get your public URL

## Test locally

```bash
pip install -r requirements.txt
python main.py
```

Visit: http://localhost:8000

## API Endpoints

- `GET /` - Health check
- `GET /company?name={name}&ticker={ticker}` - Get company data
- `GET /ticker/{ticker}` - Get company by ticker

## Example

```bash
curl "https://your-api.railway.app/ticker/AAPL"
```

## Monetize on RapidAPI

See [RAPIDAPI_GUIDE.md](RAPIDAPI_GUIDE.md) for complete instructions.

Quick steps:
1. Deploy here on Railway
2. Go to [rapidapi.com/provider](https://rapidapi.com/provider)
3. Add your API with the Railway URL
4. Set pricing and publish
5. Start earning passively

## Revenue Potential

- 100 calls/day = $365/year
- 1,000 calls/day = $3,650/year  
- 10,000 calls/day = $36,500/year

Zero customer support. RapidAPI handles everything.

## License

MIT
