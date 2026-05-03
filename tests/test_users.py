from http import HTTPStatus

import pytest

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response


@pytest.mark.users  # Добавили маркировку users
@pytest.mark.regression  # Добавили маркировку regression
def test_create_user(public_users_client: PublicUsersClient):
    # Формируем тело запроса на создание пользователя
    request = CreateUserRequestSchema()
    # Отправляем запрос на создание пользователя
    response = public_users_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    # Используем функцию для проверки кода ответа
    assert_status_code(response.status_code, HTTPStatus.OK)
    # Используем функцию для проверки ответа создания юзера
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(private_users_client: PrivateUsersClient, function_user):
    response = private_users_client.get_user_me_api()
    response_data = GetUserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_get_user_response(response_data, function_user.response)

    validate_json_schema(response.json(), response_data.model_json_schema())