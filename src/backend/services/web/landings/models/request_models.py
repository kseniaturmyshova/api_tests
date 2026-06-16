"""
Модели запросов для API endpoints Landings.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MainPageItemRequestModel(BaseModel):
    """Модель для одного item в списке main-page."""
    
    obj_id: int = Field(..., alias="objId", description="ID объекта")
    custom_title: str = Field(..., alias="customTitle", description="Кастомный заголовок")
    custom_photo_id: int = Field(..., alias="customPhotoId", description="ID кастомной фотографии")
    extra: Dict[str, Any] = Field(default_factory=dict, description="Дополнительные данные")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "objId": 42,
                "customTitle": "Пройти по всем рекам Петербурга",
                "customPhotoId": 1234,
                "extra": {}
            }
        }


class UpdateMainPageRequestModel(BaseModel):
    """Модель для обновления main-page endpoint."""
    
    title: str = Field(..., description="Заголовок главной страницы")
    subtitle: str = Field(..., description="Подзаголовок главной страницы")
    photo_desktop_id: int = Field(..., alias="photoDesktopId", description="ID фотографии для десктопа")
    photo_mobile_id: int = Field(..., alias="photoMobileId", description="ID фотографии для мобиля")
    type: str = Field(..., description="Тип (например: 'experiences', 'seasons')")
    extra: Dict[str, Any] = Field(default_factory=dict, description="Дополнительные данные (например: цвета)")
    items: List[MainPageItemRequestModel] = Field(default_factory=list, description="Список items")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "Как классно провести лето✈️",
                "subtitle": "Идеи для впечатлений в этом сезоне",
                "photoDesktopId": 2261,
                "photoMobileId": 2260,
                "type": "seasons",
                "extra": {"color": "#EBFAF5"},
                "items": [
                    {
                        "objId": 1,
                        "customTitle": "Пройти по всем рекам и каналам Петербурга",
                        "customPhotoId": 100,
                        "extra": {}
                    }
                ]
            }
        }
