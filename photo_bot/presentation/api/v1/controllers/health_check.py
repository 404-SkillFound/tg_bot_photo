from datetime import datetime

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get('/', tags=['Health'])
async def root() -> dict:
    """Корневой endpoint для проверки работы API."""
    return {
        'message': '🤖 Photo Editor Bot API работает!',
        'status': 'success',
        'version': '1.0.0',
    }


@router.get('/health', tags=['Health'])
async def health_check() -> JSONResponse:
    """Проверка здоровья сервиса."""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'status': 'healthy',
            'message': '✅ Сервис работает',
            'timestamp': datetime.now().isoformat(),
        },
    )
