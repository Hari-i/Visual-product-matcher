#!/usr/bin/env python3
"""
Railway Deployment Guide for Visual Product Matcher
"""
import os
import subprocess
import sys

def main():
    """Provide Railway deployment instructions"""
    print("🚀 Railway Deployment Guide for Visual Product Matcher")
    print("=" * 60)
    
    print("\n📋 Prerequisites:")
    print("1. GitHub repository with your code")
    print("2. Railway account (https://railway.app)")
    
    print("\n🔧 Deployment Steps:")
    print("1. Go to https://railway.app")
    print("2. Sign in with GitHub")
    print("3. Click 'Deploy from GitHub repo'")
    print("4. Select your repository")
    print("5. Railway will automatically detect it's a Python app")
    print("6. Click 'Deploy'")
    
    print("\n⚙️  Environment Variables to Set:")
    print("In Railway dashboard, go to your service → Variables tab:")
    print("- FLASK_ENV=production")
    print("- SECRET_KEY=your-secret-key-here")
    print("- PORT=5000 (Railway sets this automatically)")
    
    print("\n📁 Required Files (Already Present):")
    print("✅ requirements.txt - Python dependencies")
    print("✅ Procfile - Process configuration")
    print("✅ runtime.txt - Python version")
    print("✅ config.py - Application configuration")
    
    print("\n🎯 Railway Advantages:")
    print("- Automatic Python version detection")
    print("- Easy GitHub integration")
    print("- Built-in HTTPS")
    print("- Automatic deployments on git push")
    print("- Generous free tier")
    
    print("\n🔍 Troubleshooting:")
    print("If deployment fails:")
    print("1. Check the build logs in Railway dashboard")
    print("2. Ensure all files are committed to GitHub")
    print("3. Verify requirements.txt has correct versions")
    print("4. Check that Procfile is in the root directory")
    
    print("\n📞 Support:")
    print("If you need help, check Railway's documentation:")
    print("https://docs.railway.app/")
    
    print("\n🎉 Your app will be available at:")
    print("https://your-app-name.railway.app")

if __name__ == "__main__":
    main()
