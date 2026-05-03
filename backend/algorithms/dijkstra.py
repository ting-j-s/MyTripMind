"""
Dijkstra最短路径算法实现
用于计算从一个起点到所有其他节点的最短路径
课程要求：必须自己实现，不能直接调用库
"""

from typing import Dict, List, Tuple, Optional
from backend.core.heap import MinHeap, HeapElement


def dijkstra(graph, start: str, end: str = None,
             weight: str = 'distance') -> Dict:
    """
    Dijkstra单源最短路径算法

    时间复杂度: O((V + E) log V)
    - V: 节点数量
    - E: 边数量
    - 使用堆优化，log V来自堆操作

    参数:
        graph: Graph图对象
        start: 起点节点ID
        end: 终点节点ID（可选，不指定则计算到所有节点）
        weight: 权重类型，'distance'（距离）或'time'（时间）

    返回:
        {
            'distances': {节点ID: 最短距离},
            'paths': {节点ID: [路径节点列表]},
            'path': [终点路径列表]（如果指定了end）
        }

    算法步骤:
        1. 初始化：起点距离为0，其他为无穷大
        2. 使用优先队列（最小堆）选择当前最短距离节点
        3. 松弛操作：检查经过该节点是否能缩短到邻居的距离
        4. 重复2-3直到所有节点处理完毕
    """
    # 距离表：节点 -> 最短距离
    distances = {node: float('inf') for node in graph.get_all_nodes()}
    distances[start] = 0

    # 前驱表：节点 -> 前一个节点（用于路径重建）
    predecessors = {node: None for node in graph.get_all_nodes()}

    # 优先队列：(距离, 节点)
    pq = MinHeap()
    pq.push(HeapElement(start, 0))

    # 已访问节点集合
    visited = set()

    while not pq.is_empty():
        # 取出当前最短距离的节点
        current = pq.pop()
        current_node = current.value
        current_dist = current.key

        # 如果已访问，跳过
        if current_node in visited:
            continue

        # 标记为已访问
        visited.add(current_node)

        # 如果已经处理到目标节点，可以提前结束
        if end and current_node == end:
            break

        # 如果当前距离已经大于已知最短距离，跳过
        if current_dist > distances[current_node]:
            continue

        # 检查所有邻居
        for neighbor_info in graph.get_neighbors(current_node):
            neighbor = neighbor_info['node']

            if neighbor in visited:
                continue

            # 计算经过当前节点到邻居的距离
            edge_weight = neighbor_info.get(weight, neighbor_info['distance'])

            # 考虑拥挤度（如果有）
            if 'congestion' in neighbor_info and weight == 'time':
                congestion = neighbor_info['congestion']
                ideal_speed = neighbor_info.get('ideal_speed', 5)  # km/h
                # 真实速度 = 拥挤度 * 理想速度
                real_speed = congestion * ideal_speed
                # 时间 = 距离 / 真实速度（需要转换单位）
                edge_weight = (neighbor_info['distance'] / 1000) / real_speed * 3600

            new_dist = current_dist + edge_weight

            # 如果发现更短的路径
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = current_node
                pq.push(HeapElement(neighbor, new_dist))

    # 重建路径
    paths = {}
    for node in graph.get_all_nodes():
        if distances[node] < float('inf'):
            paths[node] = _reconstruct_path(predecessors, start, node)

    result = {
        'distances': distances,
        'paths': paths
    }

    if end:
        result['path'] = paths.get(end, [])
        result['distance'] = distances.get(end, float('inf'))

    return result


def _reconstruct_path(predecessors: Dict, start: str, end: str) -> List[str]:
    """
    重建从起点到终点的路径

    使用前驱表反向追溯
    """
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = predecessors[current]

    path.reverse()
    return path


