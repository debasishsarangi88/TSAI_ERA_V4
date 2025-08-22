// Content script for technology detection
// Runs in the context of the web page to analyze technologies

// Prevent multiple injections
if (window.techDetectorInitialized) {
  console.log('Tech Detector already initialized, skipping...');
} else {
  window.techDetectorInitialized = true;

// Technology detection patterns - Comprehensive list
const TECH_PATTERNS = {
  // JavaScript Frameworks
  'React': {
    category: 'JavaScript Framework',
    patterns: [
      { type: 'global', value: 'React' },
      { type: 'global', value: 'ReactDOM' },
      { type: 'script', value: 'react' },
      { type: 'script', value: 'react-dom' },
      { type: 'script', value: 'react.js' },
      { type: 'script', value: 'react.min.js' },
      { type: 'attribute', selector: '[data-reactroot]' },
      { type: 'attribute', selector: '[data-reactid]' }
    ]
  },
  'Vue.js': {
    category: 'JavaScript Framework',
    patterns: [
      { type: 'global', value: 'Vue' },
      { type: 'script', value: 'vue' },
      { type: 'script', value: 'vue.js' },
      { type: 'script', value: 'vue.min.js' },
      { type: 'attribute', selector: '[data-v-]' },
      { type: 'attribute', selector: '[v-]' }
    ]
  },
  'Angular': {
    category: 'JavaScript Framework',
    patterns: [
      { type: 'global', value: 'angular' },
      { type: 'script', value: 'angular' },
      { type: 'script', value: 'angular.js' },
      { type: 'script', value: 'angular.min.js' },
      { type: 'attribute', selector: '[ng-]' },
      { type: 'attribute', selector: '[data-ng-]' },
      { type: 'attribute', selector: '[x-ng-]' }
    ]
  },
  'Svelte': {
    category: 'JavaScript Framework',
    patterns: [
      { type: 'global', value: 'svelte' },
      { type: 'script', value: 'svelte' },
      { type: 'attribute', selector: '[class*="svelte-"]' }
    ]
  },
  'Next.js': {
    category: 'JavaScript Framework',
    patterns: [
      { type: 'script', value: 'next' },
      { type: 'script', value: '_next' },
      { type: 'link', value: '_next' },
      { type: 'meta', name: 'generator', value: 'next' }
    ]
  },
  'Nuxt.js': {
    category: 'JavaScript Framework',
    patterns: [
      { type: 'script', value: 'nuxt' },
      { type: 'script', value: '_nuxt' },
      { type: 'link', value: '_nuxt' },
      { type: 'meta', name: 'generator', value: 'nuxt' }
    ]
  },
  'Gatsby': {
    category: 'JavaScript Framework',
    patterns: [
      { type: 'script', value: 'gatsby' },
      { type: 'meta', name: 'generator', value: 'gatsby' }
    ]
  },
  'jQuery': {
    category: 'JavaScript Library',
    patterns: [
      { type: 'global', value: 'jQuery' },
      { type: 'global', value: '$' },
      { type: 'script', value: 'jquery' },
      { type: 'script', value: 'jquery.js' },
      { type: 'script', value: 'jquery.min.js' }
    ]
  },
  'Lodash': {
    category: 'JavaScript Library',
    patterns: [
      { type: 'global', value: '_' },
      { type: 'global', value: 'lodash' },
      { type: 'script', value: 'lodash' },
      { type: 'script', value: 'underscore' }
    ]
  },
  'Moment.js': {
    category: 'JavaScript Library',
    patterns: [
      { type: 'global', value: 'moment' },
      { type: 'script', value: 'moment' },
      { type: 'script', value: 'moment.js' }
    ]
  },
  'Axios': {
    category: 'JavaScript Library',
    patterns: [
      { type: 'global', value: 'axios' },
      { type: 'script', value: 'axios' },
      { type: 'script', value: 'axios.min.js' }
    ]
  },
  'Bootstrap': {
    category: 'CSS Framework',
    patterns: [
      { type: 'script', value: 'bootstrap' },
      { type: 'link', value: 'bootstrap' },
      { type: 'link', value: 'bootstrap.css' },
      { type: 'link', value: 'bootstrap.min.css' },
      { type: 'class', value: 'container' },
      { type: 'class', value: 'row' },
      { type: 'class', value: 'col-' },
      { type: 'class', value: 'btn-' },
      { type: 'class', value: 'navbar' },
      { type: 'class', value: 'modal' }
    ]
  },
  'Tailwind CSS': {
    category: 'CSS Framework',
    patterns: [
      { type: 'script', value: 'tailwind' },
      { type: 'link', value: 'tailwind' },
      { type: 'link', value: 'tailwind.css' },
      { type: 'class', value: 'bg-' },
      { type: 'class', value: 'text-' },
      { type: 'class', value: 'p-' },
      { type: 'class', value: 'm-' },
      { type: 'class', value: 'flex' },
      { type: 'class', value: 'grid' }
    ]
  },
  'Foundation': {
    category: 'CSS Framework',
    patterns: [
      { type: 'script', value: 'foundation' },
      { type: 'link', value: 'foundation' },
      { type: 'class', value: 'foundation' },
      { type: 'class', value: 'orbit' }
    ]
  },
  'Bulma': {
    category: 'CSS Framework',
    patterns: [
      { type: 'link', value: 'bulma' },
      { type: 'class', value: 'bulma' },
      { type: 'class', value: 'columns' },
      { type: 'class', value: 'hero' }
    ]
  },
  'Material-UI': {
    category: 'CSS Framework',
    patterns: [
      { type: 'script', value: 'material-ui' },
      { type: 'link', value: 'material-ui' },
      { type: 'class', value: 'Mui' },
      { type: 'class', value: 'mui' }
    ]
  },
  'Ant Design': {
    category: 'CSS Framework',
    patterns: [
      { type: 'script', value: 'antd' },
      { type: 'link', value: 'antd' },
      { type: 'class', value: 'ant-' },
      { type: 'class', value: 'antd' }
    ]
  },
  'WordPress': {
    category: 'CMS',
    patterns: [
      { type: 'meta', name: 'generator', value: 'wordpress' },
      { type: 'script', value: 'wp-' },
      { type: 'link', value: 'wp-' },
      { type: 'link', value: 'wp-content' },
      { type: 'link', value: 'wp-includes' },
      { type: 'meta', name: 'generator', value: 'WordPress' }
    ]
  },
  'Drupal': {
    category: 'CMS',
    patterns: [
      { type: 'meta', name: 'generator', value: 'drupal' },
      { type: 'script', value: 'drupal' },
      { type: 'link', value: 'drupal' },
      { type: 'meta', name: 'generator', value: 'Drupal' }
    ]
  },
  'Joomla': {
    category: 'CMS',
    patterns: [
      { type: 'meta', name: 'generator', value: 'joomla' },
      { type: 'script', value: 'joomla' },
      { type: 'link', value: 'joomla' },
      { type: 'meta', name: 'generator', value: 'Joomla' }
    ]
  },
  'Shopify': {
    category: 'E-commerce',
    patterns: [
      { type: 'script', value: 'shopify' },
      { type: 'global', value: 'Shopify' },
      { type: 'link', value: 'shopify' },
      { type: 'meta', name: 'generator', value: 'shopify' }
    ]
  },
  'WooCommerce': {
    category: 'E-commerce',
    patterns: [
      { type: 'script', value: 'woocommerce' },
      { type: 'link', value: 'woocommerce' },
      { type: 'class', value: 'woocommerce' }
    ]
  },
  'Magento': {
    category: 'E-commerce',
    patterns: [
      { type: 'script', value: 'magento' },
      { type: 'link', value: 'magento' },
      { type: 'meta', name: 'generator', value: 'magento' }
    ]
  },
  'Google Analytics': {
    category: 'Analytics',
    patterns: [
      { type: 'global', value: 'ga' },
      { type: 'global', value: 'gtag' },
      { type: 'global', value: 'google_tag_manager' },
      { type: 'script', value: 'google-analytics' },
      { type: 'script', value: 'gtag' },
      { type: 'script', value: 'analytics' },
      { type: 'script', value: 'ga.js' },
      { type: 'script', value: 'gtag.js' }
    ]
  },
  'Google Tag Manager': {
    category: 'Analytics',
    patterns: [
      { type: 'global', value: 'dataLayer' },
      { type: 'script', value: 'googletagmanager' },
      { type: 'script', value: 'gtm' },
      { type: 'script', value: 'gtm.js' },
      { type: 'noscript', value: 'googletagmanager' }
    ]
  },
  'Facebook Pixel': {
    category: 'Analytics',
    patterns: [
      { type: 'global', value: 'fbq' },
      { type: 'script', value: 'facebook' },
      { type: 'script', value: 'fbevents' },
      { type: 'script', value: 'facebook.net' },
      { type: 'noscript', value: 'facebook' }
    ]
  },
  'Hotjar': {
    category: 'Analytics',
    patterns: [
      { type: 'global', value: 'hj' },
      { type: 'script', value: 'hotjar' },
      { type: 'script', value: 'hotjar.com' }
    ]
  },
  'Mixpanel': {
    category: 'Analytics',
    patterns: [
      { type: 'global', value: 'mixpanel' },
      { type: 'script', value: 'mixpanel' },
      { type: 'script', value: 'mixpanel.com' }
    ]
  },
  'Segment': {
    category: 'Analytics',
    patterns: [
      { type: 'global', value: 'analytics' },
      { type: 'script', value: 'segment' },
      { type: 'script', value: 'segment.com' }
    ]
  },
  'Amplitude': {
    category: 'Analytics',
    patterns: [
      { type: 'global', value: 'amplitude' },
      { type: 'script', value: 'amplitude' },
      { type: 'script', value: 'amplitude.com' }
    ]
  },
  'Cloudflare': {
    category: 'CDN',
    patterns: [
      { type: 'meta', name: 'cf-ray' },
      { type: 'script', value: 'cloudflare' },
      { type: 'link', value: 'cloudflare' },
      { type: 'meta', name: 'server', value: 'cloudflare' }
    ]
  },
  'AWS': {
    category: 'Cloud',
    patterns: [
      { type: 'script', value: 'aws' },
      { type: 'link', value: 'amazonaws' },
      { type: 'link', value: 's3.amazonaws' },
      { type: 'link', value: 'cloudfront' }
    ]
  },
  'Netlify': {
    category: 'Hosting',
    patterns: [
      { type: 'meta', name: 'generator', value: 'netlify' },
      { type: 'script', value: 'netlify' },
      { type: 'link', value: 'netlify' }
    ]
  },
  'Vercel': {
    category: 'Hosting',
    patterns: [
      { type: 'meta', name: 'generator', value: 'vercel' },
      { type: 'script', value: 'vercel' },
      { type: 'link', value: 'vercel' }
    ]
  },
  'Heroku': {
    category: 'Hosting',
    patterns: [
      { type: 'meta', name: 'generator', value: 'heroku' },
      { type: 'script', value: 'heroku' }
    ]
  },
  'Stripe': {
    category: 'Payment',
    patterns: [
      { type: 'global', value: 'Stripe' },
      { type: 'script', value: 'stripe' },
      { type: 'script', value: 'stripe.com' },
      { type: 'link', value: 'stripe' }
    ]
  },
  'PayPal': {
    category: 'Payment',
    patterns: [
      { type: 'global', value: 'paypal' },
      { type: 'script', value: 'paypal' },
      { type: 'script', value: 'paypal.com' },
      { type: 'link', value: 'paypal' }
    ]
  },
  'Square': {
    category: 'Payment',
    patterns: [
      { type: 'script', value: 'square' },
      { type: 'script', value: 'square.com' },
      { type: 'link', value: 'square' }
    ]
  },
  'TypeScript': {
    category: 'Programming Language',
    patterns: [
      { type: 'script', value: 'typescript' },
      { type: 'script', value: '.ts' },
      { type: 'link', value: '.ts' }
    ]
  },
  'GraphQL': {
    category: 'API',
    patterns: [
      { type: 'script', value: 'graphql' },
      { type: 'link', value: 'graphql' },
      { type: 'meta', name: 'generator', value: 'graphql' }
    ]
  },
  'REST API': {
    category: 'API',
    patterns: [
      { type: 'script', value: 'api' },
      { type: 'link', value: 'api' },
      { type: 'meta', name: 'generator', value: 'rest' }
    ]
  }
};

// Technology detector class
class TechnologyDetector {
  constructor() {
    this.detectedTechnologies = new Set();
    this.categories = new Map();
  }

  // Main detection method
  async detectTechnologies() {
    try {
      console.log('Starting technology detection...');
      
      // Run all detection methods
      await Promise.all([
        this.detectGlobalVariables(),
        this.detectScriptTags(),
        this.detectMetaTags(),
        this.detectLinkTags(),
        this.detectAttributes(),
        this.detectClasses()
      ]);

      const results = this.getResults();
      console.log('Detection completed:', results);
      return results;
    } catch (error) {
      console.error('Technology detection error:', error);
      return { technologies: [], categories: new Map(), error: error.message };
    }
  }

  // Detect global JavaScript variables
  async detectGlobalVariables() {
    for (const [techName, tech] of Object.entries(TECH_PATTERNS)) {
      for (const pattern of tech.patterns) {
        if (pattern.type === 'global') {
          if (this.checkGlobalVariable(pattern.value)) {
            this.addTechnology(techName, tech.category);
            break;
          }
        }
      }
    }
  }

  // Check if a global variable exists
  checkGlobalVariable(varName) {
    try {
      return typeof window[varName] !== 'undefined';
    } catch {
      return false;
    }
  }

  // Detect technologies from script tags
  async detectScriptTags() {
    const scripts = document.querySelectorAll('script');
    console.log('Found', scripts.length, 'script tags');
    
    for (const [techName, tech] of Object.entries(TECH_PATTERNS)) {
      for (const pattern of tech.patterns) {
        if (pattern.type === 'script') {
          if (this.checkScriptPattern(scripts, pattern)) {
            console.log('Detected', techName, 'via script pattern:', pattern.value);
            this.addTechnology(techName, tech.category);
            break;
          }
        }
      }
    }
  }

  // Check script tags for patterns
  checkScriptPattern(scripts, pattern) {
    const patternLower = pattern.value.toLowerCase();
    
    for (const script of scripts) {
      const src = script.src || '';
      const content = script.textContent || '';
      
      if (src.toLowerCase().includes(patternLower) ||
          content.toLowerCase().includes(patternLower)) {
        console.log('Script pattern match:', pattern.value, 'in:', src || 'inline script');
        return true;
      }
    }
    return false;
  }

  // Detect technologies from meta tags
  async detectMetaTags() {
    const metas = document.querySelectorAll('meta');
    
    for (const [techName, tech] of Object.entries(TECH_PATTERNS)) {
      for (const pattern of tech.patterns) {
        if (pattern.type === 'meta') {
          if (this.checkMetaPattern(metas, pattern)) {
            this.addTechnology(techName, tech.category);
            break;
          }
        }
      }
    }
  }

  // Check meta tags for patterns
  checkMetaPattern(metas, pattern) {
    for (const meta of metas) {
      const name = meta.getAttribute('name') || '';
      const content = meta.getAttribute('content') || '';
      
      if (name.toLowerCase().includes(pattern.name?.toLowerCase() || '') ||
          content.toLowerCase().includes(pattern.value?.toLowerCase() || '')) {
        return true;
      }
    }
    return false;
  }

  // Detect technologies from link tags
  async detectLinkTags() {
    const links = document.querySelectorAll('link');
    
    for (const [techName, tech] of Object.entries(TECH_PATTERNS)) {
      for (const pattern of tech.patterns) {
        if (pattern.type === 'link') {
          if (this.checkLinkPattern(links, pattern)) {
            this.addTechnology(techName, tech.category);
            break;
          }
        }
      }
    }
  }

  // Check link tags for patterns
  checkLinkPattern(links, pattern) {
    for (const link of links) {
      const href = link.href || '';
      if (href.toLowerCase().includes(pattern.value.toLowerCase())) {
        return true;
      }
    }
    return false;
  }

  // Detect technologies from HTML attributes
  async detectAttributes() {
    for (const [techName, tech] of Object.entries(TECH_PATTERNS)) {
      for (const pattern of tech.patterns) {
        if (pattern.type === 'attribute') {
          if (this.checkAttributePattern(pattern)) {
            this.addTechnology(techName, tech.category);
            break;
          }
        }
      }
    }
  }

  // Check for attribute patterns
  checkAttributePattern(pattern) {
    const elements = document.querySelectorAll(pattern.selector);
    return elements.length > 0;
  }

  // Detect technologies from CSS classes
  async detectClasses() {
    console.log('Checking CSS classes for technology patterns...');
    
    for (const [techName, tech] of Object.entries(TECH_PATTERNS)) {
      for (const pattern of tech.patterns) {
        if (pattern.type === 'class') {
          if (this.checkClassPattern(pattern)) {
            console.log('Detected', techName, 'via CSS class pattern:', pattern.value);
            this.addTechnology(techName, tech.category);
            break;
          }
        }
      }
    }
  }

  // Check for class patterns
  checkClassPattern(pattern) {
    const elements = document.querySelectorAll(`[class*="${pattern.value}"]`);
    if (elements.length > 0) {
      console.log('Found', elements.length, 'elements with class pattern:', pattern.value);
      return true;
    }
    return false;
  }

  // Add detected technology to results
  addTechnology(techName, category) {
    this.detectedTechnologies.add(techName);
    
    if (!this.categories.has(category)) {
      this.categories.set(category, []);
    }
    
    if (!this.categories.get(category).includes(techName)) {
      this.categories.get(category).push(techName);
    }
  }

  // Get final results
  getResults() {
    // Convert Map to regular object for serialization
    const categoriesObj = {};
    for (const [category, technologies] of this.categories) {
      categoriesObj[category] = technologies;
    }
    
    return {
      technologies: Array.from(this.detectedTechnologies),
      categories: categoriesObj,
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString()
    };
  }
}

// Listen for messages from popup (only add once)
if (!window.techDetectorMessageListener) {
  window.techDetectorMessageListener = true;
  
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('Content script received message:', request);
    
    if (request.action === 'detectTechnologies') {
      console.log('Received detection request');
      
      // Check if we already have results from auto-detection
      if (window.techDetectorResults) {
        console.log('Using cached results:', window.techDetectorResults);
        sendResponse(window.techDetectorResults);
        return false; // No async response needed
      }
      
      // Perform fresh detection
      const detector = new TechnologyDetector();
      detector.detectTechnologies().then(results => {
        console.log('Sending fresh results:', results);
        sendResponse(results);
      }).catch(error => {
        console.error('Detection failed:', error);
        sendResponse({ 
          error: error.message, 
          technologies: [], 
          categories: new Map(),
          url: window.location.href,
          title: document.title,
          timestamp: new Date().toISOString()
        });
      });
      return true; // Keep message channel open for async response
    }
    
    return false; // No async response needed
  });
}

