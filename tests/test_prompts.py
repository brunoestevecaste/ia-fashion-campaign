import json
import re
import unittest

from campaign_core.prompts import build_shoot_prompts_request


class TestPromptsStructure(unittest.TestCase):
    def test_shoot_prompt_contains_valid_json_example(self):
        prompt_text = build_shoot_prompts_request("style", "location")
        match = re.search(
            r"Return ONLY valid JSON using this exact format:\s*(\{[\s\S]*?\})",
            prompt_text,
        )
        self.assertIsNotNone(match)

        template_json = json.loads(match.group(1))
        self.assertIn("prompts", template_json)
        self.assertEqual(len(template_json["prompts"]), 4)
        self.assertEqual(template_json["prompts"][0], "prompt 1")
        self.assertEqual(template_json["prompts"][3], "prompt 4")


if __name__ == "__main__":
    unittest.main()

