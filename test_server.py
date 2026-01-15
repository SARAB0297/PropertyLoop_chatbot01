"""Quick test script to verify the server endpoints."""
import requests
import sys

base_url = "http://127.0.0.1:8000"

print("Testing FastAPI endpoints...")
print("=" * 50)

# Test root endpoint
try:
    response = requests.get(f"{base_url}/")
    print(f"GET / -> Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error connecting to server: {e}")
    print("\nMake sure the server is running:")
    print("  python -m uvicorn app.main:app --reload")
    sys.exit(1)

print("\n" + "=" * 50)
print("✓ Root endpoint is working!")
print("\nAvailable URLs:")
print(f"  - Root: {base_url}/")
print(f"  - Health: {base_url}/health")
print(f"  - Docs: {base_url}/docs")
print(f"  - Chat: {base_url}/chat (POST)")
