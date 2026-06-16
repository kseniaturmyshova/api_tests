"""
Гайд по использованию тестов Landings API.

Этот документ описывает структуру, фикстуры и примеры использования тестов
для Landings API, в частности для endpoint'а /service/landings/api/v1/main-page
"""

# 📌 Структура тестов Landings API

## Основные компоненты

### 1. Модели (src/backend/services/web/landings/models/)

#### Request Models (request_models.py)
- `MainPageItemRequestModel` - модель для одного item
- `UpdateMainPageRequestModel` - модель для обновления main-page

```python
from src.backend.services.web.landings.models import UpdateMainPageRequestModel

# Создание модели с валидацией
request_data = UpdateMainPageRequestModel(
    title="Как классно провести лето✈️",
    subtitle="Идеи для впечатлений",
    photoDesktopId=2261,
    photoMobileId=2260,
    type="seasons",
    extra={"color": "#EBFAF5"},
    items=[...]
)

# Преобразование в словарь с alias (для API)
json_data = request_data.model_dump(by_alias=True)
```

#### Response Models (response_models.py)
- `UpdateMainPageResponseModel` - ответ при успехе (200)
- `BadRequestResponseModel` - ошибка валидации (400)
- `ForbiddenResponseModel` - нет авторизации (403)
- `ServerErrorResponseModel` - внутренняя ошибка (500)

### 2. Адаптер (adapter.py)

HTTP клиент для работы с Landings endpoints.

```python
from src.backend.services.web.landings import LandingsAdapter

adapter = LandingsAdapter(host="https://experience.staging.k8s-dev.tripster.ru")

# PUT запрос
response = adapter.update_main_page(
    headers={"Authorization": "Bearer token"},
    json={"title": "...", "subtitle": "..."}
)

# GET запрос
response = adapter.get_main_page(headers=headers)
```

### 3. Сервис (service.py)

Бизнес-логика с валидацией и Allure интеграцией.

```python
from src.backend.services.web.landings import LandingsService

service = LandingsService(adapter=adapter)

# Обновить main-page
result = service.update_main_page(
    update_data=request_data,
    headers=headers
)
# Возвращает UpdateMainPageResponseModel

# Получить main-page
result = service.get_main_page(headers=headers)
```

### 4. Фикстуры (tests/web/landings/conftest.py)

#### Основные фикстуры

```python
@pytest.fixture
def landings_adapter():
    """LandingsAdapter для работы с API."""
    return LandingsAdapter(host=TestConfig.BASE_API_URL)

@pytest.fixture
def landings_service(landings_adapter):
    """LandingsService с бизнес-логикой."""
    return LandingsService(adapter=landings_adapter)

@pytest.fixture
def update_main_page_data():
    """Полные тестовые данные с Faker."""
    # Генерирует случайный title, subtitle, items и т.д.
    # Реалистичные данные с эмодзи

@pytest.fixture
def update_main_page_data_minimal():
    """Минимальные тестовые данные."""
    # Только обязательные поля
```

#### UpdateMainPageDataGenerator

Класс для генерации реалистичных данных:

```python
from tests.web.landings.conftest import UpdateMainPageDataGenerator

# Генерировать заголовок с эмодзи
title = UpdateMainPageDataGenerator.generate_title()
# Результат: "Как классно провести лето✈️"

# Генерировать подзаголовок
subtitle = UpdateMainPageDataGenerator.generate_subtitle()
# Результат: "Идеи для впечатлений в этом сезоне"

# Генерировать items (по умолчанию 5 штук)
items = UpdateMainPageDataGenerator.generate_items(count=3)

# Генерировать extra с цветом
extra = UpdateMainPageDataGenerator.generate_extra()
# Результат: {"color": "#EBFAF5"}
```

### 5. Smoke тесты (tests/web/landings/test_main_page_smoke.py)

```python
@pytest.mark.smoke
def test_update_main_page_with_valid_data(
    landings_adapter,
    auth_headers,
    update_main_page_data
):
    """Happy path: обновление main-page с корректными данными."""
    response = landings_adapter.update_main_page(
        headers=auth_headers,
        json=update_main_page_data.model_dump(by_alias=True)
    )
    
    with allure.step("Проверить статус код 200"):
        validate_response(response=response, expected_status_code=HTTPStatus.OK)
```

---

## 🚀 Как использовать в своих тестах

### Пример 1: Простой тест с адаптером

```python
import pytest
from http import HTTPStatus
import allure

@pytest.mark.smoke
def test_update_main_page_simple(landings_adapter, auth_headers, update_main_page_data):
    """Обновить main-page."""
    response = landings_adapter.update_main_page(
        headers=auth_headers,
        json=update_main_page_data.model_dump(by_alias=True)
    )
    
    assert response.status_code == HTTPStatus.OK
    assert "title" in response.json()
```

### Пример 2: Тест с сервисом

