import unittest
import json
from src.bookmark_extractor import ChromeBookmarkExtractor

class TestChromeBookmarkExtractor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup that runs once before all tests
        # Create a sample bookmark file for testing
        cls.sample_bookmark_file = 'path/to/test/bookmark_file.json'
        cls.create_sample_bookmark_file()

    @classmethod
    def create_sample_bookmark_file(cls):
        sample_data = {
            "roots": {
                "bookmark_bar": {
                    "children": [
                        {"type": "url", "name": "Test Bookmark 1", "url": "http://example.com"},
                        {"type": "url", "name": "Test Bookmark 2", "url": "http://example.org"}
                    ]
                }
            }
        }
        with open(cls.sample_bookmark_file, 'w') as file:
            json.dump(sample_data, file)

    def test_find_bookmark_file(self):
        # Test if the bookmark file is found correctly
        extractor = ChromeBookmarkExtractor()
        self.assertEqual(extractor.bookmark_file_path, self.sample_bookmark_file)

    def test_extract_bookmarks(self):
        # Test if bookmarks are extracted correctly
        extractor = ChromeBookmarkExtractor()
        bookmarks = extractor.extract_bookmarks()
        self.assertEqual(len(bookmarks), 2)
        self.assertEqual(bookmarks[0]['name'], 'Test Bookmark 1')
        self.assertEqual(bookmarks[0]['url'], 'http://example.com')

    @classmethod
    def tearDownClass(cls):
        # Clean up that runs once after all tests
        # Delete the sample bookmark file
        os.remove(cls.sample_bookmark_file)

if __name__ == '__main__':
    unittest.main()
