import os
import sys
import time
import urllib.request
import urllib.parse
import random

try:
    from PIL import Image
except ImportError:
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image

def download_image(url, save_path):
    if not os.path.exists(save_path):
        import cloudscraper
        scraper = cloudscraper.create_scraper()
        try:
            response = scraper.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, 'wb') as out_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        out_file.write(chunk)
                
                # Verify it's not a tiny error page
                if os.path.getsize(save_path) < 1000:
                    os.remove(save_path)
                    print(f"Failed to download {url}: file too small")
                    return False
                
                print(f"Downloaded {save_path}")
                return True
            else:
                print(f"Failed to download {url}: {response.status_code}")
                return False
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
    output_dir = "images/ai_bulk"
    os.makedirs(output_dir, exist_ok=True)
    
    base_prompts = [
        "ultra realistic 8k photograph of a professional cleaner wiping a marble kitchen island interior bright natural light",
        "hyper realistic photo of a professional maid vacuuming a living room with white carpet luxury interior",
        "photorealistic 8k image of hands wearing yellow gloves scrubbing a sparkling clean modern bathroom sink",
        "ultra realistic high quality photo of cleaning supplies neatly organized in a caddy in a luxury bathroom",
        "hyper realistic wide shot of a pristine spotless master bedroom after a deep clean sunlight streaming in",
        "ultra realistic close up of a microfiber cloth polishing a stainless steel refrigerator in a modern kitchen",
        "photorealistic image of a professional commercial cleaner mopping a gleaming hallway floor",
        "hyper realistic photo of a freshly cleaned luxury glass shower cubicle sparkling with no water spots",
        "ultra realistic photo of an organized spotless office desk after commercial cleaning services",
        "photorealistic 8k shot of a person in a uniform deep cleaning a beautiful residential home carpet"
    ]
    
    count = 1
    for prompt_base in base_prompts:
        for variation in ["", "cinematic lighting", "morning sunlight", "high contrast"]:
            if count > 40:
                break
                
            full_prompt = f"{prompt_base} {variation} photography pristine 100% real no text"
            encoded_prompt = urllib.parse.quote(full_prompt)
            # Using pollinations.ai free image generation endpoint
            # Adding seed to ensure we get unique images even if the prompt is similar
            seed = random.randint(1, 1000000)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1600&height=900&nologo=true&seed={seed}"
            
            temp_path = f"{output_dir}/raw_{count}.jpg"
            final_path = f"{output_dir}/zoiris_ai_{count}.jpg"
            
            print(f"Generating image {count}/40: {prompt_base[:30]}...")
            if download_image(url, temp_path):
                add_watermark(temp_path, final_path, logo_path)
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                count += 1
            
            time.sleep(2) # Prevent overloading the API
            
    print("Finished generating 40 ultra-realistic AI images.")
