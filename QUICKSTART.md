# 🎯 Site Evaluation Scoring System - Quick Start Guide

Your complete interactive scoring system is ready!

## ✅ What's Installed

1. **Web Dashboard** - Interactive UI for viewing and managing scores
2. **Automated Scoring Service** - Background process for new submissions
3. **Scoring Engine** - Applies rubric to calculate scores
4. **Google Sheets Integration** - Reads forms, writes scores

## 🚀 How to Use

### Option 1: Web Dashboard (Easiest)

**Terminal Command:**
```bash
/Users/nina/opt/anaconda3/bin/python3 /Users/nina/Desktop/site_data/app.py
```

Or use the starter script:
```bash
bash /Users/nina/Desktop/site_data/start_web.sh
```

**Then open your browser:**
```
http://localhost:5000
```

**Features:**
- View all response scores in cards
- See breakdown by category
- Search by response ID
- Refresh scores from sheets
- Export as JSON

### Option 2: Automated Background Scoring

**Terminal Command:**
```bash
/Users/nina/opt/anaconda3/bin/python3 /Users/nina/Desktop/site_data/auto_scorer.py
```

Or use the starter script:
```bash
bash /Users/nina/Desktop/site_data/start_auto_scorer.sh
```

**What it does:**
- Checks for new form submissions every 5 minutes
- Automatically scores any new responses
- Writes scores to Scores_Summary sheet
- Runs continuously until stopped (Ctrl+C)

### Option 3: Run Both Together

**Terminal 1 (Web Dashboard):**
```bash
/Users/nina/opt/anaconda3/bin/python3 /Users/nina/Desktop/site_data/app.py
```

**Terminal 2 (Auto Scoring):**
```bash
/Users/nina/opt/anaconda3/bin/python3 /Users/nina/Desktop/site_data/auto_scorer.py
```

This gives you:
- Live web interface at `http://localhost:5000`
- Automatic background scoring every 5 minutes
- Real-time sync to Google Sheets

## 📊 Scoring Logic

**Study Capabilities:**
- More enrolling/active studies = higher score
- Range: -10 to +6 points

**Phase Capabilities:**
- Inpatient, PK/PD, Phase 2-4, etc.
- Bonus for special capabilities
- Range: 0 to +8 points

**Key Personnel:**
- Coordinators and investigators
- Certified staff get more points
- Range: -5 to +11 points

**Total Score Example:**
- Response #1 scored: +18 points

## 📁 Project Structure

```
/Users/nina/Desktop/site_data/
├── app.py                    # Flask web app
├── scorer.py                 # Main scoring engine
├── auto_scorer.py            # Background scoring service
├── sheets_connector.py        # Google Sheets API
├── templates/
│   └── index.html           # Web dashboard UI
├── README.md                # Full documentation
├── start_web.sh             # Start web server
├── start_auto_scorer.sh     # Start auto-scorer
└── requirements.txt         # Python dependencies
```

## 🔧 Configuration

All settings are pre-configured:
- API Key: Already set
- Form Spreadsheet: Already linked
- Rubric Spreadsheet: Already linked
- Auto-scorer interval: 5 minutes (change in auto_scorer.py)

## 📋 Google Sheets Connected

**Form Responses:**
- Spreadsheet: Site Evaluation Form
- Sheet: Responses_Raw
- ID: `1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY`

**Scoring Rules:**
- Spreadsheet: Rubric
- Sheet: Auto Scoring Rubric
- ID: `1vLwSqajfazSB8OYBJhK_OEwn2w5xVB-gbTsh_VjBMVI`

**Output:**
- Scores written to: Scores_Summary sheet

## 💡 Tips

1. **Keep both running:** Run web app in one terminal, auto-scorer in another
2. **Check logs:** Both output status messages
3. **Manual refresh:** Click "Refresh" button in web dashboard anytime
4. **Export:** Click "Export" to download scores as JSON
5. **Stop service:** Press Ctrl+C in the terminal

## 🐛 Troubleshooting

**Port 5000 already in use?**
- Edit `app.py`, change port 5000 to another number

**Module import errors?**
```bash
/Users/nina/opt/anaconda3/bin/python3 -m pip install -r /Users/nina/Desktop/site_data/requirements.txt
```

**No scores showing?**
- Click "Refresh" button in web dashboard
- Check that Google Sheets are publicly shared

**Auto-scorer not updating?**
- Check console for error messages
- Verify Google Sheets are accessible

## 📞 Support

All dependencies are installed. To reinstall:
```bash
/Users/nina/opt/anaconda3/bin/python3 -m pip install google-api-python-client flask flask-cors
```

---

**Ready to go!** Choose an option above and start scoring! 🎉
