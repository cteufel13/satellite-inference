import requests
from PIL import Image
from io import BytesIO


class ImageRetriever:
    def __init__(self, bearer_token: str = None):

        self.url = "https://sh.dataspace.copernicus.eu/api/v1/process"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        }

    def get_image(
        self,
        bounding_box: list,
        start_date: str,
        end_date: str,
        width: int = 353,
        height: int = 541,
    ) -> Image:

        payload = {
            "input": {
                "bounds": {"bbox": bounding_box},
                "data": [
                    {
                        "dataFilter": {
                            "timeRange": {
                                "from": start_date,
                                "to": end_date,
                            }
                        },
                        "type": "sentinel-2-l2a",
                    }
                ],
            },
            "output": {
                "width": width,
                "height": height,
                "responses": [
                    {"identifier": "default", "format": {"type": "image/jpeg"}}
                ],
            },
            "evalscript": '//VERSION=3\n\nfunction setup() {\n  return {\n    input: ["B02", "B03", "B04"],\n    output: { bands: 3 }\n  };\n}\n\nfunction evaluatePixel(sample) {\n  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];\n}',
        }
        print("Payload:", payload)
        response = requests.post(self.url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(
                f"Error retrieving image: {response.status_code} - {response.text}"
            )

        img_data = response.content
        img = Image.open(BytesIO(img_data))
        return img
