import io
import unittest
import zipfile

from campaign_app.ui import _build_campaign_zip


class TestCampaignZip(unittest.TestCase):
    def test_build_campaign_zip_contains_four_images(self):
        images = [b"img-1", b"img-2", b"img-3", b"img-4"]
        zip_bytes = _build_campaign_zip(images)

        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as archive:
            names = archive.namelist()
            self.assertEqual(
                names,
                [
                    "shooting_result_1.png",
                    "shooting_result_2.png",
                    "shooting_result_3.png",
                    "shooting_result_4.png",
                ],
            )
            self.assertEqual(archive.read("shooting_result_2.png"), b"img-2")


if __name__ == "__main__":
    unittest.main()

