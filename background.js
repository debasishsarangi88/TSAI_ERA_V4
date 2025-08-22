// Background service worker for Tech Detector extension
// Handles extension lifecycle and coordination

// Extension installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Tech Detector extension installed');
  } else if (details.reason === 'update') {
    console.log('Tech Detector extension updated');
  }
});

// Handle extension startup
chrome.runtime.onStartup.addListener(() => {
  console.log('Tech Detector extension started');
});

// Handle messages from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  switch (request.action) {
    case 'getExtensionInfo':
      handleGetExtensionInfo(sendResponse);
      return true; // Keep message channel open for async response
      
    case 'logDetection':
      handleLogDetection(request.data);
      sendResponse({ success: true });
      break;
      
    default:
      sendResponse({ error: 'Unknown action' });
  }
});

// Handle getting extension information
async function handleGetExtensionInfo(sendResponse) {
  try {
    const manifest = chrome.runtime.getManifest();
    
    sendResponse({
      name: manifest.name,
      version: manifest.version,
      description: manifest.description
    });
  } catch (error) {
    console.error('Error getting extension info:', error);
    sendResponse({ error: 'Failed to get extension info' });
  }
}

// Handle logging detection results
function handleLogDetection(data) {
  // Log detection results for debugging
  console.log('Technology detection:', {
    url: data.url,
    technologies: data.technologies,
    timestamp: data.timestamp
  });
}

// Handle tab updates for auto-detection
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && 
      !tab.url.startsWith('chrome://') && 
      !tab.url.startsWith('chrome-extension://')) {
    
    // Auto-detect technologies when page loads
    chrome.tabs.sendMessage(tabId, { action: 'autoDetect' }).catch(() => {
      // Content script might not be ready yet, ignore error
    });
  }
});

// Handle extension icon click (fallback)
chrome.action.onClicked.addListener((tab) => {
  // This is a fallback if popup fails to load
  if (tab.url && !tab.url.startsWith('chrome://') && 
      !tab.url.startsWith('chrome-extension://')) {
    
    // Open popup programmatically
    chrome.action.setPopup({ tabId: tab.id, popup: 'popup.html' });
  }
});

// Service worker keep-alive (for Manifest V3)
setInterval(() => {
  // Keep the service worker alive
}, 25000);
