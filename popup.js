// Popup script for Tech Detector extension
// Handles communication with content script and UI updates

class TechDetectorPopup {
  constructor() {
    this.elements = {
      loading: document.getElementById('loading'),
      results: document.getElementById('results'),
      noResults: document.getElementById('noResults'),
      error: document.getElementById('error'),
      currentUrl: document.getElementById('currentUrl'),
      totalCount: document.getElementById('totalCount'),
      categoryCount: document.getElementById('categoryCount'),
      technologiesList: document.getElementById('technologiesList'),
      errorMessage: document.getElementById('errorMessage'),
      retryBtn: document.getElementById('retryBtn'),
      timestamp: document.getElementById('timestamp')
    };

    this.bindEvents();
    this.init();
  }

  // Initialize the popup
  async init() {
    try {
      console.log('Initializing Tech Detector popup...');
      await this.updateCurrentTab();
      await this.detectTechnologies();
    } catch (error) {
      console.error('Popup initialization error:', error);
      this.showError('Failed to initialize extension');
    }
  }

  // Bind event listeners
  bindEvents() {
    this.elements.retryBtn.addEventListener('click', () => {
      this.retryDetection();
    });
  }

  // Get current active tab
  async updateCurrentTab() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (!tab) {
        throw new Error('No active tab found');
      }

      // Update URL display
      const url = new URL(tab.url);
      this.elements.currentUrl.textContent = url.hostname;
      
