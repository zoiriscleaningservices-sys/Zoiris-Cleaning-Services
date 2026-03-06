import os
import sys
import time
import urllib.request
import random

try:
    from PIL import Image
except ImportError:
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image

def download_image(url, save_path):
    if not os.path.exists(save_path):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as response:
                content = response.read()
                if len(content) < 1000: # Probably an error page
                    return False
                with open(save_path, 'wb') as out_file:
                    out_file.write(content)
            print(f"Downloaded {save_path}")
            return True
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return False
    return True

def add_watermark(input_path, output_path, watermark_path):
    try:
        base_image = Image.open(input_path).convert("RGBA")
        watermark = Image.open(watermark_path).convert("RGBA")
        
        # Calculate watermark size (15% of the image width)
        wm_width = int(base_image.width * 0.15)
        wm_ratio = wm_width / watermark.width
        wm_height = int(watermark.height * wm_ratio)
        watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
        
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda p: p * 0.7)
        watermark.putalpha(alpha)

        # Position watermark at bottom-right
        position = (base_image.width - wm_width - 20, base_image.height - wm_height - 20)

        transparent = Image.new('RGBA', base_image.size, (0,0,0,0))
        transparent.paste(base_image, (0,0))
        transparent.paste(watermark, position, mask=watermark)
        
        final = transparent.convert("RGB")
        final.save(output_path, "JPEG", quality=95)
        print(f"Watermark added to {output_path}")
        return True
    except Exception as e:
        print(f"Error watermarking {input_path}: {e}")
        return False

if __name__ == "__main__":
    logo_path = r"C:\Users\lucia\.gemini\antigravity\brain\034a902f-78cb-433e-a3a1-b0d0ee9cc460\media__1772799578712.png"
    output_dir = "images/bulk"
    os.makedirs(output_dir, exist_ok=True)
    
    keywords = ["house,cleaning", "luxury,home", "maid,cleaning", "clean,kitchen", "clean,bathroom", "modern,living,room", "vacuum", "mop"]
    
    count = 1
    while count <= 40:
        kw = random.choice(keywords)
        url = f"https://loremflickr.com/1600/900/{kw}?random={count}"
        temp_path = f"{output_dir}/raw_{count}.jpg"
        final_path = f"{output_dir}/zoiris_service_{count}.jpg"
        
        print(f"Fetching image {count}/40 ({kw})...")
        if download_image(url, temp_path):
            add_watermark(temp_path, final_path, logo_path)
            if os.path.exists(temp_path):
                os.remove(temp_path)
            count += 1
            
        time.sleep(1)
            
    print("Finished generating 40 bulk images.")
