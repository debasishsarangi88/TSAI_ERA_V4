# Installation Guide - arXiv Enhancer

This guide will help you install the arXiv Enhancer Chrome Extension in developer mode.

## Prerequisites

- Google Chrome browser (version 88 or higher)
- Basic computer skills

## Step-by-Step Installation

### Step 1: Download the Extension

1. Download or clone this repository to your computer
2. Extract the files if you downloaded a ZIP archive
3. Make sure you have all the required files in the extension directory

### Step 2: Open Chrome Extensions Page

1. Open Google Chrome
2. Type `chrome://extensions/` in the address bar
3. Press Enter

### Step 3: Enable Developer Mode

1. Look for the "Developer mode" toggle in the top-right corner of the page
2. Click the toggle to enable Developer mode
3. You should see additional options appear below

### Step 4: Load the Extension

1. Click the "Load unpacked" button that appeared after enabling Developer mode
2. A file dialog will open
3. Navigate to the extension directory (the folder containing `manifest.json`)
4. Select the folder and click "Select Folder"

### Step 5: Grant Permissions

1. Chrome will show a warning about the extension
2. Click "Continue" to proceed
3. The extension should now appear in your extensions list
4. Make sure the toggle next to "arXiv Enhancer" is enabled (blue)

### Step 6: Test the Extension

1. Navigate to any arXiv abstract page (e.g., `https://arxiv.org/abs/1706.03762`)
2. Look for the "Download & Rename" button next to the PDF link
3. Click the button to test the download functionality

## Troubleshooting

### Extension Not Appearing

- Make sure you selected the correct folder (the one containing `manifest.json`)
- Check that all required files are present
- Try refreshing the extensions page

### Extension Not Working on arXiv Pages

- Ensure the extension is enabled (toggle should be blue)
- Check that you're on an arXiv abstract page (`arxiv.org/abs/...`)
- Refresh the page and try again
- Check the browser console for any error messages

### Download Button Not Visible

- Wait for the page to fully load
- Check the browser console for any errors
- Try refreshing the page
- Make sure you're on the correct type of arXiv page

### Permission Errors

- The extension needs permissions to access arXiv.org
- Click "Allow" when prompted for permissions
- If you denied permissions, you may need to reinstall the extension

## Updating the Extension

When you make changes to the extension files:

1. Go to `chrome://extensions/`
2. Find "arXiv Enhancer" in the list
3. Click the refresh icon (🔄) next to the extension
4. The extension will reload with your changes

## Uninstalling the Extension

1. Go to `chrome://extensions/`
2. Find "arXiv Enhancer" in the list
3. Click "Remove" to uninstall the extension
4. Confirm the removal

## File Structure Check

Make sure your extension directory contains these files:

```
arXiv-Enhancer/
├── manifest.json          ✓ Required
├── content_script.js      ✓ Required
├── background.js          ✓ Required
├── options.html           ✓ Required
├── options.js             ✓ Required
├── styles.css             ✓ Required
├── icons/                 ✓ Required (with PNG files)
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
├── README.md              ✓ Documentation
└── INSTALLATION.md        ✓ This file
```

## Getting Help

If you encounter issues:

1. Check the browser console for error messages
2. Verify all files are present and correctly named
3. Try reinstalling the extension
4. Check that you're using a compatible Chrome version

## Security Note

This extension only requests permissions necessary for its functionality:
- Access to arXiv.org pages
- Ability to download files
- Storage for user preferences
- Notifications for download status

The extension does not collect or transmit any personal data.

---

**Need more help?** Check the main README.md file for additional troubleshooting tips.
