import urllib.request
import sys
import os
try:
    from PIL import Image
except ImportError:
    print("Pillow not found, installing...")
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image

def download_image(url, save_path):
    if not os.path.exists(save_path):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(save_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded {save_path}")

def add_watermark(input_path, output_path, watermark_path):
    try:
        base_image = Image.open(input_path).convert("RGBA")
        watermark = Image.open(watermark_path).convert("RGBA")
        
        # Calculate watermark size (e.g., 20% of the image width)
        wm_width = int(base_image.width * 0.2)
        wm_ratio = wm_width / watermark.width
        wm_height = int(watermark.height * wm_ratio)
        watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
        
        # Make watermark semi-transparent if needed, although user logo probably is good as is
        # Adjust opacity
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda p: p * 0.7)
        watermark.putalpha(alpha)

        # Position watermark at bottom-right
        position = (base_image.width - wm_width - 20, base_image.height - wm_height - 20)

        # Create a new transparent image the size of the base image
        transparent = Image.new('RGBA', base_image.size, (0,0,0,0))
        transparent.paste(base_image, (0,0))
        transparent.paste(watermark, position, mask=watermark)
        
        # Convert back to RGB for saving as jpg or keep as PNG
        if output_path.lower().endswith(".jpg") or output_path.lower().endswith(".jpeg"):
            final = transparent.convert("RGB")
            final.save(output_path, "JPEG", quality=95)
        else:
            transparent.save(output_path, "PNG")
        print(f"Watermark added to {output_path}")
    except Exception as e:
        print(f"Error watermarking {input_path}: {e}")

if __name__ == "__main__":
    logo_path = r"C:\Users\lucia\.gemini\antigravity\brain\034a902f-78cb-433e-a3a1-b0d0ee9cc460\media__1772799578712.png"
    
    # Check if there are arguments
    if len(sys.argv) > 1:
        # Process arguments as input-output pairs
        for i in range(1, len(sys.argv), 2):
            if i + 1 < len(sys.argv):
                add_watermark(sys.argv[i], sys.argv[i+1], logo_path)
    else:
        print("Ready to process images. Provide input and output paths as arguments.")
