import os
import sys
import time
import urllib.request
from duckduckgo_search import DDGS

try:
    from PIL import Image
except ImportError:
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image

def download_image(url, save_path):
    if not os.path.exists(save_path):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read()
                if len(content) < 5000: # Ensure it's not a tiny error page
                    return False
                with open(save_path, 'wb') as out_file:
                    out_file.write(content)
            
            # Verify it's an actual image
            try:
                img = Image.open(save_path)
                img.verify()
            except Exception:
                os.remove(save_path)
                return False
                
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
    output_dir = "images/real_clean"
    os.makedirs(output_dir, exist_ok=True)
    
    queries = [
        "luxury modern living room sparkling clean wide shot",
        "professional maid cleaning luxury kitchen marble counter",
        "spotless shiny modern bathroom glass shower",
        "clean organized office desk corporate bright",
        "premium green cleaning supplies caddy hardwood floor"
    ]
    
    count = 1
    with DDGS() as ddgs:
        for query in queries:
            print(f"Searching images for: {query}")
            results = ddgs.images(
                keywords=f"{query} high quality photography",
                region="wt-wt",
                safesearch="off",
                size="Large",
                color="color",
                type_image="photo",
                layout="Wide",
                license_image="any",
                max_results=5
            )
            
            for res in results:
                url = res.get("image")
                if not url:
                    continue
                    
                temp_path = f"{output_dir}/raw_{count}.jpg"
                final_path = f"{output_dir}/zoiris_real_{count}.jpg"
                
                print(f"Attempting download for {count}/5: {url[:60]}...")
                if download_image(url, temp_path):
                    if add_watermark(temp_path, final_path, logo_path):
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                        count += 1
                        break # Got a successful image for this query, move to next
                time.sleep(1)
            
            if count > 5:
                break
                
    print(f"Successfully downloaded and watermarked {count-1} ultra-realistic photos.")
