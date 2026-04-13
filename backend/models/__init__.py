# models模块 - 数据模型
from .base import BaseModel
from .user import User
from .attraction import Attraction, Campus
from .building import Building
from .facility import Facility
from .road import Road
from .diary import Diary
from .food import Food

__all__ = [
    'BaseModel',
    'User',
    'Attraction', 'Campus',
    'Building',
    'Facility',
    'Road',
    'Diary',
    'Food',
]