def dijkstra_with_constraints(graph, start: str, end: str,
                               transport: str = '步行',
                               weight: str = 'distance') -> Dict:
    """
    Dijkstra最短路径（带交通方式约束）

    参数:
        graph: Graph图对象
        start: 起点
        end: 终点
        transport: 交通方式，'步行'、'自行车'、'电瓶车'
        weight: 'distance' 或 'time'（实际计算时统一按时间）

    返回:
        同dijkstra
    """
    # 交通方式的基础速度（km/h）
    transport_speeds = {
        '步行': 5,
        '自行车': 15,
        '电瓶车': 20,
        '公交': 25,
        '驾车': 40
    }
    base_speed = transport_speeds.get(transport, 5)

    # 时间表（秒）
    times = {node: float('inf') for node in graph.get_all_nodes()}
    times[start] = 0

    # 距离表
    distances = {node: float('inf') for node in graph.get_all_nodes()}
    distances[start] = 0

    # 前驱表
    predecessors = {node: None for node in graph.get_all_nodes()}

    # 优先队列：(时间, 节点)
    pq = MinHeap()
    pq.push(HeapElement(start, 0))

    # 已访问
    visited = set()

    while not pq.is_empty():
        current = pq.pop()
        current_node = current.value
        current_time = current.key

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            break

        if current_time > times[current_node]:
            continue

        # 检查邻居
        for neighbor_info in graph.get_neighbors(current_node):
            neighbor = neighbor_info['node']

            if neighbor in visited:
                continue

            # 检查交通方式是否允许
            road_types = neighbor_info.get('road_types', ['步行'])
            if transport not in road_types:
                continue

            # 计算时间（秒）
            distance = neighbor_info['distance']
            congestion = neighbor_info.get('congestion', 1.0)
            real_speed = base_speed * max(0.3, 1 - congestion * 0.7)
            travel_time = (distance / 1000) / real_speed * 3600

            new_time = current_time + travel_time

            if new_time < times[neighbor]:
                times[neighbor] = new_time
                distances[neighbor] = distances[current_node] + distance
                predecessors[neighbor] = current_node
                pq.push(HeapElement(neighbor, new_time))

    # 重建路径
    path = _reconstruct_path(predecessors, start, end)

    return {
        'path': path,
        'distance': distances.get(end, float('inf')),
        'time': times.get(end, float('inf')),
        'transport': transport,
        'success': times.get(end, float('inf')) < float('inf')
    }


