"""
景点/校园模型
"""

from typing import List, Dict
from .base import BaseModel


class Attraction(BaseModel):
    """
    景点/校园模型

    属性:
        id: 景点ID
        name: 名称
        type: 类型（景区/校园）
        campus_id: 所属校园ID（如果是校园内景点）
        x, y: 坐标
        heat: 热度（浏览量）
        rating: 评分（1-5）
        tags: 标签列表
        description: 简介
        image_url: 图片URL
    """

    def __init__(self, id: str, name: str,
                 type: str = '景区',
                 campus_id: str = None,
                 x: float = 0, y: float = 0,
                 heat: int = 0, rating: float = 5.0,
                 tags: List[str] = None,
                 description: str = '',
                 image_url: str = None,
                 **kwargs):
        super().__init__(id, **kwargs)
        self.name = name
        self.type = type
        self.campus_id = campus_id
        self.x = x
        self.y = y
        self.heat = heat
        self.rating = rating
        self.tags = tags or []
        self.description = description
        self.image_url = image_url

    @classmethod
    def from_dict(cls, data: Dict):
        if not data:
            return None
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            type=data.get('type', '景区'),
            campus_id=data.get('campus_id'),
            x=data.get('x', 0),
            y=data.get('y', 0),
            heat=data.get('heat', 0),
            rating=data.get('rating', 5.0),
            tags=data.get('tags', []),
            description=data.get('description', ''),
            image_url=data.get('image_url')
        )

    def increment_heat(self):
        """增加热度"""
        self.heat += 1

    def update_rating(self, new_rating: float):
        """更新评分（平均值方式）"""
        # 简单实现：每次新评分直接更新
        self.rating = new_rating

    def has_tag(self, tag: str) -> bool:
        """检查是否有某标签"""
        return tag in self.tags


class Campus(BaseModel):
    """
    校园/景区模型（顶层）
    """

    def __init__(self, id: str, name: str,
                 type: str = '校园',
                 x: float = 0, y: float = 0,
                 description: str = '',
                 **kwargs):
        super().__init__(id, **kwargs)
        self.name = name
        self.type = type
        self.x = x
        self.y = y
        self.description = description

    @classmethod
    def from_dict(cls, data: Dict):
        if not data:
            return None
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            type=data.get('type', '校园'),
            x=data.get('x', 0),
            y=data.get('y', 0),
            description=data.get('description', '')
        )
