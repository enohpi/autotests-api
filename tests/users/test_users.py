from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.users.private_users_client import PrivateUsersClient
from clients.users.public_users_client import PublicUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake


@pytest.mark.users  # Добавили маркировку users
@pytest.mark.regression  # Добавили маркировку regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
class TestUsers:
    @pytest.mark.parametrize("email", ["mail.ru", "gmail.com", "example.com"])
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.title("Create user")
    @allure.severity(Severity.CRITICAL)
    def test_create_user(self, email: str, public_users_client: PublicUsersClient):
        # Формируем тело запроса на создание пользователя
        request = CreateUserRequestSchema(email=fake.email(domain=email))
        # Отправляем запрос на создание пользователя
        response = public_users_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)

        # Используем функцию для проверки кода ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Используем функцию для проверки ответа создания юзера
        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.title("Get user me")
    @allure.severity(Severity.CRITICAL)
    def test_get_user_me(self, private_users_client: PrivateUsersClient, function_user):
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), response_data.model_json_schema())
