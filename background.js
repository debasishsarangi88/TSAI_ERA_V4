// arXiv Enhancer Background Service Worker
// Handles download logic and filename generation

// Default filename template
const DEFAULT_TEMPLATE = '{YYYY} - {FirstAuthor} - {Title}';

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'downloadPaper') {
        handleDownloadRequest(message.metadata)
            .then(result => sendResponse(result))
            .catch(error => sendResponse({ success: false, error: error.message }));
        
        return true; // Keep the message channel open for async response
    }
});

// Handle download request
async function handleDownloadRequest(metadata) {
    try {
        // Get user's filename template from storage
        const template = await getUserTemplate();
        
        // Generate filename
        const filename = generateFilename(metadata, template);
        
        // Construct PDF URL
        const pdfUrl = `https://arxiv.org/pdf/${metadata.paperId}.pdf`;
        
        // Initiate download
        const downloadId = await chrome.downloads.download({
            url: pdfUrl,
            filename: filename,
            saveAs: false
        });
        
        // Show notification
        showDownloadNotification(filename);
        
        return { success: true, downloadId: downloadId };
        
    } catch (error) {
        console.error('Download error:', error);
        throw error;
    }
}

// Get user's filename template from storage
async function getUserTemplate() {
    try {
        const result = await chrome.storage.sync.get(['filenameTemplate']);
        return result.filenameTemplate || DEFAULT_TEMPLATE;
    } catch (error) {
        console.warn('Failed to get template from storage, using default:', error);
        return DEFAULT_TEMPLATE;
    }
}

// Generate filename from metadata and template
function generateFilename(metadata, template) {
    // Sanitize the title for filename use
    const sanitizedTitle = sanitizeTitle(metadata.title);
    
    // Replace placeholders in template
    let filename = template
        .replace(/{YYYY}/g, metadata.year)
        .replace(/{FirstAuthor}/g, metadata.firstAuthor)
        .replace(/{Title}/g, sanitizedTitle)
        .replace(/{ID}/g, metadata.paperId);
    
    // Ensure filename ends with .pdf
    if (!filename.toLowerCase().endsWith('.pdf')) {
        filename += '.pdf';
    }
    
    return filename;
}

// Sanitize title for use in filename
function sanitizeTitle(title) {
    return title
        // Replace invalid filename characters
        .replace(/[<>:"/\\|?*]/g, '') // Remove invalid characters
        .replace(/:/g, ' - ') // Replace colons with hyphens
        .replace(/\s+/g, ' ') // Normalize whitespace
        .trim()
        // Limit length to avoid filesystem issues
        .substring(0, 100);
}

// Show download notification
function showDownloadNotification(filename) {
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png',
        title: 'arXiv Enhancer',
        message: `Downloading: ${filename}`
    });
}

// Handle installation
chrome.runtime.onInstalled.addListener((details) => {
    if (details.reason === 'install') {
        // Set default template on first install
        chrome.storage.sync.set({
            filenameTemplate: DEFAULT_TEMPLATE
        });
        
        console.log('arXiv Enhancer installed with default template');
    }
});

// Handle download completion
chrome.downloads.onChanged.addListener((downloadDelta) => {
    if (downloadDelta.state && downloadDelta.state.current === 'complete') {
        // Download completed successfully
        console.log('Download completed:', downloadDelta.id);
    } else if (downloadDelta.error) {
        // Download failed
        console.error('Download failed:', downloadDelta.error);
        
        // Show error notification
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icons/icon48.png',
            title: 'arXiv Enhancer - Download Error',
            message: 'Failed to download paper. Please try again.'
        });
    }
});
