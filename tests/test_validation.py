import unittest
from unittest.mock import patch

from campaign_app.models import CampaignInputs
from campaign_app.validation import validate_inputs


def build_inputs(api_key: str) -> CampaignInputs:
    return CampaignInputs(
        api_key=api_key,
        garment_file=object(),
        render_mode="Final",
        style_mode="Preset optimizado",
        style_desc="style",
        location_mode="Preset optimizado",
        location_desc="location",
        model_mode="Preset de descripcion",
        model_desc="model",
        model_image_file=None,
    )


class TestValidation(unittest.TestCase):
    def test_api_key_is_required_when_server_env_is_not_configured(self):
        inputs = build_inputs(api_key="")

        with patch("campaign_app.validation.GEMINI_API_KEY", None):
            missing_fields = validate_inputs(inputs)

        self.assertIn("API key de Google", missing_fields)

    def test_api_key_is_optional_when_server_env_is_configured(self):
        inputs = build_inputs(api_key="")

        with patch("campaign_app.validation.GEMINI_API_KEY", "server-side-key"):
            missing_fields = validate_inputs(inputs)

        self.assertNotIn("API key de Google", missing_fields)


if __name__ == "__main__":
    unittest.main()
