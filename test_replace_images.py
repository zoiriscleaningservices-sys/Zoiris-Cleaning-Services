import os
import shutil
import replace_images

def test_replacement():
    test_src = r"c:\Users\lucia\OneDrive\Desktop\Zoiris-Cleaning-Services\huntsville-al\top-rated-gym-fitness-center-cleaning\index.html"
    test_dest = "test_gym_cleaning.html"
    
    print(f"Copying {test_src} to {test_dest}")
    shutil.copy2(test_src, test_dest)
    
    # Run the replacement on the single test file by temporarily overriding os.walk
    original_walk = os.walk
    def mock_walk(dir):
        return [(".", [], [test_dest])]
    
    try:
        os.walk = mock_walk
        print("Running replace script...")
        replace_images.main()
        
        print("\nChecking the modified test file for specific local URLs...")
        with open(test_dest, "r", encoding="utf-8") as f:
            content = f.read()
            
            checks = [
                "/images/logo.png",
                "/images/location_hero.png",
                "/images/services_action.png",
                "/images/services/gym_fitness_center_cleaning.jpg"
            ]
            for check in checks:
                if check in content:
                    print(f"[PASS] Found {check}")
                else:
                    print(f"[FAIL] Missing {check}")
                    
            if "i.ibb.co" not in content:
                print(f"[PASS] No more 'i.ibb.co' references found")
            else:
                print(f"[FAIL] 'i.ibb.co' still exists in the file!")
    finally:
        os.walk = original_walk
        if os.path.exists(test_dest):
            os.remove(test_dest)
            
if __name__ == "__main__":
    test_replacement()
