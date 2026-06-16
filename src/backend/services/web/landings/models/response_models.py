"""
Модели ответов для API endpoints Landings.
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class MainPageItemResponseModel(BaseModel):
    """Модель для item в ответе main-page."""
    
    id: int = Field(..., description="ID item")
    title: str = Field(..., description="Заголовок")
    url: Optional[str] = Field(None, description="URL")
    photo_url: Optional[str] = Field(None, alias="photoUrl", description="URL фотографии")
    extra: Dict[str, Any] = Field(default_factory=dict, description="Дополнительные данные")

    class Config:
        populate_by_name = True


class UpdateMainPageResponseModel(BaseModel):
    """Модель успешного ответа при обновлении main-page."""
    
    id: int = Field(..., description="ID главной страницы")
    title: str = Field(..., description="Заголовок")
    subtitle: str = Field(..., description="Подзаголовок")
    type: str = Field(..., description="Тип")
    photo_desktop_url: Optional[str] = Field(None, alias="photoDesktopUrl", description="URL фотографии для десктопа")
    photo_mobile_url: Optional[str] = Field(None, alias="photoMobileUrl", description="URL фотографии для мобиля")
    extra: Dict[str, Any] = Field(default_factory=dict, description="Дополнительные данные")
    items: List[MainPageItemResponseModel] = Field(default_factory=list, description="Список items")

    class Config:
        populate_by_name = True


class ErrorDetailResponseModel(BaseModel):
    """Модель для детали ошибки."""
    
    field: str = Field(..., description="Поле, в котором произошла ошибка")
    message: str = Field(..., description="Сообщение об ошибке")


class BadRequestResponseModel(BaseModel):
    """Модель ответа при ошибке валидации (400)."""
    
    detail: str = Field(..., description="Описание ошибки")
    errors: Optional[List[ErrorDetailResponseModel]] = Field(None, description="Список ошибок")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Validation error",
                "errors": [
                    {
                        "field": "title",
                        "message": "Это поле обязательно."
                    }
                ]
            }
        }


class ForbiddenResponseModel(BaseModel):
    """Модель ответа при отсутствии авторизации (403)."""
    
    detail: str = Field(..., description="Причина отказа в доступе")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Authentication credentials were not provided."
            }
        }


class ServerErrorResponseModel(BaseModel):
    """Модель ответа при внутренней ошибке сервера (500)."""
    
    detail: str = Field(..., description="Описание внутренней ошибки")
    request_id: Optional[str] = Field(None, alias="requestId", description="ID запроса для трекинга")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "detail": "Internal server error",
                "requestId": "abc-123-def"
            }
        }
