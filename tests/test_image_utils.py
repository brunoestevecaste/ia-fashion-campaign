import unittest

from campaign_core.image_utils import extract_json


class TestExtractJson(unittest.TestCase):
    def test_extract_json_plain(self):
        payload = '{"prompts": ["a", "b", "c", "d"]}'
        result = extract_json(payload)
        self.assertEqual(result["prompts"], ["a", "b", "c", "d"])

    def test_extract_json_wrapped_text(self):
        payload = (
            "Here is your result:\n"
            '{"prompts": ["prompt 1", "prompt 2", "prompt 3", "prompt 4"]}\n'
            "Thanks"
        )
        result = extract_json(payload)
        self.assertEqual(len(result["prompts"]), 4)

    def test_extract_json_invalid(self):
        with self.assertRaises(ValueError):
            extract_json("No JSON here")


if __name__ == "__main__":
    unittest.main()

