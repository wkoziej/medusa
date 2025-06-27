# ABOUTME: Basic usage example showing typical Medusa workflow for video upload and social sharing
# ABOUTME: Demonstrates async task creation, status monitoring, and error handling patterns

import time
from medusa import MedusaCore

def main():
    # Initialize Medusa with configuration
    medusa = MedusaCore(config_file="config_example.json")
    
    # Upload video to YouTube and share on Facebook
    task_id = medusa.publish_async(
        media_file="path/to/your/video.mp4",
        platforms=["youtube", "facebook"],
        metadata={
            "youtube": {
                "title": "My Amazing Video",
                "description": "Check out this awesome content!",
                "tags": ["demo", "medusa", "automation"],
                "privacy": "public"
            },
            "facebook": {
                "message": "Just uploaded a new video! Check it out: {youtube_url} #newvideo"
            }
        }
    )
    
    print(f"Task started with ID: {task_id}")
    
    # Monitor task progress
    while True:
        status = medusa.get_task_status(task_id)
        print(f"Status: {status['status']}")
        
        if status['status'] == 'completed':
            print("✅ Task completed successfully!")
            print(f"YouTube URL: {status['results']['youtube_url']}")
            print(f"Facebook Post ID: {status['results']['facebook_post_id']}")
            break
        elif status['status'] == 'failed':
            print("❌ Task failed!")
            print(f"Error: {status['error']}")
            print(f"Failed platform: {status['failed_platform']}")
            break
        elif status['status'] == 'in_progress':
            print(f"🔄 {status.get('message', 'Processing...')}")
        
        time.sleep(10)  # Check every 10 seconds


if __name__ == "__main__":
    main()