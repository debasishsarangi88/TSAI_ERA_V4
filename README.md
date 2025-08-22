# arXiv Enhancer

A Chrome Extension that streamlines the process of downloading and managing research papers from arXiv with clean, descriptive filenames.

## Features

### Core Features (v1.0)

- **Smart Download Button**: Automatically injects a "Download & Rename" button on arXiv abstract pages
- **Metadata Scraping**: Extracts paper title, first author's last name, and submission year
- **Custom Filenames**: Downloads papers with descriptive names like `2017 - Vaswani - Attention Is All You Need.pdf`
- **User Configuration**: Customize filename templates through the options page
- **Error Handling**: Graceful error handling with user-friendly notifications

### Advanced Features (Planned for v2.0)

- **Batch Downloading**: Download multiple papers from search results
- **Enhanced Notifications**: System notifications for download status
- **Export/Import Settings**: Backup and restore user preferences

## Installation

### From Source (Developer Mode)

1. **Download the Extension**
   ```bash
   git clone <repository-url>
   cd arXiv-Enhancer
   ```

2. **Load in Chrome**
   - Open Chrome and navigate to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top-right corner)
   - Click "Load unpacked"
   - Select the extension directory

3. **Grant Permissions**
   - The extension will request permissions for arXiv.org
   - Click "Allow" to enable the extension

### From Chrome Web Store (Coming Soon)

The extension will be available on the Chrome Web Store for easy installation.

## Usage

### Basic Usage

1. **Navigate to an arXiv Abstract Page**
   - Go to any arXiv abstract page (e.g., `https://arxiv.org/abs/1706.03762`)
   - Look for the "Download & Rename" button next to the PDF link

2. **Download with Custom Filename**
   - Click the "Download & Rename" button
   - The paper will download with a descriptive filename
   - Example: `2017 - Vaswani - Attention Is All You Need.pdf`

### Customizing Filename Templates

1. **Access Settings**
   - Click the extension icon in Chrome's toolbar
   - Or right-click the extension icon and select "Options"

2. **Configure Template**
   - Use placeholders to create your preferred filename format:
     - `{YYYY}` - Year of submission
     - `{FirstAuthor}` - First author's last name
     - `{Title}` - Paper title (sanitized)
     - `{ID}` - arXiv paper ID

3. **Examples**
   - Default: `{YYYY} - {FirstAuthor} - {Title}`
   - Result: `2017 - Vaswani - Attention Is All You Need.pdf`
   
   - Custom: `{FirstAuthor}_{YYYY}_{Title}`
   - Result: `Vaswani_2017_Attention Is All You Need.pdf`

## File Structure

```
arXiv-Enhancer/
├── manifest.json          # Extension configuration
├── content_script.js      # DOM manipulation and metadata scraping
├── background.js          # Download handling and filename generation
├── options.html           # Settings page interface
├── options.js             # Settings page logic
├── styles.css             # Styling for injected elements and options
├── icons/                 # Extension icons
│   ├── icon16.png
│   ├── icon48.png
│   └── icon128.png
└── README.md              # This file
```

## Technical Details

### Manifest V3 Compliance

The extension uses Chrome's Manifest V3 specification, ensuring compatibility with modern Chrome versions and future updates.

### Permissions

- `activeTab`: Access to the current arXiv tab
- `scripting`: Inject content scripts
- `downloads`: Download files with custom names
- `storage`: Save user preferences
- `notifications`: Show download status notifications
- `host_permissions`: Access to arXiv.org

### Content Script Injection

The extension automatically detects arXiv abstract pages using the URL pattern `https://arxiv.org/abs/*` and injects the download button into the existing download section.

### Metadata Extraction

The extension scrapes the following metadata from arXiv abstract pages:

- **Title**: From `h1.title` element (removes "Title:" prefix)
- **First Author**: From `div.authors` element (extracts last name)
- **Year**: From `div.dateline` element (extracts 4-digit year)
- **Paper ID**: From the URL path

### Filename Sanitization

Titles are automatically sanitized for filesystem compatibility:
- Removes invalid characters: `<>:"/\|?*`
- Replaces colons with hyphens
- Normalizes whitespace
- Limits length to 100 characters

## Development

### Prerequisites

- Chrome browser (version 88+ for Manifest V3)
- Basic knowledge of JavaScript and Chrome Extensions

### Local Development

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd arXiv-Enhancer
   ```

2. **Make Changes**
   - Edit the source files as needed
   - Test changes by reloading the extension in `chrome://extensions/`

3. **Testing**
   - Navigate to arXiv abstract pages to test functionality
   - Check the browser console for any errors
   - Verify download functionality works correctly

### Building for Distribution

1. **Create Icons**
   - Replace placeholder icons in the `icons/` directory
   - Ensure icons are 16x16, 48x48, and 128x128 pixels

2. **Package Extension**
   - Zip all files (excluding development files)
   - Submit to Chrome Web Store for distribution

## Troubleshooting

### Common Issues

**Extension not working on arXiv pages**
- Ensure the extension is enabled in `chrome://extensions/`
- Check that you're on an arXiv abstract page (`arxiv.org/abs/...`)
- Refresh the page and try again

**Download button not appearing**
- Check browser console for errors
- Verify the page has loaded completely
- Try refreshing the page

**Downloads failing**
- Check your browser's download settings
- Ensure you have sufficient disk space
- Verify internet connection

**Template not saving**
- Check browser console for storage errors
- Try resetting to default template
- Clear browser cache and try again

### Debug Mode

Enable debug logging by opening the browser console and looking for messages prefixed with "arXiv Enhancer:".

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Guidelines

- Follow existing code style and conventions
- Add appropriate error handling
- Include comments for complex logic
- Test changes thoroughly before submitting

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for the research community
- Inspired by the need for better paper management
- Thanks to arXiv for providing open access to research papers

## Version History

### v1.0.0 (Current)
- Initial release
- Core download and rename functionality
- User-configurable filename templates
- Options page for settings management
- Manifest V3 compliance

### Planned for v2.0
- Batch downloading from search results
- Enhanced notification system
- Export/import settings
- Additional filename placeholders
- Performance optimizations

---

**Made with ❤️ for researchers**