def shortest_path_mixed_transport(graph, start: str, end: str,
                                  allowed_modes: List[str] = None,
                                  ideal_speeds: Dict[str, float] = None) -> Dict:
    """
    混合交通工具最短时间路径算法

    对每条边枚举 allowed_modes 中可用的交通工具，选择使总时间最短的路线。
    时间 = distance / (ideal_speed * congestion)

    参数:
        graph: Graph图对象
        start: 起点节点ID
        end: 终点节点ID
        allowed_modes: 可用交通方式列表，默认 ["walk", "bike", "shuttle"]
        ideal_speeds: 各交通方式的理想速度（km/h），默认速度表

    返回:
        {
            'success': bool,
            'path': [节点ID列表],
            'segments': [{from, to, distance, mode, speed, congestion, time}, ...],
            'total_distance': float,
            'total_time': float,
            'modes_used': [使用的交通方式列表],
            'error': str（如果失败）
        }
    """
    # 默认可用交通方式
    if allowed_modes is None:
        allowed_modes = ['walk', 'bike', 'shuttle']

    # 默认理想速度（km/h）
    if ideal_speeds is None:
        ideal_speeds = {
            'walk': 5,
            'bike': 15,
            'shuttle': 20
        }

    # 检查节点是否存在
    if not graph.node_exists(start):
        return {'success': False, 'error': f'起点节点 {start} 不存在'}
    if not graph.node_exists(end):
        return {'success': False, 'error': f'终点节点 {end} 不存在'}

    # 时间表（秒）
    times = {node: float('inf') for node in graph.get_all_nodes()}
    times[start] = 0

    # 前驱表：(节点, 使用的交通方式)
    predecessors = {node: None for node in graph.get_all_nodes()}
    predecessor_modes = {node: None for node in graph.get_all_nodes()}

    # 优先队列：(时间, 节点)
    pq = MinHeap()
    pq.push(HeapElement(start, 0))

    visited = set()

    while not pq.is_empty():
        current = pq.pop()
        current_node = current.value
        current_time = current.key

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            break

        if current_time > times[current_node]:
            continue

        # 检查邻居
        for neighbor_info in graph.get_neighbors(current_node):
            neighbor = neighbor_info['node']

            if neighbor in visited:
                continue

            distance = neighbor_info.get('distance', 1)
            congestion = neighbor_info.get('congestion', 1.0)
            road_types = neighbor_info.get('road_types', ['walk'])

            # 找到该边允许的所有可用交通方式
            mode_candidates = []
            for mode in allowed_modes:
                # 统一交通方式名称：支持中英文混用
                mode_normalized = _normalize_transport(mode)
                road_type_normalized = [_normalize_transport(rt) for rt in road_types]
                if mode_normalized in road_type_normalized:
                    mode_candidates.append(mode)

            if not mode_candidates:
                continue

            # 对每个可用模式计算时间，选择最短的
            best_time = float('inf')
            best_mode = None

            for mode in mode_candidates:
                speed = ideal_speeds.get(mode, 5)
                # 真实速度 = ideal_speed * congestion
                real_speed = speed * congestion
                if real_speed > 0:
                    travel_time = (distance / 1000) / real_speed * 3600
                    if travel_time < best_time:
                        best_time = travel_time
                        best_mode = mode

            if best_mode is None:
                continue

            new_time = current_time + best_time

            if new_time < times[neighbor]:
                times[neighbor] = new_time
                predecessors[neighbor] = current_node
                predecessor_modes[neighbor] = best_mode
                pq.push(HeapElement(neighbor, new_time))

    # 检查是否可达
    if times.get(end, float('inf')) == float('inf'):
        return {'success': False, 'error': '无法找到可行路径'}

    # 重建路径
    path = _reconstruct_path(predecessors, start, end)

    # 收集每段的信息
    segments = []
    total_distance = 0
    modes_used_set = set()

    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]
        mode = predecessor_modes.get(to_node, 'walk')

        edge = graph.get_edge(from_node, to_node)
        if edge:
            distance = edge.get('distance', 0)
            cong = edge.get('congestion', 1.0)
            speed = ideal_speeds.get(mode, 5)
            real_speed = speed * cong
            time = (distance / 1000) / real_speed * 3600 if real_speed > 0 else 0

            total_distance += distance
            modes_used_set.add(mode)

            segments.append({
                'from': from_node,
                'to': to_node,
                'distance': distance,
                'mode': mode,
                'speed': speed,
                'congestion': cong,
                'time': time
            })

    return {
        'success': True,
        'path': path,
        'segments': segments,
        'total_distance': total_distance,
        'total_time': times.get(end, 0),
        'modes_used': list(modes_used_set)
    }


def _normalize_transport(mode: str) -> str:
    """统一交通方式名称：支持中英文混用"""
    transport_map = {
        '步行': 'walk',
        '自行车': 'bike',
        'bike': 'bike',
        'walk': 'walk',
        '电瓶车': 'shuttle',
        'shuttle': 'shuttle',
        '驾车': 'car',
        'car': 'car',
        '公交': 'bus',
        'bus': 'bus'
    }
    return transport_map.get(mode, mode)


def get_route_info(graph, path: List[str], weight: str = 'distance',
                   transport: str = 'walk') -> Dict:
    """
    获取路径的详细信息

    参数:
        graph: Graph图对象
        path: 路径节点列表
        weight: 权重类型
        transport: 交通方式

    返回:
        {
            'total_distance': 总距离,
            'total_time': 总时间,
            'segments': [{from, to, distance, time, road_types}, ...]
        }
    """
    if not path or len(path) < 2:
        return {'total_distance': 0, 'total_time': 0, 'segments': []}

    # 不同交通方式的速度基数（km/h）
    transport_speeds = {
        '步行': 5, 'walk': 5,
        '自行车': 15, 'bike': 15,
        '电瓶车': 20, 'shuttle': 20,
        '公交': 25, 'bus': 25,
        '驾车': 40, 'car': 40
    }
    base_speed = transport_speeds.get(transport, 5)

    total_distance = 0
    total_time = 0
    segments = []

    for i in range(len(path) - 1):
        from_node = path[i]
        to_node = path[i + 1]

        edge = graph.get_edge(from_node, to_node)
        if edge:
            distance = edge['distance']

            # 计算时间：考虑交通方式和拥挤度
            congestion = edge.get('congestion', 1.0)
            # 真实速度 = 基础速度 * (1 - 拥挤度 * 0.7)
            # 拥挤度越高，速度越低，但最低不低于30%的速度
            real_speed = base_speed * max(0.3, 1 - congestion * 0.7)
            time = (distance / 1000) / real_speed * 3600  # 秒

            total_distance += distance
            total_time += time

            segments.append({
                'from': from_node,
                'to': to_node,
                'distance': distance,
                'time': time,
                'road_types': edge.get('road_types', ['步行'])
            })

    return {
        'total_distance': total_distance,
        'total_time': total_time,
        'segments': segments
    }


