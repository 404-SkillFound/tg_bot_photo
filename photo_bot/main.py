from fastapi import FastAPI

from photo_bot.infrastructure.config.settings import get_settings


def create_application() -> FastAPI:
    """Фабрика для создания приложения."""
    settings = get_settings()
    app = FastAPI(
        title="🤖 Photo Editor Bot API",
        description=("""
        🎨 Telegram бот для обработки фотографий
        Возможности:
        - 🎭 Удаление фона через Photoroom API
        - 🌅 Изменение фона по описанию
        - 📐 Изменение размера изображений
        - 🎨 Применение фильтров (Pillow)
        API:
        - `POST /webhook` - Webhook для Telegram
        - `GET /health` - Проверка здоровья сервиса
        - `GET /set_webhook` - Установка webhook
        """),
        version="1.0.0",
        docs_url='/docs',
        redoc_url='/redoc',
    )
    app.state.settings = settings
    #if settings.is_development:
    #    print('🛠️ Режим разработки')
    #if settings.webhook_enabled:
    #    print(f'🌐 Webhook URL: {settings.WEBHOOK_URL}')
    return app


app = create_application()

# Альтернативный запуск
# if __name__ == "__main__":
#     import uvicorn
#
#     settings = get_settings()
#     uvicorn.run("photo_bot.main:app", reload=True)
