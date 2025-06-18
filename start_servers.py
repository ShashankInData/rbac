#!/usr/bin/env python3
"""
Startup script for RBAC Chatbot
Launches both FastAPI and Streamlit servers
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_fastapi():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        # Start FastAPI server in background
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app.main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ FastAPI server started successfully on http://localhost:8000")
            return process
        else:
            print("❌ FastAPI server failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting FastAPI server: {e}")
        return None

def start_streamlit():
    """Start the Streamlit server"""
    print("🚀 Starting Streamlit server...")
    try:
        # Start Streamlit server in background
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501", "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Streamlit server started successfully on http://localhost:8501")
            return process
        else:
            print("❌ Streamlit server failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting Streamlit server: {e}")
        return None

def main():
    print("🤖 RBAC Chatbot Startup")
    print("=" * 40)
    
    # Check if required files exist
    if not Path("app/main.py").exists():
        print("❌ FastAPI app not found. Please ensure app/main.py exists.")
        return
    
    if not Path("streamlit_app.py").exists():
        print("❌ Streamlit app not found. Please ensure streamlit_app.py exists.")
        return
    
    # Start FastAPI server
    fastapi_process = start_fastapi()
    if not fastapi_process:
        print("❌ Failed to start FastAPI server. Exiting.")
        return
    
    # Start Streamlit server
    streamlit_process = start_streamlit()
    if not streamlit_process:
        print("❌ Failed to start Streamlit server. Exiting.")
        fastapi_process.terminate()
        return
    
    print("\n" + "=" * 40)
    print("🎉 Both servers started successfully!")
    print("\n📱 Access your application:")
    print("   • Frontend: http://localhost:8501")
    print("   • API Docs: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    print("\n⏹️  Press Ctrl+C to stop both servers")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        fastapi_process.terminate()
        streamlit_process.terminate()
        print("✅ Servers stopped.")

if __name__ == "__main__":
    main() 