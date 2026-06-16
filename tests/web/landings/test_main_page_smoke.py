"""
Smoke тесты для Landings API - main-page endpoint.
"""

from http import HTTPStatus
import pytest
import allure

from src.utils.validations.rest_api import validate_response
from src.utils.validations.assert_wrappers import assert_eq


@pytest.mark.smoke
@allure.title("Обновление main-page: корректные данные, авторизованный пользователь")
@allure.description(
    """
    Smoke тест для проверки успешного обновления главной страницы.
    
    Шаги:
    1. Подготовить валидные данные для обновления main-page
    2. Отправить PUT запрос с авторизацией
    3. Проверить, что статус код 200 OK
    4. Проверить, что основные поля присутствуют в ответе
    """
)
def test_update_main_page_with_valid_data(
    landings_adapter,
    auth_headers,
    update_main_page_data
):
    """
    Happy path тест для обновления main-page.
    
    Проверяет:
    - Статус код 200
    - Наличие обязательных полей в ответе
    """
    with allure.step("Отправить PUT запрос на обновление main-page"):
        response = landings_adapter.update_main_page(
            headers=auth_headers,
            json=update_main_page_data.model_dump(by_alias=True)
        )
    
    with allure.step("Проверить статус код 200 OK и обязательные поля"):
        validate_response(
            response=response,
            expected_status_code=HTTPStatus.OK,
            non_empty_fields=["id", "title", "subtitle", "type"]
        )
    
    with allure.step("Проверить соответствие возвращенных данных отправленным"):
        response_json = response.json()
        
        assert_eq(
            expected_value=update_main_page_data.title,
            actual_value=response_json.get("title"),
            allure_title="Проверка заголовка main-page",
            error_msg="Заголовок в ответе не совпадает с отправленным"
        )
        
        assert_eq(
            expected_value=update_main_page_data.subtitle,
            actual_value=response_json.get("subtitle"),
            allure_title="Проверка подзаголовка main-page",
            error_msg="Подзаголовок в ответе не совпадает с отправленным"
        )
        
        assert_eq(
            expected_value=update_main_page_data.type,
            actual_value=response_json.get("type"),
            allure_title="Проверка типа main-page",
            error_msg="Тип в ответе не совпадает с отправленным"
        )


@pytest.mark.smoke
@allure.title("Обновление main-page: минимальные валидные данные")
@allure.description(
    """
    Smoke тест с минимальным набором данных.
    
    Проверяет, что API правильно обрабатывает запрос с минимальными полями:
    - title
    - subtitle
    - photoDesktopId
    - photoMobileId
    - type
    - пустые extra и items
    """
)
def test_update_main_page_with_minimal_data(
    landings_adapter,
    auth_headers,
    update_main_page_data_minimal
):
    """
    Тест обновления main-page с минимальным набором данных.
    """
    with allure.step("Отправить PUT запрос с минимальными данными"):
        response = landings_adapter.update_main_page(
            headers=auth_headers,
            json=update_main_page_data_minimal.model_dump(by_alias=True)
        )
    
    with allure.step("Проверить статус код 200 OK"):
        validate_response(
            response=response,
            expected_status_code=HTTPStatus.OK
        )
    
    with allure.step("Проверить, что ответ содержит все обязательные поля"):
        response_json = response.json()
        required_fields = ["id", "title", "subtitle", "type", "items"]
        
        for field in required_fields:
            assert field in response_json, f"Поле '{field}' отсутствует в ответе"
            allure.attach(
                f"{field}: {response_json.get(field)}",
                f"Значение поля {field}",
                allure.attachment_type.TEXT
            )


@pytest.mark.smoke
@allure.title("Обновление main-page: с несколькими items")
@allure.description(
    """
    Smoke тест для проверки обновления main-page с полным списком items.
    
    Проверяет корректность обработки:
    - Нескольких items в списке
    - Структуры каждого item
    - Сохранения данных items в ответе
    """
)
def test_update_main_page_with_items(
    landings_adapter,
    auth_headers,
    update_main_page_data
):
    """
    Тест обновления main-page с несколькими items.
    """
    request_json = update_main_page_data.model_dump(by_alias=True)
    items_count = len(request_json.get("items", []))
    
    with allure.step(f"Подготовить данные с {items_count} items"):
        allure.attach(
            str(request_json["items"]),
            "Список items для отправки",
            allure.attachment_type.JSON
        )
    
    with allure.step("Отправить PUT запрос на обновление main-page"):
        response = landings_adapter.update_main_page(
            headers=auth_headers,
            json=request_json
        )
    
    with allure.step("Проверить статус код 200 OK"):
        validate_response(
            response=response,
            expected_status_code=HTTPStatus.OK
        )
    
    with allure.step("Проверить, что items присутствуют в ответе"):
        response_json = response.json()
        response_items = response_json.get("items", [])
        
        assert len(response_items) > 0, "Ответ не содержит items"
        
        allure.attach(
            str(response_items),
            "Список items в ответе",
            allure.attachment_type.JSON
        )
        
        with allure.step("Проверить структуру первого item"):
            first_item = response_items[0]
            required_item_fields = ["id", "title"]
            
            for field in required_item_fields:
                assert field in first_item, f"Поле '{field}' отсутствует в item"