```python
@pytest.mark.smoke
@allure.title("Обновление main-page через сервис")
def test_update_main_page_with_service(landings_service, auth_headers, update_main_page_data):
    """Обновить main-page используя сервис."""
    result = landings_service.update_main_page(
        update_data=update_main_page_data,
        headers=auth_headers
    )
    
    assert result.id > 0
    assert result.title == update_main_page_data.title
    assert result.subtitle == update_main_page_data.subtitle
```

### Пример 3: Тест с кастомными данными

```python
@pytest.mark.regression
def test_update_main_page_with_custom_data(landings_adapter, auth_headers):
    """Обновить main-page с кастомными данными."""
    from tests.web.landings.conftest import UpdateMainPageDataGenerator
    
    custom_data = UpdateMainPageRequestModel(
        title="Моя тестовая страница",
        subtitle="Тестовое описание",
        photoDesktopId=9999,
        photoMobileId=9998,
        type="experiences",
        extra={"color": "#FF0000"},
        items=UpdateMainPageDataGenerator.generate_items(count=2)
    )
    
    response = landings_adapter.update_main_page(
        headers=auth_headers,
        json=custom_data.model_dump(by_alias=True)
    )
    
    assert response.status_code == HTTPStatus.OK
```

### Пример 4: Параметризованный тест

```python
@pytest.mark.regression
@pytest.mark.parametrize(
    "landing_type",
    ["experiences", "seasons", "destinations"]
)
def test_update_main_page_with_different_types(
    landings_adapter,
    auth_headers,
    update_main_page_data,
    landing_type
):
    """Обновить main-page с разными типами."""
    data = update_main_page_data
    data.type = landing_type
    
    response = landings_adapter.update_main_page(
        headers=auth_headers,
        json=data.model_dump(by_alias=True)
    )
    
    assert response.status_code == HTTPStatus.OK
    assert response.json()["type"] == landing_type
```

---

## ⚙️ Конфигурация

Все тесты используют `TestConfig.BASE_API_URL` из `config.py`:

```python
class TestConfig:
    BASE_API_URL = os.getenv("BASE_API_URL", "https://experience.staging.k8s-dev.tripster.ru")
```

Для изменения окружения установи переменную окружения:

```bash
export BASE_API_URL=https://your-api-url.com
pytest tests/web/landings/
```

---

## 🏃‍♂️ Запуск тестов

### Запустить все smoke тесты Landings

```bash
pytest tests/web/landings/test_main_page_smoke.py -m smoke -v
```

### Запустить конкретный тест

```bash
pytest tests/web/landings/test_main_page_smoke.py::test_update_main_page_with_valid_data -v
```

### Запустить с Allure отчетом

```bash
pytest tests/web/landings/ --alluredir=./allure-results
allure serve ./allure-results
```

### Запустить параллельно (xdist)

```bash
pytest tests/web/landings/ -n auto
```

---

## 📋 Чек-лист перед использованием

✅ **Убедись, что:**

1. [ ] Есть фикстура `auth_headers` в `tests/conftest.py`
   - Должна возвращать заголовки с авторизацией
   - Пример:
     ```python
     @pytest.fixture
     def auth_headers(auth_service):
         token = auth_service.register_user(...)
         return {"Authorization": f"Bearer {token}"}
     ```

2. [ ] HTTPClient поддерживает методы `put()` и `get()`

3. [ ] Переменные окружения настроены:
   - `BASE_API_URL` (опционально, есть дефолт)
   - `RECAPTCHA_TOKEN` (если нужно для регистрации)

4. [ ] Установлены зависимости:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🐛 Отладка

### Просмотреть детали запроса/ответа в Allure

Все HTTP запросы автоматически логируются в Allure с:
- cURL командой
- Временем выполнения
- Статус кодом
- Телом ответа

### Добавить кастомный лог

```python
import allure

with allure.step("Описание шага"):
    allure.attach(
        str(response.json()),
        "Response JSON",
        allure.attachment_type.JSON
    )
```

---

## 📚 Полезные ссылки

- [Документация Pydantic](https://docs.pydantic.dev/)
- [Документация Pytest](https://docs.pytest.org/)
- [Документация Allure](https://docs.qameta.io/allure/)
- [Faker документация](https://faker.readthedocs.io/)

---

## ❓ FAQ

**Q: Как изменить количество items в фикстуре?**

A: Используй параметр `count` в фикстуре:
```python
@pytest.fixture
def custom_items():
    from tests.web.landings.conftest import UpdateMainPageDataGenerator
    return UpdateMainPageDataGenerator.generate_items(count=10)
```

**Q: Как создать тест без авторизации?**

A: Передай пустой словарь или None:
```python
response = landings_adapter.get_main_page(headers={})
# Ожидаем 403 Forbidden
```

**Q: Как добавить новый тип данных в генератор?**

A: Отредактируй `UpdateMainPageDataGenerator` в `conftest.py`:
```python
TYPES = ["experiences", "seasons", "destinations", "my_new_type"]
```

---

Все готово! 🚀 Тесты готовы к использованию!
"""
