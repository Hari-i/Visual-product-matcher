#!/usr/bin/env python3
"""
Startup script for Visual Product Matcher
"""
import os
import sys
import subprocess

def main():
    """Start the Flask application"""
    print("Starting Visual Product Matcher...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    print(f"Working directory: {os.getcwd()}")
    print("Starting Flask server on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        # Start the Flask app
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")

if __name__ == "__main__":
    main()
