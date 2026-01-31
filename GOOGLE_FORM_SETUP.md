# Google Form URL Configuration

To enable "View Raw" links to the Google Form in the dashboard, you need to add your form URL to the configuration.

## How to Find Your Google Form URL

1. Open your Google Form in a web browser
2. Click the **Send** button (top right)
3. Copy the URL shown in the "Link" section
4. It will look something like: `https://docs.google.com/forms/d/e/1FAIpQLSd_xxxxxxxxxx/viewform`

## How to Update the Configuration

### Option 1: Update app.py directly (Simple)

1. Open `app.py` in your editor
2. Find this line (around line 19):
   ```python
   GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSd_Abc123XYZ/viewform'  # Replace with your form URL
   ```
3. Replace the URL with your actual Google Form URL
4. Save the file
5. Restart the web server: `./start_web.sh`

### Example:
If your form URL is `https://docs.google.com/forms/d/e/1FAIpQLSd_abc123xyz789/viewform`, update it to:
```python
GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSd_abc123xyz789/viewform'
```

## What This Does

Once configured, each response in the dashboard will show a **"📋 View Raw"** button that links directly to your Google Form. This allows you to:
- Review the original form submission
- See all the raw data entered
- Access any attachments or supporting documents

The link appears in two places:
1. On each individual score card in the "Individual Scores" tab
2. On each evaluation in the "Site Detail" view when viewing a specific clinical site

## Notes

- The same form URL will be used for all responses (they all go to the same form)
- The link opens in a new tab
- Make sure the form is shared with the appropriate people before sharing dashboard links
