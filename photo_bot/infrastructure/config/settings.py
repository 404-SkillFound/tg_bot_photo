"""МОДУЛЬ НАСТРОЕК ПРИЛОЖЕНИЯ.

Централизованное управление всеми настройками проекта
"""

from typing import List, Optional

from dotenv import load_dotenv
from pydantic import Field, validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Настройки приложения."""

    # ==================== 🔐 API КЛЮЧИ И ТОКЕНЫ ====================
    TELEGRAM_BOT_TOKEN: str = Field(
        default=...,
        description='Токен бота в Telegram',
        example='1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi',
    )

    PHOTOROOM_API_KEY: str = Field(
        default=...,
        description='API ключ для сервиса Photoroom',
        example='photoroom_apikey_1234567890abcdef',
    )
    SECRET_TOKEN: str = Field(
        default='my_secret_token_123',
        description='Секретный токен для верификации вебхуков',
        example='my_super_secret_token_2025',
    )

    # ==================== 🌐 СЕРВЕР И СЕТЬ =========================
    HOST: str = Field(
        default='127.0.0.1',
        description='Хост для запуска сервера',
        example='0.0.0.0 или 127.0.0.1',
    )
    PORT: int = Field(
        default=8000,
        description='Порт для запуска сервера',
        ge=1000, le=65535,  # Валидация: порт от 1000 до 65535
    )
    WEBHOOK_URL: Optional[str] = Field(
        default=None,
        description='URL для вебхука Telegram (для продакшена)',
        example='https://yourdomain.com',
    )

    # ==================== 🖼️ НАСТРОЙКИ ИЗОБРАЖЕНИЙ =================
    MAX_IMAGE_SIZE_MB: int = Field(
        default=10,
        description='Максимальный размер изображения в МБ',
        ge=1, le=50,  # От 1 до 50 МБ
    )
    DEFAULT_IMAGE_QUALITY: int = Field(
        default=85,
        description='Качество изображения по умолчанию (0-100)',
        ge=1, le=100,
    )
    SUPPORTED_FORMATS: List[str] = Field(
        default=['JPEG', 'PNG', 'WEBP'],
        description='Поддерживаемые форматы изображений',
    )

    # ==================== ⏱️ ТАЙМАУТЫ И ЛИМИТЫ =====================
    REQUEST_TIMEOUT: int = Field(
        default=30,
        description='Таймаут HTTP запросов в секундах',
        ge=5, le=120,
    )
    SESSION_TTL: int = Field(
        default=3600,
        description='Время жизни сессии в секундах (1 час)',
        ge=300, le=86400,  # От 5 минут до 24 часов
    )
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=20,
        description='Лимит запросов в минуту на пользователя',
        ge=1, le=1000,
    )

    # ==================== 🎨 НАСТРОЙКИ ОБРАБОТКИ ===================
    ENABLE_PHOTOROOM: bool = Field(
        default=True,
        description='Включить обработку через Photoroom API',
    )

    ENABLE_PILLOW: bool = Field(
        default=True,
        description='Включить локальную обработку через Pillow',
    )
    DEFAULT_PROCESSOR: str = Field(
        default='photoroom',
        description='Процессор по умолчанию',
        pattern='^(photoroom|pillow)$',
    )

    # ==================== 📝 ЛОГИРОВАНИЕ ===========================
    LOG_LEVEL: str = Field(
        default='INFO',
        description='Уровень логирования',
        pattern='^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$',
    )
    ENABLE_FILE_LOGGING: bool = Field(
        default=True,
        description='Сохранять логи в файл',
    )

    # ==================== 🔧 ВАЛИДАТОРЫ ============================

    @validator('TELEGRAM_BOT_TOKEN')
    def validate_telegram_token(
            cls, v: Optional[str],  # noqa: N805
    ) -> str:
        """Валидация токена Telegram бота."""
        if not v or v == 'your_telegram_bot_token_here':
            raise ValueError(
                '❌ TELEGRAM_BOT_TOKEN не настроен. '
                'Проверьте .env файл',
            )
        if ':' not in v or len(v) < 30:
            raise ValueError('❌ Неверный формат TELEGRAM_BOT_TOKEN')
        return v

    @validator('PHOTOROOM_API_KEY')
    def validate_photoroom_key(
            cls, v: Optional[str],  # noqa: N805
    ) -> str:
        """Валидация ключа Photoroom API."""
        if not v or v == 'your_photoroom_api_key_here':
            raise ValueError(
                '❌ PHOTOROOM_API_KEY не настроен. '
                'Проверьте .env файл',
            )
        return v

    @validator('WEBHOOK_URL')
    def validate_webhook_url(
            cls, v: Optional[str],  # noqa: N805
    ) -> str | None:
        """Валидация URL вебхука."""
        if v and v.startswith('https://yourdomain'):
            return None  # Игнорируем пример из .env.example
        return v

    @validator('DEFAULT_PROCESSOR')
    def validate_default_processor(
            cls, v: Optional[str], values: dict[str, bool],  # noqa: N805
    ) -> str:
        """Валидация процессора по умолчанию."""
        if v == 'photoroom' and not values.get(
                'ENABLE_PHOTOROOM',
                True,
        ):
            raise ValueError(
                '❌ Photoroom отключен, но выбран '
                'как процессор по умолчанию',
            )
        if v == 'pillow' and not values.get('ENABLE_PILLOW', True):
            raise ValueError(
                '❌ Pillow отключен, но выбран '
                'как процессор по умолчанию',
            )
        return v

    # ==================== 🎯 СВОЙСТВА ДЛЯ УДОБСТВА =================
    @property
    def is_development(self) -> bool:
        """Проверка, что это режим разработки."""
        return self.HOST in [
            '127.0.0.1',
            'localhost',
        ] or self.PORT in [8000, 8080]

    @property
    def is_production(self) -> bool:
        """Проверка, что это продакшен режим."""
        return (self.WEBHOOK_URL is not None and
                not self.is_development)

    @property
    def max_image_size_bytes(self) -> int:
        """Максимальный размер изображения в байтах."""
        return self.MAX_IMAGE_SIZE_MB * 1024 * 1024

    @property
    def webhook_enabled(self) -> bool:
        """Проверка, включены ли вебхуки."""
        return self.WEBHOOK_URL is not None and self.is_production

    class Config:
        """⚙Конфигурация Pydantic."""

        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
        use_enum_values = True


# ==================== 🎯 ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР И ФУНКЦИИ ============
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """ПОЛУЧЕНИЕ ЭКЗЕМПЛЯРА НАСТРОЕК.

    Гарантирует, что настройки загружаются только один раз
    """
    global _settings_instance

    if _settings_instance is None:
        try:
            _settings_instance = Settings()

            settings_instance = '✅ Настроен' \
                if _settings_instance.TELEGRAM_BOT_TOKEN else '❌ Нет'
            photo_api = '✅ Настроен' \
                if _settings_instance.PHOTOROOM_API_KEY else '❌ Нет'
            webhook = '✅ ' + _settings_instance.WEBHOOK_URL \
                if _settings_instance.WEBHOOK_URL else '❌ Локальный режим'

            print('✅ Настройки приложения успешно загружены')
            print(f'\t🌐 Host: {_settings_instance.HOST}')
            print(f'\t🚪 Port: {_settings_instance.PORT}')
            print(f'\t🤖 Telegram Bot: {settings_instance}')
            print(f'\t🎨 Photoroom API: {photo_api}')
            print(f'\t🌐 Webhook: {webhook}')

        except Exception as e:
            print(f'❌ Ошибка загрузки настроек: {e}')
            print('📋 Проверьте .env файл или переменные окружения')
            raise

    return _settings_instance


def reload_settings() -> Settings:
    """ПЕРЕЗАГРУЗКА НАСТРОЕК.

    Полезно при изменении .env файла во время работы.
    """
    global _settings_instance
    _settings_instance = None
    return get_settings()


# ==================== 🧪 ТЕСТОВЫЕ НАСТРОЙКИ ========================

class TestSettings(Settings):
    """Класс для настроек при тесте."""

    class Config:
        """Настройки для тестов."""

        env_file = '.env.test'
        env_file_encoding = 'utf-8'


def get_test_settings() -> Settings:
    """Получение настроек для тестов."""
    return TestSettings()
