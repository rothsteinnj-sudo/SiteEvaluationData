# Site Evaluation System - Complete Setup Summary

## ✓ What's Been Created

### 1. **Scoring Engine** (`scorer.py`)
- Reads form responses from Google Sheets
- Applies scoring rubric for 3 categories:
  - Study Capabilities
  - Phase Capabilities
  - Key Personnel
- Detailed point calculations per question
- Test response score: **18 points**

### 2. **Web Dashboard** (`app.py` + `templates/index.html`)
- Interactive dashboard at `http://localhost:5000`
- View all responses with scores
- Search and filter by response ID/timestamp
- Export scores to JSON
- Real-time statistics (average, high, low scores)
- Beautiful responsive card layout

### 3. **Automated Scoring**
- Background worker checks every 30 seconds
- Auto-detects new form submissions
- Automatically scores new responses
- Writes scores back to `Scores_ItemLevel` sheet

### 4. **Google Sheets Integration**
- Reads from: `Responses_Raw` sheet
- Writes to: `Scores_ItemLevel` sheet
- API Key authentication (read-only API)
- Spreadsheet IDs hardcoded in configuration

### 5. **Command Line Tools**
- `scorer.py` - Score all responses
- `list_sheets.py` - Browse available sheets
- `fetch_auto_rubric.py` - View the rubric
- `quick_test.py` - Test API connection
- `sheets_connector.py` - Reusable API connector

## 🚀 How to Use

### Start the Web Dashboard
```bash
cd /Users/nina/Desktop/site_data
./start_web.sh
```

Then open: **http://localhost:5000**

### Features in Dashboard
- ✓ See all scored responses
- ✓ View breakdown by category
- ✓ Search responses
- ✓ Export all scores as JSON
- ✓ Refresh to load new submissions
- ✓ Real-time statistics

## 📊 Scoring Structure

### Study Capabilities (0-7 points)
- Enrolling studies: -10 to +5
- Active studies: -3 to +1

### Phase Capabilities (0-9 points)
- Inpatient: +3
- PK/PD: +1
- Phase 2-4: +1
- High-volume: +1
- PBMC: +1
- NIH: +1

### Key Personnel (0+ points)
- Coordinators: 0-2
- Certified: 0-4
- Total Investigators: -2 to +2
- Active Investigators: -3 to +3
- Experienced: 0-2

## 🔧 Configuration

All settings are in `app.py`:
```python
API_KEY = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
FORM_SPREADSHEET_ID = '1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY'
```

## 📡 API Endpoints

```bash
# Get all scores
curl http://localhost:5000/api/scores

# Get statistics
curl http://localhost:5000/api/stats

# Manually refresh
curl -X POST http://localhost:5000/api/refresh

# Export as JSON
curl http://localhost:5000/api/export > scores.json

# Get auto-scoring status
curl http://localhost:5000/api/auto-scoring

# Toggle auto-scoring
curl -X POST http://localhost:5000/api/auto-scoring \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
```

## 📁 Project Files

```
/Users/nina/Desktop/site_data/
├── app.py                          # Flask web app (WITH auto-scoring)
├── scorer.py                       # Scoring engine (UPDATED)
├── sheets_connector.py             # API connector
├── quick_test.py                   # Test connection
├── list_sheets.py                  # Browser sheets
├── fetch_auto_rubric.py           # View rubric
├── start_web.sh                    # Startup script (UPDATED)
├── templates/
│   └── index.html                 # Dashboard UI (ENHANCED)
├── requirements.txt               # Dependencies
└── README.md                       # Documentation (UPDATED)
```

## ✅ What's Automated

1. **Auto-Detection**: Every 30 seconds, checks for new form submissions
2. **Auto-Scoring**: New responses are automatically scored
3. **Auto-Write**: Scores written to `Scores_ItemLevel` sheet
4. **Auto-Notify**: Dashboard shows updated timestamp
5. **Auto-Refresh**: Can be triggered from dashboard or API

## 🎯 Next Steps

1. **Start the dashboard**: `./start_web.sh`
2. **Submit test form**: Add response to Google Form
3. **Watch it auto-score**: Within 30 seconds you'll see it appear
4. **Export results**: Use "Export" button or API

## 🐛 Troubleshooting

**Port 5000 in use?**
```bash
lsof -ti:5000 | xargs kill -9
# Or change port in app.py: app.run(port=5001)
```

**Scores not updating?**
- Click "Refresh" button in dashboard
- Check console for errors
- Verify API key is correct

**No scores showing?**
- Make sure Google Sheet is shared publicly
- Check spreadsheet IDs in app.py
- Run `python3 quick_test.py` to test connection

## 📞 URLs & References

- **Dashboard**: http://localhost:5000
- **API Docs**: http://localhost:5000/api/scores
- **Scoring Rubric**: https://docs.google.com/spreadsheets/d/1vLwSqajfazSB8OYBJhK_OEwn2w5xVB-gbTsh_VjBMVI
- **Form Data**: https://docs.google.com/spreadsheets/d/1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY

---

**Created**: January 30, 2026
**Status**: ✅ Ready to Deploy
