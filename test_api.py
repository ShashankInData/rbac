import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    response = requests.get(f"{BASE_URL}/")
    print("\nTesting root endpoint:")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_login():
    """Test login with Tony's credentials"""
    login_data = {
        "username": "Tony",
        "password": "password123"
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json=login_data
    )
    print("\nTesting login endpoint:")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get("access_token") if response.status_code == 200 else None

def test_protected_endpoint(token):
    if not token:
        print("\nSkipping protected endpoint test - no token available")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/test", headers=headers)
    print("\nTesting protected endpoint:")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_chat_query(token, message, expected_status=200):
    """Test chat query with authorization"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/api/v1/chat/query",
        headers=headers,
        json={"message": message}
    )
    print(f"\nTesting chat query with message: {message}")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == expected_status

def main():
    # Test login
    token = test_login()
    if not token:
        print("Login failed, aborting tests")
        return

    # Test engineering question (should succeed)
    test_chat_query(token, "Give me Q2 revenue", expected_status=200)

    # Test HR question (should fail)
    test_chat_query(token, "What are our HR policies?", expected_status=403)

if __name__ == "__main__":
    test_root()
    token = test_login()
    test_protected_endpoint(token)
    main() 