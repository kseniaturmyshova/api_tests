"""
Сервис для работы с Landings API.
"""

from http import HTTPStatus
import allure
import requests

from src.backend.services.web.landings.adapter import LandingsAdapter
from src.backend.services.web.landings.models.request_models import UpdateMainPageRequestModel
from src.backend.services.web.landings.models.response_models import UpdateMainPageResponseModel
from src.utils.validations.rest_api import validate_response


class LandingsService:
    """Сервис для управления Landings endpoints."""
    
    def __init__(self, adapter: LandingsAdapter):
        """
        Инициализация сервиса.
        
        Args:
            adapter: LandingsAdapter для работы с API
        """
        self._adapter = adapter
    
    @allure.step("Обновить главную страницу (main-page)")
    def update_main_page(
        self,
        update_data: UpdateMainPageRequestModel,
        headers: dict
    ) -> UpdateMainPageResponseModel:
        """
        Обновить информацию о главной странице.
        
        Args:
            update_data: Модель с данными для обновления
            headers: HTTP заголовки с авторизацией
        
        Returns:
            UpdateMainPageResponseModel с данными обновленной страницы
        
        Raises:
            AssertionError: Если статус код не 200
        """
        # Преобразуем модель в словарь с alias (для API)
        validated_data = update_data.model_dump(by_alias=True)
        
        with allure.step("Отправить PUT запрос на обновление main-page"):
            response = self._adapter.update_main_page(json=validated_data, headers=headers)
        
        # Проверяем, что ответ успешный
        with allure.step(f"Проверить статус код {HTTPStatus.OK}"):
            validate_response(
                response=response,
                expected_status_code=HTTPStatus.OK
            )
        
        # Парсим ответ в модель
        response_data = response.json()
        
        with allure.step("Спарсить ответ в модель UpdateMainPageResponseModel"):
            return UpdateMainPageResponseModel(**response_data)
    
    @allure.step("Получить информацию о главной странице (main-page)")
    def get_main_page(self, headers: dict) -> UpdateMainPageResponseModel:
        """
        Получить информацию о главной странице.
        
        Args:
            headers: HTTP заголовки
        
        Returns:
            UpdateMainPageResponseModel с данными страницы
        
        Raises:
            AssertionError: Если статус код не 200
        """
        with allure.step("Отправить GET запрос для получения main-page"):
            response = self._adapter.get_main_page(headers=headers)
        
        # Проверяем, что ответ успешный
        with allure.step(f"Проверить статус код {HTTPStatus.OK}"):
            validate_response(
                response=response,
                expected_status_code=HTTPStatus.OK
            )
        
        # Парсим ответ в модель
        response_data = response.json()
        
        with allure.step("Спарсить ответ в модель UpdateMainPageResponseModel"):
            return UpdateMainPageResponseModel(**response_data)
