# Site Evaluation Scoring System

Complete solution for scoring clinical research site evaluations with automated processing and interactive web dashboard.

## Features

✓ **Automated Scoring** - Automatically scores Google Form responses based on comprehensive rubric
✓ **Real-time Web Dashboard** - View all scores with interactive cards and filtering
✓ **Auto-Detection** - Detects new form submissions every 30 seconds and scores them automatically
✓ **Google Sheets Integration** - Reads responses and writes scores back to sheets
✓ **Statistics & Analytics** - View category averages, highest/lowest scores
✓ **JSON Export** - Export all scores in JSON format
✓ **Search & Filter** - Find responses by ID or timestamp

## Quick Start

### 1. Start the Web Dashboard

```bash
./start_web.sh
```

Or manually:

```bash
/Users/nina/opt/anaconda3/bin/python3 app.py
```

Then open: **http://localhost:5000**

### 2. Access the API

```bash
# Get all scores
curl http://localhost:5000/api/scores

# Get statistics
curl http://localhost:5000/api/stats

# Refresh scores from Google Sheets
curl -X POST http://localhost:5000/api/refresh

# Get auto-scoring status
curl http://localhost:5000/api/auto-scoring

# Export as JSON
curl http://localhost:5000/api/export > scores.json
```

## How It Works

### Scoring Rules

Scores are calculated based on three categories:

**Study Capabilities**
- Enrolling studies (0 to 10+): -10 to 5 points
- Active studies (0 to 10+): -3 to 1 points

**Phase Capabilities**
- Inpatient capabilities: 0 or 3 points
- PK/PD studies: 0 or 1 points
- Phase 2-4 capable: 0 or 1 points
- High-volume studies (100+): 0 or 1 points
- PBMC processing: 0 or 1 points
- NIH studies: 0 or 1 points

**Key Personnel**
- Total coordinators: 0 to 2 points
- Certified coordinators: 0, 2, or 4 points
- Total investigators: -2 to 2 points
- Active investigators: -3 to 3 points
- Experienced investigators (100+ studies): 0 to 2 points

### Automated Scoring

The system runs a background worker that:
1. Checks for new form submissions every 30 seconds
2. Automatically scores new responses
3. Writes scores back to the `Scores_ItemLevel` sheet
4. Notifies the dashboard of updates

### Data Flow

```
Google Form → Responses_Raw Sheet
    ↓
Scorer Engine (reads all questions)
    ↓
Scoring Rules Applied
    ↓
Results Written to → Scores_ItemLevel Sheet
    ↓
Web Dashboard (http://localhost:5000)
```

## Command Line Scripts

### Score All Responses

```bash
/Users/nina/opt/anaconda3/bin/python3 scorer.py
```

### List Available Sheets

```bash
/Users/nina/opt/anaconda3/bin/python3 list_sheets.py
```

### Fetch Rubric

```bash
/Users/nina/opt/anaconda3/bin/python3 fetch_auto_rubric.py
```

### Test Google Sheets Connection

```bash
/Users/nina/opt/anaconda3/bin/python3 quick_test.py
```

## Configuration

Edit `app.py` to customize:

- **API_KEY**: Your Google API key
- **FORM_SPREADSHEET_ID**: The Google Form responses sheet ID
- **Port**: Change port from 5000 to something else
- **Auto-scoring interval**: Change from 30 seconds to desired interval

## Files

- `app.py` - Flask web application with automated scoring
- `scorer.py` - Scoring engine with rubric rules
- `sheets_connector.py` - Google Sheets API connector
- `templates/index.html` - Web dashboard UI
- `start_web.sh` - Startup script
- `requirements.txt` - Python dependencies

## API Reference

### GET /api/scores
Returns all scored responses

**Response:**
```json
{
  "success": true,
  "count": 1,
  "last_updated": "2026-01-30T...",
  "scores": [...]
}
```

### GET /api/score/<id>
Returns a specific response score

### GET /api/stats
Returns scoring statistics and averages

**Response:**
```json
{
  "success": true,
  "total_responses": 1,
  "average_score": 18,
  "highest_score": 18,
  "lowest_score": 18,
  "category_averages": {
    "Study Capabilities": 2,
    "Phase Capabilities": 5,
    "Key Personnel": 11
  }
}
```

### POST /api/refresh
Manually refresh scores from Google Sheets

### GET /api/auto-scoring
Get auto-scoring status

### POST /api/auto-scoring
Toggle auto-scoring (send JSON: `{"enabled": true/false}`)

