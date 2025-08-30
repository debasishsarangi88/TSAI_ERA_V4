import browser_cookie3
import yt_dlp
import os
import tempfile

def download_with_browser_cookies(url, output_path):
    """
    Download YouTube video using browser cookies to bypass bot detection
    """
    try:
        print(f"Attempting download with browser cookies: {url}")
        
        # Get cookies from Chrome/Firefox
        try:
            cookies = browser_cookie3.chrome(domain_name='.youtube.com')
            print("Using Chrome cookies")
        except:
            try:
                cookies = browser_cookie3.firefox(domain_name='.youtube.com')
                print("Using Firefox cookies")
            except:
                print("No browser cookies found")
                return False
        
        # Create temporary cookie file
        cookie_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        
        # Write cookies to file
        for cookie in cookies:
            cookie_file.write(f"{cookie.domain}\tTRUE\t{cookie.path}\t"
                            f"{'TRUE' if cookie.secure else 'FALSE'}\t{cookie.expires}\t"
                            f"{cookie.name}\t{cookie.value}\n")
        cookie_file.close()
        
        # Configure yt-dlp with cookies
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio',
            'outtmpl': output_path,
            'cookiefile': cookie_file.name,
            'quiet': False,
            'no_check_certificate': True,
            'extractor_retries': 5,
            'retries': 5,
        }
        
        print("Downloading with cookies...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Clean up cookie file
        os.unlink(cookie_file.name)
        
        # Check if download succeeded
        for ext in ['.m4a', '.webm', '.mp3', '.wav']:
            test_path = output_path + ext
            if os.path.exists(test_path):
                print(f"Successfully downloaded: {test_path}")
                return True
        
        print("Download completed but no file found")
        return False
        
    except Exception as e:
        print(f"Error with browser cookies: {e}")
        return False

# Test the function
if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = download_with_browser_cookies(test_url, "/tmp/test_audio")
    print(f"Download result: {result}")
