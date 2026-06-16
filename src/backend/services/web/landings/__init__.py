"""
Пакет Landings сервиса.
"""

from src.backend.services.web.landings.adapter import LandingsAdapter
from src.backend.services.web.landings.service import LandingsService

__all__ = [
    "LandingsAdapter",
    "LandingsService",
]
