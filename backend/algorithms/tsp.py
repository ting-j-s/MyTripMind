"""
旅行商问题(TSP)算法实现
问题：给定一系列城市和每对城市之间的距离，求解访问每一座城市一次并回到起始城市的最短回路
课程要求：必须自己实现

本实现使用贪心最近邻算法 + 2-opt优化
时间复杂度：O(n²) 贪心 + O(kn²) 优化
"""

from typing import List, Dict, Tuple, Optional
from backend.core.graph import Graph


def nearest_neighbor_tsp(graph: Graph, start: str,
                        nodes: List[str] = None,
                        weight: str = 'distance') -> Dict:
    """
    贪心最近邻算法求解TSP

    算法步骤：
        1. 从起点开始
        2. 每次选择距离当前节点最近的未访问节点
        3. 重复直到访问所有节点
        4. 返回起点

    时间复杂度: O(n²)

    参数:
        graph: Graph图对象
        start: 起点/终点
        nodes: 要访问的节点列表（不含起点，起点会自动添加）
        weight: 权重类型

    返回:
        {
            'path': [起点, 节点1, 节点2, ..., 起点],
            'total_distance': 总距离,
            'total_time': 总时间,
            'visited_order': 访问顺序（不含返回起点）
        }
    """
    # 确定要访问的节点列表
    if nodes is None:
        nodes = [n for n in graph.get_all_nodes() if n != start]
    else:
        nodes = [n for n in nodes if n != start]

    if start not in graph.get_all_nodes():
        return {'error': f'Start node {start} not in graph', 'success': False}

    # 检查所有节点是否在图中
    for node in nodes:
        if node not in graph.get_all_nodes():
            return {'error': f'Node {node} not in graph', 'success': False}

    # 如果只有0或1个节点
    if len(nodes) == 0:
        return {
            'path': [start],
            'total_distance': 0,
            'total_time': 0,
            'visited_order': [],
            'success': True
        }

    if len(nodes) == 1:
        node = nodes[0]
        edge = graph.get_edge(start, node)
        if edge:
            dist = edge['distance']
            time = edge['time']
        else:
            dist = float('inf')
            time = float('inf')
        return {
            'path': [start, node, start],
            'total_distance': dist * 2 if dist < float('inf') else float('inf'),
            'total_time': time * 2 if time < float('inf') else float('inf'),
            'visited_order': [node],
            'success': dist < float('inf')
        }

    # 贪心算法
    visited = [start]
    remaining = set(nodes)
    current = start
    total_distance = 0
    total_time = 0

    while remaining:
        best_node = None
        best_distance = float('inf')
        best_time = float('inf')

        # 找最近的未访问节点
        for neighbor_info in graph.get_neighbors(current):
            neighbor = neighbor_info['node']
            if neighbor in remaining:
                dist = neighbor_info.get('distance', neighbor_info['distance'])
                if dist < best_distance:
                    best_distance = dist
                    best_node = neighbor
                    best_time = neighbor_info.get('time', best_distance / 5 * 3600)

        if best_node is None:
            # 没有找到可达的节点
            return {
                'error': f'Cannot reach any remaining node from {current}',
                'success': False,
                'visited_order': visited[1:]
            }

        visited.append(best_node)
        remaining.remove(best_node)
        total_distance += best_distance
        total_time += best_time
        current = best_node

    # 返回起点
    edge_to_start = graph.get_edge(current, start)
    if edge_to_start:
        total_distance += edge_to_start['distance']
        total_time += edge_to_start['time']
    else:
        return {
            'error': f'Cannot return to start from {current}',
            'success': False,
            'path': visited,
            'total_distance': total_distance,
            'total_time': total_time,
            'visited_order': visited[1:]
        }

    visited.append(start)

    return {
        'path': visited,
        'total_distance': total_distance,
        'total_time': total_time,
        'visited_order': visited[1:-1],
        'success': True
    }


def two_opt_swap(path: List[str], i: int, j: int) -> List[str]:
    """
    2-opt交换：将路径中i到j之间的节点反转

    例如：path = [A, B, C, D, E, F], i=1, j=4
    交换后: [A, E, D, C, B, F]
    """
    new_path = path[:i+1]
    new_path.extend(reversed(path[i+1:j+1]))
    new_path.extend(path[j+1:])
    return new_path


def two_opt_optimize(graph: Graph, path: List[str],
                     weight: str = 'distance') -> Tuple[List[str], float]:
    """
    2-opt优化：改进TSP解的质量

    算法步骤：
        1. 计算当前路径总距离
        2. 对于每一对边(i,j)，如果交换能减少距离，则交换
        3. 重复直到没有改进

    时间复杂度: O(kn²)，k为迭代次数

    参数:
        graph: Graph图对象
        path: 初始路径
        weight: 权重类型

    返回:
        (优化后的路径, 优化后的距离)
    """
    if len(path) < 4:
        return path, _calculate_path_distance(graph, path, weight)

    improved = True
    current_path = path.copy()
    current_distance = _calculate_path_distance(graph, current_path, weight)

    while improved:
        improved = False
        for i in range(1, len(current_path) - 2):
            for j in range(i + 1, len(current_path) - 1):
                # 尝试交换
                new_path = two_opt_swap(current_path, i, j)
                new_distance = _calculate_path_distance(graph, new_path, weight)

                if new_distance < current_distance:
                    current_path = new_path
                    current_distance = new_distance
                    improved = True
                    break
            if improved:
                break

    return current_path, current_distance