// Auto-detect on page load for faster response
console.log('Tech Detector content script loaded');
const detector = new TechnologyDetector();
detector.detectTechnologies().then(results => {
  window.techDetectorResults = results;
  console.log('Auto-detection completed:', results);
  console.log('Total technologies detected:', results.technologies.length);
  console.log('Categories found:', Object.keys(results.categories));
  
  // Log detailed results for debugging
  for (const [category, technologies] of Object.entries(results.categories)) {
    console.log(`Category "${category}":`, technologies);
  }
}).catch(error => {
  console.error('Auto-detection failed:', error);
});

// Add a test function for debugging
window.testTechDetection = function() {
  console.log('=== TECH DETECTION DEBUG ===');
  console.log('Current URL:', window.location.href);
  console.log('Page title:', document.title);
  
  // Log all script sources
  const scripts = document.querySelectorAll('script[src]');
  console.log('Script sources found:', scripts.length);
  scripts.forEach((script, index) => {
    console.log(`Script ${index + 1}:`, script.src);
  });
  
  // Log all link sources
  const links = document.querySelectorAll('link[href]');
  console.log('Link sources found:', links.length);
  links.forEach((link, index) => {
    console.log(`Link ${index + 1}:`, link.href);
  });
  
  // Log all meta tags
  const metas = document.querySelectorAll('meta');
  console.log('Meta tags found:', metas.length);
  metas.forEach((meta, index) => {
    const name = meta.getAttribute('name') || meta.getAttribute('property') || '';
    const content = meta.getAttribute('content') || '';
    if (name || content) {
      console.log(`Meta ${index + 1}:`, { name, content });
    }
  });
  
  // Log global variables
  const globalVars = ['React', 'Vue', 'jQuery', '$', 'angular', 'ga', 'gtag', 'dataLayer', 'fbq'];
  console.log('Global variables check:');
  globalVars.forEach(varName => {
    if (typeof window[varName] !== 'undefined') {
      console.log(`Found global: ${varName}`);
    }
  });
  
  console.log('=== END DEBUG ===');
};

} // End of initialization check
