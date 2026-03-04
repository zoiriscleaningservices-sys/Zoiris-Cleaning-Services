import os
import shutil
import subprocess

BATCH_SIZE = 50
ARCHIVE_DIR = "archived_cities"

def deploy_next_batch():
    if not os.path.exists(ARCHIVE_DIR):
        print("Archive directory not found or already empty.")
        return

    archived = [d for d in os.listdir(ARCHIVE_DIR)]
    
    if not archived:
        print("No more cities left in the archive to deploy!")
        return

    # Take the next batch
    batch = archived[:BATCH_SIZE]
    print(f"Moving next batch of {len(batch)} cities into the main repository...")

    for city in batch:
        src = os.path.join(ARCHIVE_DIR, city)
        dest = city
        try:
            shutil.move(src, dest)
        except Exception as e:
            print(f"Error moving {city}: {e}")

    print("Batch moved successfully. Committing to Git...")
    
    # Run Git commands
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", f"Deploy exact batch: {len(batch)} additional cities"], check=True)
    
    print("Pushing to GitHub...")
    subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
    
    cities_left = len(os.listdir(ARCHIVE_DIR))
    print(f"Deployment successful. {cities_left} cities remaining in the archive.")

if __name__ == "__main__":
    while os.path.exists(ARCHIVE_DIR) and len(os.listdir(ARCHIVE_DIR)) > 0:
        deploy_next_batch()
