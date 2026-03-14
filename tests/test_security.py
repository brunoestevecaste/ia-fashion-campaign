import unittest

from campaign_app.security import redact_sensitive_text
from server import is_forbidden_path


class TestSecurity(unittest.TestCase):
    def test_redacts_google_api_key_in_query_string(self):
        text = (
            "HTTPSConnectionPool(host='example.com', port=443): "
            "Max retries exceeded with url: /v1/models/test?key=test-google-api-key-value"
        )
        redacted = redact_sensitive_text(text)

        self.assertNotIn("test-google-api-key-value", redacted)
        self.assertIn("key=[REDACTED]", redacted)

    def test_redacts_authorization_and_api_key_headers(self):
        text = "Authorization: Bearer abc.def.ghi api_key=test-google-api-key-value"
        redacted = redact_sensitive_text(text)

        self.assertNotIn("abc.def.ghi", redacted)
        self.assertNotIn("test-google-api-key-value", redacted)
        self.assertIn("[REDACTED]", redacted)

    def test_marks_dotfiles_and_traversal_as_forbidden_paths(self):
        self.assertTrue(is_forbidden_path("/.streamlit/secrets.toml"))
        self.assertTrue(is_forbidden_path("/../../server.py"))
        self.assertFalse(is_forbidden_path("/index.html"))
        self.assertFalse(is_forbidden_path("/styles.css"))


if __name__ == "__main__":
    unittest.main()
