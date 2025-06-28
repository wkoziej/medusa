#!/usr/bin/env python3
"""
Basic Facebook publishing example for Medusa library.

This example demonstrates how to use the FacebookPublisher to publish
text posts and link posts to Facebook pages, including scheduled posts.
"""

import asyncio
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Add the src directory to the path so we can import medusa
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from medusa.publishers.facebook import FacebookPublisher
from medusa.models import PlatformConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example configuration - replace with your actual Facebook credentials
EXAMPLE_CONFIG = {
    "page_id": "your_facebook_page_id",
    "access_token": "your_facebook_page_access_token"
}

def create_facebook_config():
    """Create Facebook configuration."""
    return PlatformConfig(
        platform_name="facebook",
        credentials=EXAMPLE_CONFIG,
        enabled=True
    )

async def example_text_post():
    """Example: Simple text post."""
    print("\n=== Example: Simple Text Post ===")
    
    config = create_facebook_config()
    publisher = FacebookPublisher(config)
    
    try:
        # Authenticate
        await publisher.authenticate()
        print("✓ Authentication successful")
        
        # Publish simple text post
        result = await publisher.publish_post(
            content="Hello from Medusa! 🚀 This is a test post from our automation library.",
            metadata={}
        )
        
        print(f"✓ Post published successfully!")
        print(f"  Post ID: {result.post_id}")
        print(f"  Post URL: {result.post_url}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await publisher.cleanup()

async def example_link_post():
    """Example: Post with link."""
    print("\n=== Example: Link Post ===")
    
    config = create_facebook_config()
    publisher = FacebookPublisher(config)
    
    try:
        # Authenticate
        await publisher.authenticate()
        print("✓ Authentication successful")
        
        # Publish post with link
        result = await publisher.publish_post(
            content="Check out this amazing project! 🔗",
            metadata={
                "type": "link",
                "link": "https://github.com/your-username/medusa",
                "name": "Medusa - Media Upload & Social Automation",
                "description": "Python library for automating media uploads and social media publishing"
            }
        )
        
        print(f"✓ Link post published successfully!")
        print(f"  Post ID: {result.post_id}")
        print(f"  Post URL: {result.post_url}")
        print(f"  Link: {result.metadata.get('link', 'N/A') if result.metadata else 'N/A'}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await publisher.cleanup()

async def example_scheduled_post():
    """Example: Scheduled post for future publishing."""
    print("\n=== Example: Scheduled Post ===")
    
    config = create_facebook_config()
    publisher = FacebookPublisher(config)
    
    try:
        # Authenticate
        await publisher.authenticate()
        print("✓ Authentication successful")
        
        # Calculate scheduled time (30 minutes from now)
        scheduled_time = datetime.now(timezone.utc) + timedelta(minutes=30)
        scheduled_timestamp = int(scheduled_time.timestamp())
        
        print(f"📅 Scheduling post for: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Publish scheduled post
        result = await publisher.publish_post(
            content="This is a scheduled post! 📅 It was created automatically by Medusa.",
            metadata={
                "scheduled_publish_time": scheduled_timestamp
            }
        )
        
        print(f"✓ Scheduled post created successfully!")
        print(f"  Post ID: {result.post_id}")
        print(f"  Post URL: {result.post_url}")
        print(f"  Scheduled for: {datetime.fromtimestamp(scheduled_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"  Note: Post will be published automatically by Facebook at the scheduled time")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await publisher.cleanup()

async def example_scheduled_link_post():
    """Example: Scheduled post with link."""
    print("\n=== Example: Scheduled Link Post ===")
    
    config = create_facebook_config()
    publisher = FacebookPublisher(config)
    
    try:
        # Authenticate
        await publisher.authenticate()
        print("✓ Authentication successful")
        
        # Calculate scheduled time (1 hour from now)
        scheduled_time = datetime.now(timezone.utc) + timedelta(hours=1)
        scheduled_timestamp = int(scheduled_time.timestamp())
        
        print(f"📅 Scheduling link post for: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Publish scheduled link post
        result = await publisher.publish_post(
            content="Exciting announcement coming up! 🎉 Stay tuned for something amazing.",
            metadata={
                "type": "link",
                "link": "https://example.com/announcement",
                "name": "Big Announcement",
                "description": "Something exciting is coming soon!",
                "scheduled_publish_time": scheduled_timestamp
            }
        )
        
        print(f"✓ Scheduled link post created successfully!")
        print(f"  Post ID: {result.post_id}")
        print(f"  Post URL: {result.post_url}")
        print(f"  Link: {result.metadata.get('link', 'N/A') if result.metadata else 'N/A'}")
        print(f"  Scheduled for: {datetime.fromtimestamp(scheduled_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await publisher.cleanup()

async def example_with_progress_tracking():
    """Example: Post with progress tracking."""
    print("\n=== Example: Post with Progress Tracking ===")
    
    config = create_facebook_config()
    publisher = FacebookPublisher(config)
    
    def progress_callback(progress):
        print(f"📊 Progress: {progress.step} ({progress.current_step}/{progress.total_steps})")
        print(f"   Message: {progress.message}")
        if progress.status == "completed":
            print("   ✓ Completed!")
    
    try:
        # Authenticate
        await publisher.authenticate()
        print("✓ Authentication successful")
        
        # Publish with progress tracking
        result = await publisher.publish_post(
            content="This post demonstrates progress tracking! 📊 Each step is reported.",
            metadata={},
            progress_callback=progress_callback
        )
        
        print(f"✓ Post with progress tracking completed!")
        print(f"  Post ID: {result.post_id}")
        print(f"  Post URL: {result.post_url}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await publisher.cleanup()

async def example_health_check():
    """Example: Health check functionality."""
    print("\n=== Example: Health Check ===")
    
    config = create_facebook_config()
    publisher = FacebookPublisher(config)
    
    try:
        # Check health before authentication
        print(f"Health before auth: {'✓ Healthy' if publisher.health_check() else '✗ Unhealthy'}")
        
        # Authenticate
        await publisher.authenticate()
        print("✓ Authentication successful")
        
        # Check health after authentication
        print(f"Health after auth: {'✓ Healthy' if publisher.health_check() else '✗ Unhealthy'}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        await publisher.cleanup()

async def main():
    """Run all examples."""
    print("🚀 Facebook Publisher Examples")
    print("=" * 50)
    
    # Check if configuration is set up
    if EXAMPLE_CONFIG["page_id"] == "your_facebook_page_id":
        print("⚠️  WARNING: Please update EXAMPLE_CONFIG with your actual Facebook credentials")
        print("   - page_id: Your Facebook page ID")
        print("   - access_token: Your Facebook page access token")
        print("\n   These examples will fail without proper credentials!")
        print("\n   To get Facebook credentials:")
        print("   1. Create a Facebook App at https://developers.facebook.com/")
        print("   2. Add 'Pages' permission to your app")
        print("   3. Generate a Page Access Token for your Facebook page")
        print("   4. Update the EXAMPLE_CONFIG above with your credentials")
        return
    
    try:
        # Run examples
        await example_text_post()
        await example_link_post()
        await example_scheduled_post()
        await example_scheduled_link_post()
        await example_with_progress_tracking()
        await example_health_check()
        
        print("\n🎉 All examples completed!")
        print("\nKey Features Demonstrated:")
        print("✓ Text posts")
        print("✓ Link posts with metadata")
        print("✓ Scheduled posts (future publishing)")
        print("✓ Progress tracking")
        print("✓ Health checking")
        print("✓ Error handling")
        
        print("\nScheduled Posts Notes:")
        print("• Scheduled posts are created immediately but published later by Facebook")
        print("• You can see scheduled posts in your Facebook page's Publishing Tools")
        print("• Minimum scheduling time is typically 10 minutes in the future")
        print("• Maximum scheduling time is typically 6 months in the future")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Examples interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 