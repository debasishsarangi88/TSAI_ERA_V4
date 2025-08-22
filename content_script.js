// arXiv Enhancer Content Script
// Handles DOM manipulation and metadata scraping on arXiv abstract pages

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        buttonId: 'arxiv-enhancer-download-btn',
        buttonText: 'Download & Rename',
        buttonClass: 'arxiv-enhancer-btn',
        statusClass: 'arxiv-enhancer-status'
    };

    // Main initialization function
    function init() {
        // Check if we're on an arXiv abstract page
        if (!isArxivAbstractPage()) {
            return;
        }

        // Wait for the page to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', injectDownloadButton);
        } else {
            injectDownloadButton();
        }
    }

    // Check if current page is an arXiv abstract page
    function isArxivAbstractPage() {
        return window.location.href.match(/^https:\/\/arxiv\.org\/abs\/.+$/);
    }

    // Inject the download button into the page
    function injectDownloadButton() {
        // Find the download section
        const downloadSection = document.querySelector('div.full-text ul');
        
        if (!downloadSection) {
            console.warn('arXiv Enhancer: Could not find download section');
            return;
        }

        // Check if button already exists
        if (document.getElementById(CONFIG.buttonId)) {
            return;
        }

        // Create the download button
        const downloadButton = document.createElement('li');
        downloadButton.innerHTML = `
            <a href="#" id="${CONFIG.buttonId}" class="${CONFIG.buttonClass} abs-button">
                ${CONFIG.buttonText}
            </a>
        `;

        // Add click event listener
        downloadButton.addEventListener('click', handleDownloadClick);

        // Insert the button after the PDF link
        const pdfLink = downloadSection.querySelector('a[href*="/pdf/"]');
        if (pdfLink && pdfLink.parentElement) {
            downloadSection.insertBefore(downloadButton, pdfLink.parentElement.nextSibling);
        } else {
            downloadSection.appendChild(downloadButton);
        }

        console.log('arXiv Enhancer: Download button injected successfully');
    }

    // Handle download button click
    async function handleDownloadClick(event) {
        event.preventDefault();
        
        const button = event.target;
        const originalText = button.textContent;
        
        try {
            // Show loading state
            button.textContent = 'Processing...';
            button.disabled = true;

            // Scrape metadata
            const metadata = scrapeMetadata();
            
            if (!metadata) {
                throw new Error('Failed to scrape metadata');
            }

            // Send message to background script
            const response = await chrome.runtime.sendMessage({
                action: 'downloadPaper',
                metadata: metadata
            });

            if (response.success) {
                showStatus('Download started!', 'success');
            } else {
                throw new Error(response.error || 'Download failed');
            }

        } catch (error) {
            console.error('arXiv Enhancer Error:', error);
            showStatus('Error: ' + error.message, 'error');
        } finally {
            // Restore button state
            button.textContent = originalText;
            button.disabled = false;
        }
    }

    // Scrape metadata from the page
    function scrapeMetadata() {
        try {
            // Extract paper ID from URL
            const paperId = extractPaperId();
            if (!paperId) {
                throw new Error('Could not extract paper ID from URL');
            }

            // Extract title
            const titleElement = document.querySelector('h1.title');
            if (!titleElement) {
                throw new Error('Could not find title element');
            }
            let title = titleElement.textContent.trim();
            // Remove "Title:" prefix if present
            title = title.replace(/^Title:\s*/, '');

            // Extract first author's last name
            const authorsElement = document.querySelector('div.authors');
            if (!authorsElement) {
                throw new Error('Could not find authors element');
            }
            const firstAuthor = extractFirstAuthorLastName(authorsElement.textContent);

            // Extract year from dateline
            const datelineElement = document.querySelector('div.dateline');
            if (!datelineElement) {
                throw new Error('Could not find dateline element');
            }
            const year = extractYear(datelineElement.textContent);

            return {
                paperId: paperId,
                title: title,
                firstAuthor: firstAuthor,
                year: year
            };

        } catch (error) {
            console.error('Metadata scraping error:', error);
            return null;
        }
    }

    // Extract paper ID from URL
    function extractPaperId() {
        const match = window.location.pathname.match(/\/abs\/(.+)$/);
        return match ? match[1] : null;
    }

    // Extract first author's last name
    function extractFirstAuthorLastName(authorsText) {
        // Clean up the text and get the first author
        const authors = authorsText
            .replace(/^Authors?:\s*/, '') // Remove "Author:" or "Authors:" prefix
            .split(',')[0] // Get first author
            .trim();

        // Extract last name (everything after the last space)
        const nameParts = authors.split(' ');
        return nameParts[nameParts.length - 1];
    }

    // Extract year from dateline
    function extractYear(datelineText) {
        const yearMatch = datelineText.match(/(\d{4})/);
        return yearMatch ? yearMatch[1] : new Date().getFullYear().toString();
    }

    // Show status message
    function showStatus(message, type = 'info') {
        // Remove existing status messages
        const existingStatus = document.querySelector(`.${CONFIG.statusClass}`);
        if (existingStatus) {
            existingStatus.remove();
        }

        // Create status element
        const statusElement = document.createElement('div');
        statusElement.className = `${CONFIG.statusClass} ${CONFIG.statusClass}--${type}`;
        statusElement.textContent = message;

        // Insert near the download button
        const downloadButton = document.getElementById(CONFIG.buttonId);
        if (downloadButton) {
            downloadButton.parentElement.appendChild(statusElement);
        }

        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (statusElement.parentElement) {
                statusElement.remove();
            }
        }, 3000);
    }

    // Initialize the extension
    init();

})();
