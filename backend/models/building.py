"""
建筑模型（室内导航用）
"""

from typing import List, Dict
from .base import BaseModel


class Building(BaseModel):
    """
    建筑模型（用于室内导航）

    属性:
        id: 建筑ID
        name: 名称
        type: 类型（教学楼/宿舍/食堂等）
        campus_id: 所属校区ID
        x, y: 坐标
        floors: 楼层数
        rooms: 房间列表
        elevators: 电梯列表
        entrances: 入口列表
    """

    def __init__(self, id: str, name: str,
                 type: str = '教学楼',
                 campus_id: str = None,
                 x: float = 0, y: float = 0,
                 floors: int = 1,
                 rooms: List[str] = None,
                 elevators: List[str] = None,
                 entrances: List[str] = None,
                 **kwargs):
        super().__init__(id, **kwargs)
        self.name = name
        self.type = type
        self.campus_id = campus_id
        self.x = x
        self.y = y
        self.floors = floors
        self.rooms = rooms or []
        self.elevators = elevators or []
        self.entrances = entrances or []

    @classmethod
    def from_dict(cls, data: Dict):
        if not data:
            return None
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            type=data.get('type', '教学楼'),
            campus_id=data.get('campus_id'),
            x=data.get('x', 0),
            y=data.get('y', 0),
            floors=data.get('floors', 1),
            rooms=data.get('rooms', []),
            elevators=data.get('elevators', []),
            entrances=data.get('entrances', [])
        )

    def get_all_nodes(self) -> List[str]:
        """获取建筑内所有导航节点ID"""
        nodes = []
        # 入口节点
        for entrance in self.entrances:
            nodes.append(f"{self.id}_ENTRANCE_{entrance}")
        # 电梯节点
        for elevator in self.elevators:
            nodes.append(f"{self.id}_ELEVATOR_{elevator}")
        # 房间节点（每层）
        for floor in range(1, self.floors + 1):
            for room in self.rooms:
                nodes.append(f"{self.id}_F{floor}_{room}")
        return nodes
