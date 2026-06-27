import allure

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema, CreateExerciseResponseSchema,
    ExerciseSchema, GetExerciseResponseSchema, UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema, GetExercisesResponseSchema
)
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.errors import assert_internal_error_response


@allure.step("Check exercise response")
def assert_create_exercise_response(request: CreateExerciseRequestSchema, response: CreateExerciseResponseSchema):
    """
    Проверяет, что ответ на создание упражнения соответствует запросу.

    :param request: Исходный запрос на создание упражнения.
    :param response: Ответ API с данными упражнения.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(response.exercise.title, request.title, "title")
    assert_equal(response.exercise.course_id, request.course_id, "course_id")
    assert_equal(response.exercise.max_score, request.max_score, "max_score")
    assert_equal(response.exercise.min_score, request.min_score, "min_score")
    assert_equal(response.exercise.order_index, request.order_index, "order_index")
    assert_equal(response.exercise.description, request.description, "description")
    assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check exercise")
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные упражнения соответствуют ожидаемым.

    :param actual: Фактические данные упражнения.
    :param expected: Ожидаемые данные упражнения.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


@allure.step("Check get exercise response")
def assert_get_exercise_response(get_exercise_response: GetExerciseResponseSchema,
                                 create_exercise_response: CreateExerciseResponseSchema):
    """
    Проверяет, что ответ на получение упражнения соответствует ответу на его создание.

    :param get_exercise_response: Ответ API при запросе данных упражнения.
    :param create_exercise_response: Ответ API при создании упражнения.
    :raises AssertionError: Если данные упражнения не совпадают.
    """
    assert_exercise(get_exercise_response.exercise, create_exercise_response.exercise)


@allure.step("Check update exercise response")
def assert_update_exercise_response(request: UpdateExerciseRequestSchema, response: UpdateExerciseResponseSchema):
    """
    Проверяет, что ответ на обновление упражнения соответствует данным из запроса.

    :param request: Исходный запрос на обновление упражнения.
    :param response: Ответ API с обновленными данными упражнения.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    if request.title is not None:
        assert_equal(response.exercise.title, request.title, "title")

    if request.max_score is not None:
        assert_equal(response.exercise.max_score, request.max_score, "max_score")

    if request.min_score is not None:
        assert_equal(response.exercise.min_score, request.min_score, "min_score")

    if request.order_index is not None:
        assert_equal(response.exercise.order_index, request.order_index, "order_index")

    if request.description is not None:
        assert_equal(response.exercise.description, request.description, "description")

    if request.estimated_time is not None:
        assert_equal(response.exercise.estimated_time, request.estimated_time, "estimated_time")


@allure.step("Check exercise not found response")
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если упражнение не найдено на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Exercise not found"
    """
    expected = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(actual, expected)


@allure.step("Check get exercises response")
def assert_get_exercises_response(get_exercises_response: GetExercisesResponseSchema,
                                  create_exercise_responses: list[CreateExerciseResponseSchema]):
    """
    Проверяет, что ответ на получение списка упражнений соответствует ответам на их создание.

    :param get_exercises_response: Ответ API при запросе списка упражнений.
    :param create_exercise_responses: Список API ответов при создании упражнений.
    :raises AssertionError: Если данные курсов не совпадают.
    """
    assert_length(get_exercises_response.exercises, create_exercise_responses, "exercises")

    for index, create_exercise_response in enumerate(create_exercise_responses):
        assert_exercise(get_exercises_response.exercises[index], create_exercise_response.exercise)