### GET /api/export
Export all scores as JSON

## Troubleshooting

**Dashboard shows "No scores available"**
- Click the "Refresh" button to load scores from Google Sheets

**Port 5000 is already in use**
- Edit `app.py` and change `port=5000` to another port (e.g., 5001)
- Or kill the process: `lsof -ti:5000 | xargs kill`

**API Key errors**
- Verify your API_KEY in `app.py` is correct
- Ensure Google Sheets API is enabled in Google Cloud Console

**Scores not updating**
- Check that auto-scoring worker is running (see console output)
- Manually click "Refresh" to force a score calculation

## Next Steps

1. **Customize scoring rules** - Edit the `scoring_rules` dict in `scorer.py`
2. **Add more categories** - Extend the category scoring in `scorer.py`
3. **Create reports** - Add new API endpoints for specific reports
4. **Set up alerts** - Alert when a site scores below/above thresholds
5. **Deploy to cloud** - Use Heroku, AWS, or Google Cloud App Engine

## Contact & Support

For questions about the scoring rubric, refer to:
https://docs.google.com/spreadsheets/d/1vLwSqajfazSB8OYBJhK_OEwn2w5xVB-gbTsh_VjBMVI

Features:
- View all scores in interactive cards
- Search responses by ID or timestamp
- Refresh scores from Google Sheets
- Export scores as JSON
- Real-time category breakdown

### Option 2: Automated Scoring Service

Start the background service:
```bash
/Users/nina/opt/anaconda3/bin/python3 auto_scorer.py
```

This will:
- Monitor Google Forms for new submissions every 5 minutes
- Automatically score new responses
- Write scores to the Scores_Summary sheet
- Run continuously until stopped (Ctrl+C)

### Option 3: Run Scoring Script

Score all responses and display in terminal:
```bash
/Users/nina/opt/anaconda3/bin/python3 scorer.py
```

## Scoring Categories

### Study Capabilities
- Enrolling studies (0-10+): -10 to +5 points
- Active studies (0-10+): -3 to +1 points

### Phase Capabilities
- Inpatient: +3 points
- PK/PD: +1 point
- Phase 2-4: +1 point
- High-volume (100+ patients): +1 point
- PBMC processing: +1 point
- NIH studies: +1 point

### Key Personnel
- Coordinators (0-10+): 0-2 points
- Certified coordinators (0-5): 0-4 points
- Total investigators (1-6+): -2 to +2 points
- Active investigators (0-5+): -3 to +3 points
- Experienced investigators (0-2+): 0-2 points

## API Endpoints

- `GET /` - Web dashboard
- `GET /api/scores` - Get all scores
- `GET /api/score/<id>` - Get specific score
- `POST /api/refresh` - Refresh scores from sheets
- `GET /api/export` - Export all scores as JSON

## Running Multiple Services

You can run both the web app and auto-scorer simultaneously:

**Terminal 1:**
```bash
/Users/nina/opt/anaconda3/bin/python3 app.py
```

**Terminal 2:**
```bash
/Users/nina/opt/anaconda3/bin/python3 auto_scorer.py
```

This gives you:
- Web interface for viewing scores (port 5000)
- Automatic background scoring every 5 minutes
- Continuous sync with Google Sheets

## Troubleshooting

**Module not found errors:**
```bash
/Users/nina/opt/anaconda3/bin/python3 -m pip install -r requirements.txt
```

**Port already in use (for web app):**
Edit `app.py` and change the port number in the last line:
```python
app.run(debug=True, port=5001)  # Change 5000 to any available port
```

**API errors:**
- Ensure spreadsheets are publicly shared
- Verify API key has Google Sheets API enabled
- Check internet connection

## Data Sheets

**Form Data:**
- Spreadsheet: `1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY`
- Sheet: `Responses_Raw`

**Scoring Rubric:**
- Spreadsheet: `1vLwSqajfazSB8OYBJhK_OEwn2w5xVB-gbTsh_VjBMVI`
- Sheet: `Auto Scoring Rubric`

**Output Scores:**
- Written to: `Scores_Summary` in the form responses spreadsheet

## Example Output

```
Response #1:
  Study Capabilities: +2
  Phase Capabilities: +5
  Key Personnel:      +11
  TOTAL:              +18
```

## Support

For issues or feature requests, check:
1. API key validity
2. Google Sheets sharing settings
3. Internet connectivity
4. Python 3.9+ version
