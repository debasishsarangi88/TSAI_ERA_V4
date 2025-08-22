# Tech Detector Chrome Extension

A highly-performant and lightweight Google Chrome extension that functions like "BuiltWith" or "Wappalyzer" to identify technologies used on web pages.

## Features

### Core Functionality
- **Technology Detection**: Analyzes web pages to identify JavaScript frameworks, libraries, analytics tools, CMS, and server-side technologies
- **High Performance**: Fast, non-blocking analysis using asynchronous operations
- **Lightweight**: Minimal resource usage with clean, modular vanilla JavaScript (ES6+)
- **Real-time Analysis**: Instantly detects technologies when you click the extension icon

### Detected Technologies
- **JavaScript Frameworks**: React, Vue.js, Angular, Svelte, Next.js, Nuxt.js
- **JavaScript Libraries**: jQuery, Lodash, Axios, Moment.js
- **CSS Frameworks**: Bootstrap, Tailwind CSS, Bulma, Foundation
- **CMS**: WordPress, Drupal, Joomla, Shopify
- **Analytics**: Google Analytics, Google Tag Manager, Facebook Pixel, Hotjar
- **E-commerce**: WooCommerce, Shopify, Magento
- **Payment Systems**: Stripe, PayPal, Square
- **Cloud Services**: AWS, Cloudflare, Netlify, Vercel
- **APIs**: GraphQL, REST APIs, WebSocket
- **Build Tools**: Webpack, Vite, Parcel
- **And many more...**

## Installation

### From Source (Developer Mode)

1. **Clone or Download the Extension**
   ```bash
   git clone https://github.com/debasishsarangi88/ERA-V4_Session1.git
   cd ERA-V4_Session1
   ```

2. **Load in Chrome**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top-right corner)
   - Click "Load unpacked"
   - Select the extension directory

3. **Grant Permissions**
   - The extension will request permissions for `activeTab` and `scripting`
   - Click "Allow" to enable the extension

### Create Icons (Required)
Before loading the extension, you need to create the icon files:

1. Open `create-icons.html` in your browser
2. Click the download buttons to generate the PNG icon files
3. Replace the placeholder files in the `icons/` directory

## Usage

### Basic Usage
1. **Navigate to any website** you want to analyze
2. **Click the Tech Detector icon** in your Chrome toolbar
3. **View detected technologies** organized by category
4. **See statistics** including total technologies and categories found

### Testing
Use the included `test-extension.html` file to test the extension with a wide variety of simulated technologies.

## File Structure

```
Tech-Detector/
├── manifest.json          # Extension configuration (Manifest V3)
├── content.js             # Core technology detection logic
├── popup.html             # Extension popup interface
├── popup.css              # Popup styling
├── popup.js               # Popup functionality and communication
├── background.js          # Service worker for coordination
├── create-icons.html      # Icon generation tool
├── test-extension.html    # Comprehensive test page
├── icons/                 # Extension icons (PNG files)
│   ├── icon16.png
│   ├── icon32.png
│   ├── icon48.png
│   └── icon128.png
└── README.md              # This file
```

## Technical Details

### Manifest V3 Compliance
The extension uses Chrome's Manifest V3 specification for modern compatibility and security.

### Permissions
- `activeTab`: Access to the current tab for analysis
- `scripting`: Inject content scripts for technology detection
- `storage`: Save extension settings and cache results

### Detection Methods
The extension uses multiple detection techniques:

1. **Global Variables**: Checks for `window.React`, `window.jQuery`, etc.
2. **Script Tags**: Analyzes `<script>` tag sources and content
3. **Meta Tags**: Examines `<meta>` tags for CMS and framework indicators
4. **Link Tags**: Checks `<link>` tags for CSS frameworks and CDNs
5. **HTML Attributes**: Looks for framework-specific attributes like `[ng-]`, `[data-v-]`
6. **CSS Classes**: Detects framework-specific classes like `container`, `bg-`
7. **HTML Comments**: Searches for technology-specific comments

### Performance Optimizations
- Asynchronous detection using `async/await`
- Efficient DOM queries with `querySelectorAll`
- Parallel processing of detection methods
- Minimal memory footprint
- Event-driven architecture

## Development

### Prerequisites
- Chrome browser (version 88+ for Manifest V3)
- Basic knowledge of JavaScript and Chrome Extensions

### Local Development
1. **Make Changes**: Edit the source files as needed
2. **Test Changes**: Reload the extension in `chrome://extensions/`
3. **Debug**: Use browser console for debugging and testing

### Testing
The extension includes comprehensive testing capabilities:
- `test-extension.html`: Test page with multiple technologies
- Console debugging: Use `window.testTechDetection()` in browser console
- Real-world testing: Test on various websites

## Troubleshooting

### Common Issues

**Extension not working**
- Ensure the extension is enabled in `chrome://extensions/`
- Check browser console for errors
- Verify all icon files are present in the `icons/` directory

**No technologies detected**
- Refresh the page and try again
- Check if the website uses client-side rendering
- Use the test page to verify extension functionality

**Popup not displaying correctly**
- Check for CSS conflicts
- Verify all files are properly loaded
- Clear browser cache and reload extension

### Debug Mode
Enable debug logging by opening the browser console and looking for messages prefixed with "Tech Detector:".

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Guidelines
- Follow existing code style and conventions
- Add appropriate error handling
- Include comments for complex logic
- Test changes thoroughly before submitting

## License

This project is licensed under the MIT License.

## Version History

### v1.0.0 (Current)
- Initial release
- Core technology detection functionality
- Comprehensive technology database
- High-performance detection algorithms
- Clean, responsive UI
- Manifest V3 compliance

### Planned Features
- Technology confidence scores
- Custom detection patterns
- Export detection results
- Batch analysis capabilities
- Enhanced UI with technology icons

---

**Built with ❤️ for developers and tech enthusiasts**

## Acknowledgments

- Inspired by BuiltWith and Wappalyzer
- Built for the developer community
- Thanks to all the open-source technologies that make this possible
