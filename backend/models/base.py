"""
数据模型基类
所有数据模型都继承自这个基类
"""

from typing import Dict, Any
import json


class BaseModel:
    """
    数据模型基类

    提供：
    - 对象与字典的相互转换
    - JSON序列化/反序列化
    """

    def __init__(self, id: str, **kwargs):
        self.id = id
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict:
        """
        将模型转换为字典
        """
        result = {'id': self.id}
        for key, value in self.__dict__.items():
            if key.startswith('_'):
                continue
            if isinstance(value, (str, int, float, bool, list, dict, type(None))):
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict) -> 'BaseModel':
        """
        从字典创建模型实例
        """
        if not data:
            return None
        id = data.get('id', '')
        kwargs = {k: v for k, v in data.items() if k != 'id'}
        return cls(id=id, **kwargs)

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """从JSON字符串创建实例"""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"