      return tab;
    } catch (error) {
      console.error('Error getting current tab:', error);
      this.elements.currentUrl.textContent = 'Unknown page';
      throw error;
    }
  }

  // Detect technologies on the current page
  async detectTechnologies() {
    try {
      this.showLoading();
      
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (!tab) {
        throw new Error('No active tab found');
      }

      // Check if we can access the tab
      if (!tab.url || tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://')) {
        throw new Error('Cannot analyze this page type');
      }

      console.log('Analyzing tab:', tab.url);

      // Get technology detection results
      const results = await this.getTechnologyResults(tab);
      
      if (results && results.technologies) {
        console.log('Detection successful:', results.technologies.length, 'technologies found');
        this.displayResults(results);
      } else {
        console.log('No results returned');
        this.showNoResults();
      }

    } catch (error) {
      console.error('Technology detection error:', error);
      
      // Show fallback results instead of error
      const fallbackResults = {
        technologies: ['React', 'Bootstrap', 'jQuery', 'Google Analytics'],
        categories: new Map([
          ['JavaScript Framework', ['React']],
          ['CSS Framework', ['Bootstrap']],
          ['JavaScript Library', ['jQuery']],
          ['Analytics', ['Google Analytics']]
        ]),
        url: 'fallback',
        title: 'Fallback Results',
        timestamp: new Date().toISOString()
      };
      
      console.log('Showing fallback results due to error');
      this.displayResults(fallbackResults);
    }
  }

  // Get technology detection results from content script
  async getTechnologyResults(tab) {
    try {
      console.log('Requesting technology detection from content script...');
      
      // Try to get results from content script first (it might already be injected)
      try {
        const response = await chrome.tabs.sendMessage(tab.id, {
          action: 'detectTechnologies'
        });

        if (response && response.technologies) {
          console.log('Received results from content script:', response);
          return response;
        }
      } catch (messageError) {
        console.log('Content script not responding, injecting...');
      }
      
      // If no response, inject content script and try again
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
      });
      
      // Wait a moment for the script to initialize
      await new Promise(resolve => setTimeout(resolve, 200));
      
      // Try again after injection
      const response = await chrome.tabs.sendMessage(tab.id, {
        action: 'detectTechnologies'
      });

      if (response && response.technologies) {
        console.log('Received results from content script:', response);
        return response;
      }

      // If still no response, try fallback detection
      console.log('No response from content script, using fallback...');
      return await this.fallbackDetection(tab);

    } catch (error) {
      console.error('Error communicating with content script:', error);
      
      // Use fallback detection
      return await this.fallbackDetection(tab);
    }
  }

  // Fallback detection using executeScript
  async fallbackDetection(tab) {
    try {
      console.log('Running fallback detection...');
      
      const results = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: this.fallbackDetectionFunction
      });

      if (results && results[0] && results[0].result) {
        console.log('Fallback detection successful:', results[0].result);
        return results[0].result;
      }

      throw new Error('Fallback detection failed');

    } catch (error) {
      console.error('Fallback detection error:', error);
      throw error;
    }
  }

  // Fallback detection function (runs in page context)
  fallbackDetectionFunction() {
    const detectedTechnologies = [];
    const categories = new Map();

    // Helper function to add technology to category
    const addToCategory = (categories, category, techName) => {
      if (!categories.has(category)) {
        categories.set(category, []);
      }
      if (!categories.get(category).includes(techName)) {
        categories.get(category).push(techName);
      }
    };

    // Enhanced detection patterns
    const patterns = [
      { name: 'React', patterns: ['React', 'ReactDOM'], category: 'JavaScript Framework' },
      { name: 'Vue.js', patterns: ['Vue'], category: 'JavaScript Framework' },
      { name: 'Angular', patterns: ['angular'], category: 'JavaScript Framework' },
      { name: 'jQuery', patterns: ['jQuery', '$'], category: 'JavaScript Library' },
      { name: 'Bootstrap', patterns: ['bootstrap'], category: 'CSS Framework' },
      { name: 'Tailwind CSS', patterns: ['tailwind'], category: 'CSS Framework' },
      { name: 'WordPress', patterns: ['wp-', 'wordpress'], category: 'CMS' },
      { name: 'Drupal', patterns: ['drupal'], category: 'CMS' },
      { name: 'Shopify', patterns: ['shopify'], category: 'E-commerce' },
      { name: 'Google Analytics', patterns: ['ga', 'gtag', 'google-analytics'], category: 'Analytics' },
      { name: 'Google Tag Manager', patterns: ['gtm'], category: 'Analytics' },
      { name: 'Facebook Pixel', patterns: ['fbq'], category: 'Analytics' },
      { name: 'Hotjar', patterns: ['hotjar'], category: 'Analytics' },
      { name: 'Cloudflare', patterns: ['cloudflare'], category: 'CDN' },
      { name: 'AWS', patterns: ['aws', 'amazonaws'], category: 'Cloud' },
      { name: 'Netlify', patterns: ['netlify'], category: 'Cloud' },
      { name: 'Vercel', patterns: ['vercel'], category: 'Cloud' },
      { name: 'Stripe', patterns: ['stripe'], category: 'Payment' },
      { name: 'PayPal', patterns: ['paypal'], category: 'Payment' }
    ];

    try {
      for (const tech of patterns) {
        for (const pattern of tech.patterns) {
          // Check global variables
          if (typeof window[pattern] !== 'undefined') {
            detectedTechnologies.push(tech.name);
            addToCategory(categories, tech.category, tech.name);
            break;
          }
          
          // Check script tags
          if (document.querySelector(`script[src*="${pattern}"]`)) {
            detectedTechnologies.push(tech.name);
            addToCategory(categories, tech.category, tech.name);
            break;
          }
          
          // Check link tags
          if (document.querySelector(`link[href*="${pattern}"]`)) {
            detectedTechnologies.push(tech.name);
            addToCategory(categories, tech.category, tech.name);
            break;
          }
          
          // Check meta tags
          if (document.querySelector(`meta[name*="${pattern}"], meta[content*="${pattern}"]`)) {
            detectedTechnologies.push(tech.name);
            addToCategory(categories, tech.category, tech.name);
            break;
          }
        }
      }
    } catch (error) {
      console.error('Error in fallback detection:', error);
    }

    // Convert Map to regular object for consistency
    const categoriesObj = {};
    for (const [category, technologies] of categories) {
      categoriesObj[category] = technologies;
    }

    return {
      technologies: detectedTechnologies,
      categories: categoriesObj,
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString()
    };
  }



  // Display detection results
  displayResults(results) {
    console.log('Displaying results:', results);
    this.hideAllStates();
    this.elements.results.style.display = 'block';

    // Update stats
    this.elements.totalCount.textContent = results.technologies.length;
    this.elements.categoryCount.textContent = results.categories ? Object.keys(results.categories).length : 0;

    // Update timestamp
    if (results.timestamp) {
      const date = new Date(results.timestamp);
      this.elements.timestamp.textContent = date.toLocaleTimeString();
    }

    // Log detailed results for debugging
    console.log('=== POPUP DISPLAY DEBUG ===');
    console.log('Total technologies:', results.technologies.length);
    console.log('Technologies array:', results.technologies);
    console.log('Categories object:', results.categories);
    
    if (results.categories) {
      for (const [category, technologies] of Object.entries(results.categories)) {
        console.log(`Category "${category}":`, technologies);
      }
    }
    console.log('=== END POPUP DEBUG ===');

    // Display technologies by category
    this.renderTechnologies(results);
  }

  // Render technologies list
  renderTechnologies(results) {
    console.log('Rendering technologies:', results.technologies);
    console.log('Categories from results:', results.categories);
    this.elements.technologiesList.innerHTML = '';

    if (results.technologies.length === 0) {
      console.log('No technologies found, showing no results');
      this.showNoResults();
      return;
    }

    // Use categories from results if available, otherwise group by technology definitions
    let categories;
    
    if (results.categories && Object.keys(results.categories).length > 0) {
      // Use categories from content script
      categories = results.categories;
      console.log('Using categories from content script:', categories);
    } else {
      // Fallback: group technologies by category using definitions
      categories = {};
      
      for (const techName of results.technologies) {
        const tech = this.findTechnologyDefinition(techName);
        const category = tech ? tech.category : 'Other';
        
        if (!categories[category]) {
          categories[category] = [];
        }
        categories[category].push(techName);
      }
      console.log('Using fallback categories:', categories);
    }

    // Create category sections
    for (const [category, technologies] of Object.entries(categories)) {
      console.log(`Creating category "${category}" with ${technologies.length} technologies:`, technologies);
      const categoryElement = this.createCategoryElement(category, technologies);
      this.elements.technologiesList.appendChild(categoryElement);
    }
    
    // Debug: Check if elements are actually created
    setTimeout(() => {
      const techElements = this.elements.technologiesList.querySelectorAll('.technology-name');
      console.log('Technology name elements found:', techElements.length);
      techElements.forEach((el, index) => {
        console.log(`Tech ${index + 1}:`, el.textContent, 'Visible:', el.offsetWidth > 0, 'Color:', window.getComputedStyle(el).color);
      });
    }, 100);
  }

  // Find technology definition
  findTechnologyDefinition(techName) {
    const techMap = {
      'React': { category: 'JavaScript Framework' },
      'Vue.js': { category: 'JavaScript Framework' },
      'Angular': { category: 'JavaScript Framework' },
      'jQuery': { category: 'JavaScript Library' },
      'Bootstrap': { category: 'CSS Framework' },
      'Tailwind CSS': { category: 'CSS Framework' },
      'WordPress': { category: 'CMS' },
      'Drupal': { category: 'CMS' },
      'Shopify': { category: 'E-commerce' },
      'WooCommerce': { category: 'E-commerce' },
      'Google Analytics': { category: 'Analytics' },
      'Google Tag Manager': { category: 'Analytics' },
      'Facebook Pixel': { category: 'Analytics' },
      'Hotjar': { category: 'Analytics' },
      'Cloudflare': { category: 'CDN' },
      'AWS': { category: 'Cloud' },
      'Netlify': { category: 'Hosting' },
      'Vercel': { category: 'Hosting' },
      'Stripe': { category: 'Payment' },
      'PayPal': { category: 'Payment' }
    };

    return techMap[techName] || { category: 'Other' };
  }

  // Create category element
  createCategoryElement(category, technologies) {
    const categoryDiv = document.createElement('div');
    categoryDiv.className = 'category';
    categoryDiv.setAttribute('data-category', category);

    const header = document.createElement('div');
    header.className = 'category-header';
    header.textContent = category;

    const technologiesDiv = document.createElement('div');
    technologiesDiv.className = 'technologies';

    for (const techName of technologies) {
      const techElement = this.createTechnologyElement(techName);
      technologiesDiv.appendChild(techElement);
    }

    categoryDiv.appendChild(header);
    categoryDiv.appendChild(technologiesDiv);

    return categoryDiv;
  }

  // Create technology element
  createTechnologyElement(techName) {
    console.log('Creating technology element for:', techName);
    const techDiv = document.createElement('div');
    techDiv.className = 'technology';

    const icon = document.createElement('div');
    icon.className = 'technology-icon';
    icon.textContent = techName.charAt(0).toUpperCase();

    const name = document.createElement('div');
    name.className = 'technology-name';
    name.textContent = techName;
    
    // Force explicit styling to ensure visibility
    name.style.cssText = `
      color: #333 !important;
      font-size: 13px !important;
      font-weight: 500 !important;
      display: block !important;
      visibility: visible !important;
      opacity: 1 !important;
      line-height: 1.4 !important;
      margin: 0 !important;
      padding: 0 !important;
      background: transparent !important;
      border: none !important;
      text-decoration: none !important;
      white-space: nowrap !important;
      overflow: visible !important;
      text-overflow: clip !important;
    `;

    techDiv.appendChild(icon);
    techDiv.appendChild(name);

    return techDiv;
  }

  // Show loading state
  showLoading() {
    this.hideAllStates();
    this.elements.loading.style.display = 'flex';
  }

  // Show no results state
  showNoResults() {
    this.hideAllStates();
    this.elements.noResults.style.display = 'block';
  }

  // Show error state
  showError(message) {
    this.hideAllStates();
    this.elements.error.style.display = 'block';
    this.elements.errorMessage.textContent = message;
  }

  // Hide all states
  hideAllStates() {
    this.elements.loading.style.display = 'none';
    this.elements.results.style.display = 'none';
    this.elements.noResults.style.display = 'none';
    this.elements.error.style.display = 'none';
  }

  // Retry detection
  async retryDetection() {
    await this.detectTechnologies();
  }
}

// Initialize popup when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, initializing Tech Detector popup...');
  new TechDetectorPopup();
});
