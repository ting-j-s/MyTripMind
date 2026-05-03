# services模块 - 业务逻辑层
from .aigc_service import AIGCService, get_aigc_service, generate_mock_animation

__all__ = [
    'AIGCService',
    'get_aigc_service',
    'generate_mock_animation',
]
