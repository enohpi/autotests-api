from typing import TypedDict

from clients.api_client import APIClient

class CreateUserRequestDict(TypedDict):
    """
    Описание структуры запроса для создания пользователя.
    """
    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str

class PublicUsersClient(APIClient):
    """
    Клиент для работы с публичным запросами /api/v1/users
    """
    def create_user_api(self, request: CreateUserRequestDict):
        """
        Метод выполняет аутентификацию пользователя.

        :param request: Словарь с email, password, lastName, firstName, middleName.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/users", json=request)