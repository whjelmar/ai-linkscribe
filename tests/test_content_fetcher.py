import unittest
import requests_mock
from src.content_fetcher import ContentFetcher

class TestContentFetcher(unittest.TestCase):

    @requests_mock.Mocker()
    def test_fetch_content_success(self, mock):
        # Mock a successful HTTP response
        mock.get('http://example.com', text='Example Content')
        fetcher = ContentFetcher('http://example.com')
        content = fetcher.fetch_content()
        self.assertEqual(content, 'Example Content')

    @requests_mock.Mocker()
    def test_fetch_content_failure(self, mock):
        # Mock a failed HTTP response
        mock.get('http://example.com', status_code=500)
        fetcher = ContentFetcher('http://example.com')
        content = fetcher.fetch_content()
        self.assertIsNone(content)

    @requests_mock.Mocker()
    def test_fetch_content_with_retry(self, mock):
        # Mock a scenario with a retry (first fail, then succeed)
        mock.get('http://example.com', [{'status_code': 500}, {'text': 'Retried Content'}])
        fetcher = ContentFetcher('http://example.com')
        content = fetcher.fetch_content()
        self.assertEqual(content, 'Retried Content')

# More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
