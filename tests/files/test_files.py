from http import HTTPStatus

import pytest

from clients.errors_schema import ValidationErrorResponseSchema, InternalErrorResponseSchema
from clients.files.files_client import FilesClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, GetFileResponseSchema
from fixtures.files import FileFixture
from tools.assertions.base import assert_status_code
from tools.assertions.files import assert_create_file_response, assert_file_is_accessible, assert_get_file_response, \
    assert_create_file_with_empty_directory_response, assert_create_file_with_empty_filename_response, \
    assert_file_not_found_response, assert_get_file_with_incorrect_file_id_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.files
@pytest.mark.regression
class TestFiles:
    def test_create_file(self, files_client: FilesClient):
        request = CreateFileRequestSchema(upload_file="./testdata/files/image.png")
        response = files_client.create_file_api(request)
        response_data = CreateFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_file_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

        expected_url = f"http://localhost:8000/static/{request.directory}/{request.filename}"
        assert_file_is_accessible(expected_url)

    def test_get_file(self, files_client: FilesClient, function_file: FileFixture):
        # Здесь используется клиент files_client, который делает HTTP-запрос на получение данных файла по его id.
        # function_file.response.file.id — это id ранее созданного файла, переданный из фикстуры.
        response = files_client.get_file_api(function_file.response.file.id)
        # Это позволяет проверить, что API действительно вернул JSON-ответ в ожидаемом формате.
        response_data = GetFileResponseSchema.model_validate_json(response.text)
        # Если API работает корректно, сервер должен вернуть статус 200 OK.
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Эта функция сравнивает содержимое полученного файла с тем, что было создано ранее,
        # проверяя соответствие всех полей (id, url, filename, directory).
        assert_get_file_response(response_data, function_file.response)
        # Здесь проверяется, что структура JSON-ответа соответствует схеме GetFileResponseSchema.
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_create_file_with_empty_filename(self, files_client: FilesClient):
        request = CreateFileRequestSchema(
            filename="",
            upload_file="./testdata/files/image.png"
        )
        response = files_client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        # Проверка, что код ответа соответствует ожиданиям (422 - Unprocessable Entity)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # Проверка, что ответ API соответствует ожидаемой валидационной ошибке
        assert_create_file_with_empty_filename_response(response_data)

        # Дополнительная проверка структуры JSON, чтобы убедиться, что схема валидационного ответа не изменилась
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_create_file_with_empty_directory(self, files_client: FilesClient):
        request = CreateFileRequestSchema(
            directory="",
            upload_file="./testdata/files/image.png"
        )
        response = files_client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        # Проверка, что код ответа соответствует ожиданиям (422 - Unprocessable Entity)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # Проверка, что ответ API соответствует ожидаемой валидационной ошибке
        assert_create_file_with_empty_directory_response(response_data)

        # Дополнительная проверка структуры JSON
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_file(self, files_client: FilesClient, function_file: FileFixture):
        # 1. Удаляем файл
        delete_response = files_client.delete_file_api(function_file.response.file.id)
        # 2. Проверяем, что файл успешно удален (статус 200 OK)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        # 3. Пытаемся получить удаленный файл
        get_response = files_client.get_file_api(function_file.response.file.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        # 4. Проверяем, что сервер вернул 404 Not Found
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        # 5. Проверяем, что в ответе содержится ошибка "File not found"
        assert_file_not_found_response(get_response_data)

        # 6. Проверяем, что ответ соответствует схеме
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    def test_get_file_with_incorrect_file_id(self, files_client: FilesClient, ):
        # 1. Запрос с некорректным id
        response = files_client.get_file_api("incorrect-file-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        # 2. Проверка, что код ответа соответствует ожиданиям (422 - Unprocessable Entity)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        # 3. Проверяем, что в ответе содержится ошибка "invalid character: expected an optional prefix"
        assert_get_file_with_incorrect_file_id_response(response_data)

        # 4. Проверяем, что ответ соответствует схеме
        validate_json_schema(response.json(), response_data.model_json_schema())
