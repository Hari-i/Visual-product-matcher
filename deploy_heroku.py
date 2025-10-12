#!/usr/bin/env python3
"""
Heroku Deployment Script for Visual Product Matcher
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Deploy to Heroku"""
    print("🚀 Starting Heroku deployment for Visual Product Matcher")
    
    # Check if Heroku CLI is installed
    if not run_command("heroku --version", "Checking Heroku CLI"):
        print("❌ Heroku CLI not found. Please install it from https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # Get app name from user or use default
    app_name = input("Enter Heroku app name (or press Enter for 'visual-product-matcher'): ").strip()
    if not app_name:
        app_name = "visual-product-matcher"
    
    # Check if app exists
    if not run_command(f"heroku apps:info {app_name}", f"Checking if app '{app_name}' exists"):
        # Create new app
        if not run_command(f"heroku create {app_name}", f"Creating new Heroku app '{app_name}'"):
            return False
    
    # Set environment variables
    env_vars = {
        'FLASK_ENV': 'production',
        'SECRET_KEY': 'your-secret-key-change-this-in-production'
    }
    
    for key, value in env_vars.items():
        if not run_command(f"heroku config:set {key}={value} -a {app_name}", f"Setting {key}"):
            return False
    
    # Deploy to Heroku
    if not run_command("git add .", "Staging files"):
        return False
    
    if not run_command('git commit -m "Deploy Visual Product Matcher to Heroku"', "Committing changes"):
        return False
    
    if not run_command(f"git push heroku main", f"Pushing to Heroku app '{app_name}'"):
        return False
    
    # Open the app
    if run_command(f"heroku open -a {app_name}", f"Opening app '{app_name}'"):
        print(f"\n🎉 Deployment successful!")
        print(f"Your app is available at: https://{app_name}.herokuapp.com")
        return True
    else:
        print(f"\n⚠️  Deployment completed but couldn't open the app automatically.")
        print(f"Your app should be available at: https://{app_name}.herokuapp.com")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
