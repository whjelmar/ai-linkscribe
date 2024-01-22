import json
import os

class ChromeBookmarkExtractor:
    def __init__(self):
        self.bookmark_file_path = self.find_bookmark_file()

    def find_bookmark_file(self):
        # Path to Chrome's default bookmark file location varies by OS
        # Example for Windows:
        path = os.path.join(os.getenv('LOCALAPPDATA'), 
                            'Google', 'Chrome', 'User Data', 'Default', 'Bookmarks')
        # Add paths for other OS (Mac, Linux) here
        if os.path.exists(path):
            return path
        else:
            raise FileNotFoundError("Chrome bookmark file not found.")

    def extract_bookmarks(self):
        # Read the bookmark file and parse the JSON
        with open(self.bookmark_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return self.parse_bookmarks(data['roots'])

    def parse_bookmarks(self, bookmark_data):
        # Recursively parse the bookmark data
        bookmarks = []
        for key, value in bookmark_data.items():
            if key == 'bookmark_bar' or key == 'other' or key == 'synced':
                bookmarks.extend(self.parse_folder(value))
        return bookmarks

    def parse_folder(self, folder):
        # Extract bookmarks from a folder
        bookmarks = []
        for item in folder['children']:
            if item['type'] == 'url':
                bookmarks.append({'name': item['name'], 'url': item['url']})
            elif item['type'] == 'folder':
                bookmarks.extend(self.parse_folder(item))
        return bookmarks
    
def get_bookmark_extractor(browser_type):
    if browser_type == 'chrome':
        return ChromeBookmarkExtractor()
    elif browser_type == 'firefox':
        return FirefoxBrowserExtractor()
    # Add other browsers as needed


# Example usage
# extractor = ChromeBookmarkExtractor()
extractor = get_bookmark_extractor('chrome')
bookmarks = extractor.extract_bookmarks()
print(bookmarks)
