"""
Модели пакета Landings.
"""

from src.backend.services.web.landings.models.request_models import (
    MainPageItemRequestModel,
    UpdateMainPageRequestModel,
)
from src.backend.services.web.landings.models.response_models import (
    MainPageItemResponseModel,
    UpdateMainPageResponseModel,
    ErrorDetailResponseModel,
    BadRequestResponseModel,
    ForbiddenResponseModel,
    ServerErrorResponseModel,
)

__all__ = [
    "MainPageItemRequestModel",
    "UpdateMainPageRequestModel",
    "MainPageItemResponseModel",
    "UpdateMainPageResponseModel",
    "ErrorDetailResponseModel",
    "BadRequestResponseModel",
    "ForbiddenResponseModel",
    "ServerErrorResponseModel",
]