# 测试代码
if __name__ == "__main__":
    from backend.core.graph import Graph

    print("=" * 50)
    print("Dijkstra算法测试")
    print("=" * 50)

    # 创建测试图
    g = Graph(directed=False)

    # 添加节点
    nodes = [
        ("A", "起点", 0, 0),
        ("B", "景点1", 100, 0),
        ("C", "景点2", 100, 100),
        ("D", "景点3", 200, 100),
        ("E", "终点", 300, 100),
    ]
    for node_id, name, x, y in nodes:
        g.add_node(node_id, {'name': name, 'x': x, 'y': y})

    # 添加边
    edges = [
        ("A", "B", 100, 72, ["步行", "自行车"]),
        ("A", "C", 150, 108, ["步行"]),
        ("B", "D", 120, 86, ["步行", "自行车"]),
        ("C", "D", 80, 58, ["步行"]),
        ("D", "E", 100, 72, ["步行", "自行车"]),
        ("B", "C", 50, 36, ["步行"]),
    ]
    for from_node, to_node, dist, time_sec, road_types in edges:
        g.add_edge(from_node, to_node, distance=dist, time=time_sec, road_types=road_types)

    print("\n图结构:")
    print(g)

    # 测试1：最短距离
    print("\n1. A到E的最短距离路径:")
    result = dijkstra(g, "A", "E", weight='distance')
    print(f"  路径: {' -> '.join(result['path'])}")
    print(f"  距离: {result['distance']:.0f}米")

    # 测试2：最短时间（考虑拥挤度）
    print("\n2. A到E的最短时间路径（考虑拥挤度）:")
    # 给一些边添加拥挤度
    g.get_edge("B", "D")['congestion'] = 0.5  # 比较堵
    g.get_edge("D", "E")['congestion'] = 0.8
    g.get_edge("C", "D")['congestion'] = 1.0  # 不堵

    result = dijkstra(g, "A", "E", weight='time')
    print(f"  路径: {' -> '.join(result['path'])}")
    print(f"  时间: {result['distance']:.0f}秒 (约{result['distance']/60:.1f}分钟)")

    # 测试3：带交通约束
    print("\n3. A到E的自行车最短路径:")
    result = dijkstra_with_constraints(g, "A", "E", transport='自行车')
    print(f"  路径: {' -> '.join(result['path'])}")
    print(f"  距离: {result['distance']:.0f}米")
    print(f"  成功: {result['success']}")

    # 测试4：路径详情
    print("\n4. 路径详细信息:")
    path_info = get_route_info(g, result['path'])
    print(f"  总距离: {path_info['total_distance']:.0f}米")
    print(f"  总时间: {path_info['total_time']:.0f}秒")
    print("  分段信息:")
    for seg in path_info['segments']:
        print(f"    {seg['from']} -> {seg['to']}: {seg['distance']:.0f}米, {seg['time']:.0f}秒")

    # 测试5：混合交通工具
    print("\n5. A到E的混合交通工具最短时间路径:")
    result_mixed = shortest_path_mixed_transport(g, "A", "E")
    print(f"  成功: {result_mixed['success']}")
    print(f"  路径: {' -> '.join(result_mixed['path'])}")
    print(f"  总距离: {result_mixed['total_distance']:.0f}米")
    print(f"  总时间: {result_mixed['total_time']:.0f}秒")
    print(f"  使用交通方式: {result_mixed['modes_used']}")
    print("  分段信息:")
    for seg in result_mixed['segments']:
        print(f"    {seg['from']} -> {seg['to']}: {seg['distance']:.0f}米, mode={seg['mode']}, time={seg['time']:.0f}秒")

    print("\n[SUCCESS] Dijkstra test passed!")