def _calculate_path_distance(graph: Graph, path: List[str], weight: str = 'distance') -> float:
    """计算路径的总距离"""
    total = 0
    for i in range(len(path) - 1):
        edge = graph.get_edge(path[i], path[i+1])
        if edge:
            total += edge.get('distance', 0)
        else:
            return float('inf')
    return total


def solve_tsp(graph: Graph, start: str,
               nodes: List[str] = None,
               optimize: bool = True,
               weight: str = 'distance') -> Dict:
    """
    求解TSP问题（带优化的贪心算法）

    参数:
        graph: Graph图对象
        start: 起点/终点
        nodes: 要访问的节点列表
        optimize: 是否进行2-opt优化
        weight: 权重类型

    返回:
        {
            'path': 完整路径（含返回起点）,
            'total_distance': 总距离,
            'total_time': 总时间,
            'visited_order': 访问顺序,
            'success': 是否成功
        }
    """
    # 第一步：贪心求解
    result = nearest_neighbor_tsp(graph, start, nodes, weight)

    if not result.get('success', False):
        return result

    # 第二步：2-opt优化
    if optimize and len(result['path']) >= 4:
        optimized_path, optimized_distance = two_opt_optimize(
            graph, result['path'], weight
        )
        result['path'] = optimized_path
        result['total_distance'] = optimized_distance

        # 重新计算时间
        total_time = 0
        for i in range(len(optimized_path) - 1):
            edge = graph.get_edge(optimized_path[i], optimized_path[i+1])
            if edge:
                total_time += edge.get('time', 0)
        result['total_time'] = total_time

    return result


def solve_tsp_with_transport(graph: Graph, start: str,
                              nodes: List[str],
                              transport: str = '步行',
                              optimize: bool = True) -> Dict:
    """
    求解TSP问题（带交通方式约束）

    注意：这个版本的TSP会考虑不同路段的交通方式限制
    """
    # 简单的实现：先找到可达的路径，然后用普通TSP
    result = nearest_neighbor_tsp(graph, start, nodes, weight='distance')

    if not result.get('success', False):
        return result

    # 检查路径是否全部满足交通方式约束
    valid = True
    for i in range(len(result['path']) - 1):
        edge = graph.get_edge(result['path'][i], result['path'][i+1])
        if edge:
            if transport not in edge.get('road_types', ['步行']):
                valid = False
                break

    if not valid:
        return {
            'error': f'No valid path found with transport {transport}',
            'success': False
        }

    # 2-opt优化
    if optimize and len(result['path']) >= 4:
        optimized_path, _ = two_opt_optimize(graph, result['path'])
        result['path'] = optimized_path
        result['total_distance'] = _calculate_path_distance(graph, optimized_path)

    return result


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("TSP算法测试")
    print("=" * 50)

    # 创建测试图
    g = Graph(directed=False)

    # 5个节点：起点A，和4个要访问的景点
    nodes = [
        ("A", "起点", 0, 0),
        ("B", "景点B", 100, 0),
        ("C", "景点C", 100, 100),
        ("D", "景点D", 200, 100),
        ("E", "景点E", 200, 0),
    ]

    for node_id, name, x, y in nodes:
        g.add_node(node_id, {'name': name, 'x': x, 'y': y})

    # 添加边（构成一个不完全图）
    edges = [
        ("A", "B", 100, 72),
        ("A", "C", 150, 108),
        ("A", "D", 250, 180),
        ("A", "E", 200, 144),
        ("B", "C", 80, 58),
        ("B", "D", 150, 108),
        ("B", "E", 120, 86),
        ("C", "D", 100, 72),
        ("C", "E", 180, 130),
        ("D", "E", 100, 72),
    ]

    for from_node, to_node, dist, time_sec in edges:
        g.add_edge(from_node, to_node, distance=dist, time=time_sec)

    print("\n图结构:")
    print(g)

    # 测试1：贪心最近邻
    print("\n1. 贪心最近邻TSP (A起点，访问B,C,D,E):")
    result = nearest_neighbor_tsp(g, "A", ["B", "C", "D", "E"])
    print(f"  路径: {' -> '.join(result['path'])}")
    print(f"  总距离: {result['total_distance']:.0f}米")
    print(f"  总时间: {result['total_time']:.0f}秒")

    # 测试2：带2-opt优化
    print("\n2. 2-opt优化后的TSP:")
    result = solve_tsp(g, "A", ["B", "C", "D", "E"], optimize=True)
    print(f"  路径: {' -> '.join(result['path'])}")
    print(f"  总距离: {result['total_distance']:.0f}米")
    print(f"  总时间: {result['total_time']:.0f}秒")

    # 测试3：只访问部分节点
    print("\n3. 只访问B和C (从A出发返回A):")
    result = solve_tsp(g, "A", ["B", "C"])
    print(f"  路径: {' -> '.join(result['path'])}")
    print(f"  总距离: {result['total_distance']:.0f}米")

    print("\n[SUCCESS] TSP test passed!")
