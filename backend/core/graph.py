"""
图(Graph)的实现 - 使用邻接表存储
图是路线规划的基础数据结构
支持有向图和无向图
"""

from typing import Dict, List, Tuple, Optional, Any


class Graph:
    """
    图结构 - 邻接表实现

    适用场景：
    - 校园/景区道路网络
    - 室内导航（楼层、房间）
    - 公交/地铁线路

    存储方式：邻接表（Adjacency List）
    - 优点：节省空间，适合稀疏图（边少节点多）
    - 缺点：边的查找需要遍历
    """

    def __init__(self, directed=False):
        """
        初始化图

        参数:
            directed: 是否为有向图，默认无向图
        """
        self._adj = {}  # 邻接表：{节点ID: [(邻居, 边权重), ...]}
        self._nodes = set()  # 所有节点
        self._edges = []  # 所有边
        self.directed = directed

    def add_node(self, node_id: str, data: Any = None):
        """
        添加节点

        参数:
            node_id: 节点唯一标识
            data: 节点附带的数据（如景点名称、坐标等）
        """
        if node_id not in self._adj:
            self._adj[node_id] = []
            self._nodes.add(node_id)
        if data is not None:
            if not hasattr(self, '_node_data'):
                self._node_data = {}
            self._node_data[node_id] = data

    def add_edge(self, from_node: str, to_node: str,
                 distance: float = 1.0,
                 time: float = None,
                 road_types: List[str] = None,
                 **attrs):
        """
        添加边

        参数:
            from_node: 起点节点ID
            to_node: 终点节点ID
            distance: 距离（米）
            time: 时间（秒），如果不指定则根据distance和默认速度计算
            road_types: 允许的交通方式，如 ["步行", "自行车"]
            **attrs: 其他属性，如 congestion（拥挤度）
        """
        # 确保节点存在
        self.add_node(from_node)
        self.add_node(to_node)

        # 默认时间计算：假设步行速度5km/h
        if time is None:
            time = (distance / 1000) / 5 * 3600  # 秒

        if road_types is None:
            road_types = ["步行"]

        edge = {
            'from': from_node,
            'to': to_node,
            'distance': distance,
            'time': time,
            'road_types': road_types,
            **attrs
        }

        self._edges.append(edge)

        # 邻接表添加
        self._adj[from_node].append({
            'node': to_node,
            **edge
        })

        # 无向图需要添加反向边
        if not self.directed:
            reverse_edge = {
                'from': to_node,
                'to': from_node,
                'distance': distance,
                'time': time,
                'road_types': road_types,
                **attrs
            }
            self._adj[to_node].append({
                'node': from_node,
                **reverse_edge
            })

    def get_neighbors(self, node_id: str) -> List[Dict]:
        """获取某节点的所有邻居"""
        return self._adj.get(node_id, [])

    def get_node_data(self, node_id: str) -> Any:
        """获取节点的附带数据"""
        if hasattr(self, '_node_data'):
            return self._node_data.get(node_id)
        return None

    def node_exists(self, node_id: str) -> bool:
        """检查节点是否存在"""
        return node_id in self._nodes

    def get_all_nodes(self) -> List[str]:
        """获取所有节点ID"""
        return list(self._nodes)

    def get_all_edges(self) -> List[Dict]:
        """获取所有边"""
        return self._edges

    def node_count(self) -> int:
        """节点数量"""
        return len(self._nodes)

    def edge_count(self) -> int:
        """边数量"""
        return len(self._edges)

    def get_edge(self, from_node: str, to_node: str) -> Optional[Dict]:
        """
        获取两点之间的边信息
        """
        for edge in self._adj.get(from_node, []):
            if edge['node'] == to_node:
                return edge
        return None

    def __repr__(self):
        return f"Graph(nodes={self.node_count()}, edges={self.edge_count()}, directed={self.directed})"

    def __str__(self):
        lines = [f"Graph: {self.node_count()} nodes, {self.edge_count()} edges"]
        for node in self._nodes:
            neighbors = self._adj.get(node, [])
            if neighbors:
                neighbor_str = ", ".join(
                    f"{n['node']}(d={n['distance']:.0f}m)" for n in neighbors
                )
                lines.append(f"  {node} -> [{neighbor_str}]")
        return "\n".join(lines)


