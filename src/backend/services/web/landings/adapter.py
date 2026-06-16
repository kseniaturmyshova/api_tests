"""
Адаптер для взаимодействия с API Landings сервиса.
"""

from typing import Optional, Dict, Any
import requests
from src.backend.clients.http_client import HTTPClient


class LandingsAdapter:
    """Адаптер для работы с endpoints Landings API."""
    
    def __init__(self, host: str):
        """
        Инициализация адаптера.
        
        Args:
            host: Базовый URL API (например: https://experience.staging.k8s-dev.tripster.ru)
        """
        self._http_client = HTTPClient(host=host)
    
    def update_main_page(
        self,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Обновить главную страницу (main-page).
        
        Args:
            json: Данные для обновления
            headers: HTTP заголовки (должны содержать авторизацию)
        
        Returns:
            Response объект с результатом запроса
        """
        return self._http_client.put(
            route="/service/landings/api/v1/main-page",
            json=json,
            headers=headers
        )
    
    def get_main_page(
        self,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        Получить информацию о главной странице.
        
        Args:
            headers: HTTP заголовки
        
        Returns:
            Response объект с результатом запроса
        """
        return self._http_client.get(
            route="/service/landings/api/v1/main-page",
            headers=headers
        )
