"""
Фикстуры для тестов Landings API.
"""

import pytest
from faker import Faker
from config import TestConfig
from src.backend.services.web.landings.adapter import LandingsAdapter
from src.backend.services.web.landings.service import LandingsService
from src.backend.services.web.landings.models.request_models import (
    UpdateMainPageRequestModel,
    MainPageItemRequestModel
)


fake = Faker('ru_RU')


class UpdateMainPageDataGenerator:
    """Генератор тестовых данных для обновления main-page."""
    
    EMOJIS = ["✈️", "🌍", "🏖️", "🎭", "🏰", "⛰️", "🌊", "🚀"]
    COLORS = ["#EBFAF5", "#FFF5E6", "#E6F3FF", "#F0E6FF", "#E6FFE6"]
    TYPES = ["experiences", "seasons", "destinations"]
    
    @staticmethod
    def generate_title() -> str:
        """Генерировать заголовок с эмодзи."""
        adjectives = [
            "Как классно провести",
            "Идеальные идеи для",
            "Лучшие варианты",
            "Новые впечатления",
            "Незабываемые моменты"
        ]
        nouns = ["лето", "зиму", "осень", "весну", "выходные", "отпуск"]
        emoji = UpdateMainPageDataGenerator.EMOJIS[
            hash(fake.word()) % len(UpdateMainPageDataGenerator.EMOJIS)
        ]
        return f"{fake.random.choice(adjectives)} {fake.random.choice(nouns)}{emoji}"
    
    @staticmethod
    def generate_subtitle() -> str:
        """Генерировать подзаголовок."""
        subtitles = [
            "Идеи для впечатлений в этом сезоне",
            "Откройте для себя лучшие места",
            "Планируйте вашу следующую поездку",
            "Вдохновитесь новыми путешествиями",
            "Найдите идеальное приключение"
        ]
        return fake.random.choice(subtitles)
    
    @staticmethod
    def generate_items(count: int = 5) -> list:
        """
        Генерировать список items.
        
        Args:
            count: Количество items
        
        Returns:
            Список MainPageItemRequestModel
        """
        items = []
        titles = [
            "Пройти по всем рекам и каналам Петербурга",
            "Выдохнуть и перезагрузиться на Алтае",
            "Почувствовать себя дворянином в замках Беларуси",
            "Посмотреть экскурсии",
            "Откроить красоту русской природы",
            "Погрузиться в историю древних городов"
        ]
        
        for i in range(count):
            item = MainPageItemRequestModel(
                objId=fake.random_int(min=1, max=1000),
                customTitle=fake.random.choice(titles),
                customPhotoId=fake.random_int(min=100, max=9999),
                extra={}
            )
            items.append(item)
        
        return items
    
    @staticmethod
    def generate_extra() -> dict:
        """Генерировать extra данные."""
        return {
            "color": UpdateMainPageDataGenerator.COLORS[
                hash(fake.word()) % len(UpdateMainPageDataGenerator.COLORS)
            ]
        }


@pytest.fixture
def landings_adapter():
    """Фикстура для LandingsAdapter."""
    return LandingsAdapter(host=TestConfig.BASE_API_URL)


@pytest.fixture
def landings_service(landings_adapter):
    """Фикстура для LandingsService."""
    return LandingsService(adapter=landings_adapter)


@pytest.fixture
def update_main_page_data():
    """Фикстура для генерации данных UpdateMainPageRequestModel."""
    return UpdateMainPageRequestModel(
        title=UpdateMainPageDataGenerator.generate_title(),
        subtitle=UpdateMainPageDataGenerator.generate_subtitle(),
        photoDesktopId=fake.random_int(min=1000, max=9999),
        photoMobileId=fake.random_int(min=1000, max=9999),
        type=fake.random.choice(UpdateMainPageDataGenerator.TYPES),
        extra=UpdateMainPageDataGenerator.generate_extra(),
        items=UpdateMainPageDataGenerator.generate_items(count=5)
    )


@pytest.fixture
def update_main_page_data_minimal():
    """Фикстура для генерации минимальных данных UpdateMainPageRequestModel."""
    return UpdateMainPageRequestModel(
        title="Тестовая страница",
        subtitle="Тестовое описание",
        photoDesktopId=1000,
        photoMobileId=1001,
        type="experiences",
        extra={},
        items=[]
    )
