import os
import sys

try:
    from g4f.client import Client
    import g4f.Provider
except Exception as e:
    print(f"Failed to import g4f: {e}")
    sys.exit(1)

def test_generate_image():
    client = Client()
    print("Requesting image from g4f...")
    try:
        response = client.images.generate(
            model="flux",
            prompt="Ultra realistic 8k photo of a professional maid polishing a spotless dark marble kitchen island, bright natural sunlight, pristine high-end home, photorealistic, no text.",
            provider=g4f.Provider.HuggingFace,
            response_format="url"
        )
        image_url = response.data[0].url
        print(f"Successfully generated image URL: {image_url}")
        
        import urllib.request
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as res, open("test_g4f.jpg", 'wb') as f:
            f.write(res.read())
        print("Downloaded to test_g4f.jpg")
    except Exception as e:
        print(f"Failed to generate: {e}")

if __name__ == "__main__":
    test_generate_image()
