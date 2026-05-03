"""
道路模型
"""

from typing import List, Dict
from .base import BaseModel


class Road(BaseModel):
    """
    道路模型

    属性:
        id: 道路ID
        from_node: 起点节点ID
        to_node: 终点节点ID
        distance: 距离（米）
        ideal_speed: 理想速度（km/h）
        congestion: 拥挤度（0-1，越大越堵）
        road_types: 允许的交通方式列表
        floor: 楼层（室内导航用，0表示室外）
    """

    ROAD_TYPES = ['步行', '自行车', '电瓶车']

    def __init__(self, id: str,
                 from_node: str, to_node: str,
                 distance: float,
                 ideal_speed: float = 5.0,
                 congestion: float = 1.0,
                 road_types: List[str] = None,
                 floor: int = 0,
                 **kwargs):
        super().__init__(id, **kwargs)
        self.from_node = from_node
        self.to_node = to_node
        self.distance = distance
        self.ideal_speed = ideal_speed
        self.congestion = congestion
        self.road_types = road_types or ['步行']
        self.floor = floor

    @classmethod
    def from_dict(cls, data: Dict):
        if not data:
            return None
        return cls(
            id=data.get('id', ''),
            from_node=data.get('from', ''),
            to_node=data.get('to', ''),
            distance=data.get('distance', 0),
            ideal_speed=data.get('ideal_speed', 5.0),
            congestion=data.get('congestion', 1.0),
            road_types=data.get('road_types', ['步行']),
            floor=data.get('floor', 0)
        )

    def get_travel_time(self, transport: str = '步行') -> float:
        """
        计算通行时间（秒）

        公式：时间 = 距离 / 真实速度
        真实速度 = 拥挤度 × 理想速度
        """
        if transport not in self.road_types:
            return float('inf')  # 不允许该交通方式

        real_speed = self.congestion * self.ideal_speed  # km/h
        time = (self.distance / 1000) / real_speed * 3600  # 转换为秒
        return time

    def supports_transport(self, transport: str) -> bool:
        """检查是否支持某种交通方式"""
        return transport in self.road_types

    @staticmethod
    def is_valid_road_type(road_type: str) -> bool:
        """检查道路类型是否有效"""
        return road_type in Road.ROAD_TYPES
