import httpx

login_payload = {
    "email": "vadim@example.com",
    "password": "vadim"
}

login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_json = login_response.json()

print(f"Login response: {login_response_json}")
print(f"Status code: {login_response.status_code}")

user_me_payload = {
    "Authorization": f"Bearer {login_response_json["token"]["accessToken"]}",
}

user_me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=user_me_payload)
user_me_json = user_me_response.json()

print(f"User response: {user_me_json}")
print(f"Status code: {user_me_response.status_code}")