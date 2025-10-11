#!/usr/bin/env python3
"""
Quick deployment script for Visual Product Matcher
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    """Deploy to Heroku"""
    print("🚀 Visual Product Matcher - Quick Deploy")
    print("=" * 50)
    
    # Check if git is initialized
    if not os.path.exists('.git'):
        print("📁 Initializing git repository...")
        if not run_command("git init", "Git initialization"):
            return False
    
    # Add all files
    if not run_command("git add .", "Adding files to git"):
        return False
    
    # Commit changes
    if not run_command('git commit -m "Deploy Visual Product Matcher"', "Committing changes"):
        return False
    
    # Check if Heroku CLI is installed
    try:
        subprocess.run("heroku --version", shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ Heroku CLI not found. Please install it from: https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Get app name from user
    app_name = input("Enter your Heroku app name (or press Enter for auto-generated): ").strip()
    
    if app_name:
        create_cmd = f"heroku create {app_name}"
    else:
        create_cmd = "heroku create"
    
    # Create Heroku app
    if not run_command(create_cmd, "Creating Heroku app"):
        return False
    
    # Deploy to Heroku
    if not run_command("git push heroku main", "Deploying to Heroku"):
        return False
    
    # Open the app
    print("🌐 Opening your deployed app...")
    run_command("heroku open", "Opening app in browser")
    
    print("\n🎉 Deployment completed successfully!")
    print("Your Visual Product Matcher is now live on Heroku!")
    print("\n📱 Features available:")
    print("  ✅ Image upload (file + URL)")
    print("  ✅ Visual similarity search")
    print("  ✅ Similarity score filtering")
    print("  ✅ Mobile responsive design")
    print("  ✅ 100+ product database")

if __name__ == "__main__":
    main()
