import unittest

from campaign_app.models import CampaignResult
from campaign_app.web_support import (
    InMemoryUpload,
    build_campaign_inputs_from_api_payload,
    build_result_manifest,
    estimate_job_progress,
    guess_mime_type,
)


class TestWebSupport(unittest.TestCase):
    def test_build_campaign_inputs_from_api_payload(self):
        garment_upload = InMemoryUpload(name="garment.png", content=b"garment")
        model_upload = InMemoryUpload(name="model.jpg", content=b"model")
        payload = {
            "apiKey": "AIza-test",
            "renderMode": "Final",
            "styleMode": "Preset optimizado",
            "styleDesc": "style prompt",
            "locationMode": "Prompt personalizado",
            "locationDesc": "location prompt",
            "modelMode": "Subir imagen del modelo",
            "modelDesc": "",
        }

        inputs = build_campaign_inputs_from_api_payload(payload, garment_upload, model_upload)

        self.assertEqual(inputs.api_key, "AIza-test")
        self.assertEqual(inputs.render_mode, "Final")
        self.assertEqual(inputs.style_mode, "Preset optimizado")
        self.assertEqual(inputs.location_mode, "Prompt personalizado")
        self.assertEqual(inputs.model_mode, "Subir imagen del modelo")
        self.assertEqual(inputs.garment_file.name, "garment.png")
        self.assertEqual(inputs.model_image_file.name, "model.jpg")

    def test_build_result_manifest_uses_expected_urls(self):
        result = CampaignResult(
            prompts=["prompt 1", "prompt 2"],
            model_ref_bytes=b"model",
            model_ref_mime="image/png",
            result_images=[b"img-1", b"img-2"],
            zip_bytes=b"zip",
        )

        manifest = build_result_manifest("job123", result)

        self.assertEqual(manifest["modelReferenceUrl"], "/api/campaigns/job123/model-reference")
        self.assertEqual(manifest["downloadZipUrl"], "/api/campaigns/job123/download.zip")
        self.assertEqual(len(manifest["images"]), 2)
        self.assertEqual(manifest["images"][0]["url"], "/api/campaigns/job123/images/1")
        self.assertEqual(manifest["images"][1]["downloadUrl"], "/api/campaigns/job123/images/2?download=1")

    def test_guess_mime_type_supports_expected_extensions(self):
        self.assertEqual(guess_mime_type("look.png"), "image/png")
        self.assertEqual(guess_mime_type("look.webp"), "image/webp")
        self.assertEqual(guess_mime_type("look.jpeg"), "image/jpeg")
        self.assertEqual(guess_mime_type("archive.zip"), "application/zip")

    def test_estimate_job_progress_stays_in_expected_range(self):
        progress = estimate_job_progress(log_count=4, render_mode="Final")
        self.assertGreaterEqual(progress, 8)
        self.assertLessEqual(progress, 94)


if __name__ == "__main__":
    unittest.main()
