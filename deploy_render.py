#!/usr/bin/env python3
"""
Render Deployment Guide for Visual Product Matcher
"""
import os
import subprocess
import sys

def main():
    """Provide Render deployment instructions"""
    print("🚀 Render Deployment Guide for Visual Product Matcher")
    print("=" * 60)
    
    print("\n📋 Prerequisites:")
    print("1. GitHub repository with your code")
    print("2. Render account (https://render.com)")
    
    print("\n🔧 Deployment Steps:")
    print("1. Go to https://render.com")
    print("2. Sign in with GitHub")
    print("3. Click 'New +' → 'Web Service'")
    print("4. Connect your GitHub repository")
    print("5. Configure the service:")
    print("   - Name: visual-product-matcher")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: cd backend && gunicorn app:app --bind 0.0.0.0:$PORT")
    print("6. Click 'Create Web Service'")
    
    print("\n⚙️  Environment Variables to Set:")
    print("In Render dashboard, go to your service → Environment tab:")
    print("- FLASK_ENV=production")
    print("- SECRET_KEY=your-secret-key-here")
    print("- PORT=10000 (Render sets this automatically)")
    
    print("\n📁 Required Files (Already Present):")
    print("✅ requirements.txt - Python dependencies")
    print("✅ Procfile - Process configuration")
    print("✅ runtime.txt - Python version")
    print("✅ config.py - Application configuration")
    
    print("\n🎯 Render Advantages:")
    print("- Free tier available")
    print("- Automatic HTTPS")
    print("- Easy GitHub integration")
    print("- Automatic deployments on git push")
    print("- Good for Python applications")
    
    print("\n🔍 Troubleshooting:")
    print("If deployment fails:")
    print("1. Check the build logs in Render dashboard")
    print("2. Ensure all files are committed to GitHub")
    print("3. Verify requirements.txt has correct versions")
    print("4. Check that the start command is correct")
    print("5. Make sure Python version in runtime.txt is supported")
    
    print("\n⚠️  Common Issues:")
    print("- Build timeout: Add 'pip install --no-cache-dir' to build command")
    print("- Memory issues: Upgrade to paid plan if needed")
    print("- Python version: Ensure runtime.txt specifies a supported version")
    
    print("\n📞 Support:")
    print("If you need help, check Render's documentation:")
    print("https://render.com/docs")
    
    print("\n🎉 Your app will be available at:")
    print("https://your-app-name.onrender.com")

if __name__ == "__main__":
    main()
