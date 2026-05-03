"""
用户模型
"""

from typing import List, Dict
import hashlib
from .base import BaseModel


class User(BaseModel):
    """
    用户模型

    属性:
        id: 用户ID
        username: 用户名
        password_hash: 密码哈希
        interests: 兴趣标签列表
        favorites: 收藏的景点ID列表
        visited: 去过的景点ID列表
        create_time: 创建时间
    """

    def __init__(self, id: str, username: str, password: str = '',
                 interests: List[str] = None,
                 favorites: List[str] = None,
                 visited: List[str] = None,
                 create_time: str = None,
                 password_hash: str = None,
                 **kwargs):
        super().__init__(id, **kwargs)
        self.username = username
        # 优先使用传入的password_hash，否则从password计算
        if password_hash:
            self.password_hash = password_hash
        elif password:
            self.password_hash = self._hash_password(password)
        else:
            self.password_hash = ''
        self.interests = interests or []
        self.favorites = favorites or []
        self.visited = visited or []
        self.create_time = create_time

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        简单哈希密码（实际应用应使用更安全的方法）
        """
        return hashlib.md5(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        """验证密码"""
        return self.password_hash == self._hash_password(password)

    def add_interest(self, interest: str):
        """添加兴趣标签"""
        if interest not in self.interests:
            self.interests.append(interest)

    def add_favorite(self, attraction_id: str):
        """收藏景点"""
        if attraction_id not in self.favorites:
            self.favorites.append(attraction_id)

    def remove_favorite(self, attraction_id: str):
        """取消收藏"""
        if attraction_id in self.favorites:
            self.favorites.remove(attraction_id)

    def add_visited(self, attraction_id: str):
        """添加已访问"""
        if attraction_id not in self.visited:
            self.visited.append(attraction_id)

    @classmethod
    def from_dict(cls, data: Dict):
        """从字典创建用户"""
        if not data:
            return None
        # 优先使用明文password，否则使用已存储的password_hash
        password = data.get('password', '')
        password_hash = data.get('password_hash', '')
        if not password and password_hash:
            # 如果没有明文密码但有哈希，使用特殊标记避免__init__重新计算
            kwargs = {
                'username': data.get('username', ''),
                'interests': data.get('interests', []),
                'favorites': data.get('favorites', []),
                'visited': data.get('visited', []),
                'create_time': data.get('create_time'),
                'password_hash': password_hash
            }
            return cls(id=data.get('id', ''), **kwargs)
        return cls(
            id=data.get('id', ''),
            username=data.get('username', ''),
            password=password,
            interests=data.get('interests', []),
            favorites=data.get('favorites', []),
            visited=data.get('visited', []),
            create_time=data.get('create_time'),
            password_hash=password_hash
        )

    def to_dict(self) -> Dict:
        result = super().to_dict()
        # 移除明文密码
        if 'password' in result:
            del result['password']
        return result