class IndoorGraph(Graph):
    """
    室内导航专用图 - 支持楼层信息

    特殊节点类型：
    - 入口节点（entrance）
    - 电梯节点（elevator）
    - 房间节点（room）
    """

    def __init__(self):
        super().__init__(directed=False)
        self._floor_nodes = {}  # {楼层: [节点列表]}

    def add_room(self, building_id: str, floor: int, room_id: str,
                 x: float, y: float, data: Dict = None):
        """
        添加房间节点

        参数:
            building_id: 建筑ID
            floor: 楼层
            room_id: 房间号
            x, y: 坐标
        """
        node_id = f"{building_id}_F{floor}_{room_id}"
        node_data = {
            'type': 'room',
            'building': building_id,
            'floor': floor,
            'room': room_id,
            'x': x,
            'y': y,
            **(data or {})
        }
        self.add_node(node_id, node_data)

        if floor not in self._floor_nodes:
            self._floor_nodes[floor] = []
        self._floor_nodes[floor].append(node_id)

    def add_elevator(self, building_id: str, elevator_id: str, x: float, y: float):
        """
        添加电梯节点（可跨楼层）
        """
        node_id = f"{building_id}_ELEVATOR_{elevator_id}"
        node_data = {
            'type': 'elevator',
            'building': building_id,
            'x': x,
            'y': y
        }
        self.add_node(node_id, node_data)

        for floor in self._floor_nodes:
            if building_id in str(self._floor_nodes[floor]):
                if floor not in self._floor_nodes:
                    self._floor_nodes[floor] = []
                if node_id not in self._floor_nodes[floor]:
                    self._floor_nodes[floor].append(node_id)

    def add_entrance(self, building_id: str, entrance_id: str, x: float, y: float):
        """添加入口节点"""
        node_id = f"{building_id}_ENTRANCE_{entrance_id}"
        node_data = {
            'type': 'entrance',
            'building': building_id,
            'x': x,
            'y': y
        }
        self.add_node(node_id, node_data)

    def get_floor_nodes(self, floor: int) -> List[str]:
        """获取某楼层的所有节点"""
        return self._floor_nodes.get(floor, [])

    def get_elevators(self, building_id: str) -> List[str]:
        """获取某建筑的所有电梯"""
        result = []
        for node_id in self._nodes:
            data = self.get_node_data(node_id)
            if data and data.get('type') == 'elevator' and data.get('building') == building_id:
                result.append(node_id)
        return result


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("图结构测试")
    print("=" * 50)

    # 创建简单道路图
    print("\n1. 创建简单道路图:")
    g = Graph(directed=False)

    # 添加节点（景点）
    g.add_node("图书馆", {'name': '图书馆', 'x': 100, 'y': 200})
    g.add_node("食堂", {'name': '食堂', 'x': 200, 'y': 150})
    g.add_node("教学楼", {'name': '教学楼', 'x': 300, 'y': 250})
    g.add_node("体育馆", {'name': '体育馆', 'x': 400, 'y': 200})

    # 添加边（道路）
    g.add_edge("图书馆", "食堂", distance=150, time=180, road_types=["步行", "自行车"])
    g.add_edge("食堂", "教学楼", distance=200, time=240, road_types=["步行", "自行车"])
    g.add_edge("教学楼", "体育馆", distance=180, time=216, road_types=["步行"])
    g.add_edge("图书馆", "体育馆", distance=350, time=420, road_types=["步行"])

    print(g)
    print(f"\n节点数: {g.node_count()}, 边数: {g.edge_count()}")

    # 获取邻居
    print("\n2. 邻居查询:")
    neighbors = g.get_neighbors("图书馆")
    for n in neighbors:
        print(f"  图书馆 -> {n['node']}: 距离{n['distance']}米")

    # 获取边信息
    print("\n3. 边信息查询:")
    edge = g.get_edge("图书馆", "食堂")
    print(f"  图书馆->食堂: {edge}")

    # 节点数据
    print("\n4. 节点数据:")
    data = g.get_node_data("图书馆")
    print(f"  图书馆数据: {data}")

    print("\n[SUCCESS] Graph test passed!")
