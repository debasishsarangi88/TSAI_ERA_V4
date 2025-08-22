// arXiv Enhancer Options Page Script
// Handles user preferences and settings

// Default template
const DEFAULT_TEMPLATE = '{YYYY} - {FirstAuthor} - {Title}';

// Sample metadata for preview
const SAMPLE_METADATA = {
    year: '2017',
    firstAuthor: 'Vaswani',
    title: 'Attention Is All You Need',
    paperId: '1706.03762'
};

// DOM elements
let templateInput;
let previewBox;
let saveButton;
let resetButton;

// Initialize the options page
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    loadSavedTemplate();
    setupEventListeners();
    updatePreview();
});

// Initialize DOM elements
function initializeElements() {
    templateInput = document.getElementById('filenameTemplate');
    previewBox = document.getElementById('filenamePreview');
    saveButton = document.getElementById('saveButton');
    resetButton = document.getElementById('resetButton');
}

// Load saved template from storage
async function loadSavedTemplate() {
    try {
        const result = await chrome.storage.sync.get(['filenameTemplate']);
        const savedTemplate = result.filenameTemplate || DEFAULT_TEMPLATE;
        templateInput.value = savedTemplate;
    } catch (error) {
        console.error('Failed to load saved template:', error);
        templateInput.value = DEFAULT_TEMPLATE;
    }
}

// Setup event listeners
function setupEventListeners() {
    // Update preview on input change
    templateInput.addEventListener('input', updatePreview);
    
    // Save button click
    saveButton.addEventListener('click', saveTemplate);
    
    // Reset button click
    resetButton.addEventListener('click', resetToDefault);
    
    // Save on Enter key
    templateInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            saveTemplate();
        }
    });
}

// Update the preview box with current template
function updatePreview() {
    const template = templateInput.value.trim();
    
    if (!template) {
        previewBox.innerHTML = '<em>Enter a template to see a preview</em>';
        return;
    }
    
    try {
        const preview = generatePreview(template);
        previewBox.textContent = preview;
        previewBox.className = 'preview-box preview-valid';
    } catch (error) {
        previewBox.innerHTML = `<em class="error">Invalid template: ${error.message}</em>`;
        previewBox.className = 'preview-box preview-error';
    }
}

// Generate preview filename from template
function generatePreview(template) {
    // Sanitize the title for preview
    const sanitizedTitle = sanitizeTitle(SAMPLE_METADATA.title);
    
    // Replace placeholders
    let preview = template
        .replace(/{YYYY}/g, SAMPLE_METADATA.year)
        .replace(/{FirstAuthor}/g, SAMPLE_METADATA.firstAuthor)
        .replace(/{Title}/g, sanitizedTitle)
        .replace(/{ID}/g, SAMPLE_METADATA.paperId);
    
    // Ensure it ends with .pdf
    if (!preview.toLowerCase().endsWith('.pdf')) {
        preview += '.pdf';
    }
    
    return preview;
}

// Sanitize title for filename (same as in background.js)
function sanitizeTitle(title) {
    return title
        .replace(/[<>:"/\\|?*]/g, '')
        .replace(/:/g, ' - ')
        .replace(/\s+/g, ' ')
        .trim()
        .substring(0, 100);
}

// Save template to storage
async function saveTemplate() {
    const template = templateInput.value.trim();
    
    if (!template) {
        showMessage('Template cannot be empty', 'error');
        return;
    }
    
    try {
        // Validate template by generating a preview
        generatePreview(template);
        
        // Save to storage
        await chrome.storage.sync.set({
            filenameTemplate: template
        });
        
        showMessage('Settings saved successfully!', 'success');
        
        // Update save button state
        saveButton.textContent = 'Saved!';
        setTimeout(() => {
            saveButton.textContent = 'Save Settings';
        }, 2000);
        
    } catch (error) {
        console.error('Failed to save template:', error);
        showMessage('Failed to save settings: ' + error.message, 'error');
    }
}

// Reset template to default
function resetToDefault() {
    templateInput.value = DEFAULT_TEMPLATE;
    updatePreview();
    showMessage('Reset to default template', 'info');
}

// Show status message
function showMessage(message, type = 'info') {
    // Remove existing messages
    const existingMessage = document.querySelector('.status-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = `status-message status-message--${type}`;
    messageElement.textContent = message;
    
    // Insert after the button group
    const buttonGroup = document.querySelector('.button-group');
    buttonGroup.parentNode.insertBefore(messageElement, buttonGroup.nextSibling);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (messageElement.parentNode) {
            messageElement.remove();
        }
    }, 3000);
}

// Validate template format
function validateTemplate(template) {
    const validPlaceholders = ['{YYYY}', '{FirstAuthor}', '{Title}', '{ID}'];
    const foundPlaceholders = template.match(/\{[^}]+\}/g) || [];
    
    for (const placeholder of foundPlaceholders) {
        if (!validPlaceholders.includes(placeholder)) {
            throw new Error(`Invalid placeholder: ${placeholder}`);
        }
    }
    
    return true;
}
