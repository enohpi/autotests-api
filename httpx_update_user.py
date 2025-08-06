import httpx

from tools.fakers import get_random_email

client = httpx.Client(base_url="http://localhost:8000")

# Создаем пользователя
create_user_payload = {
    "email": get_random_email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

create_user_response = client.post("/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()
print(f"Create user data: {create_user_response_data}")
print(f"Status code: {create_user_response.status_code}")

login_payload = {
    "email": create_user_payload['email'],
    "password": create_user_payload['password'],
}

# Проходим аутентификацию
login_response = client.post("/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()
print(f"Login response: {login_response_data}")
print(f"Status code: {login_response.status_code}")

# Получение пользователя
authorization_payload = {
    "Authorization": f"Bearer {login_response_data["token"]["accessToken"]}",
}

# Обновление пользователя
edit_user_payload = {
    "email": get_random_email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

edit_user_response = client.patch(f"/api/v1/users/{create_user_response_data["user"]["id"]}", json=edit_user_payload,
                                  headers=authorization_payload)
edit_user_response_data = edit_user_response.json()

print(f"Edit user data: {edit_user_response_data}")
print(f"Status code: {edit_user_response.status_code}")
