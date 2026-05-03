"""
估算景点间的道路距离
对于无法从高德获取的路径，使用坐标直线距离乘以系数估算
城市道路实际距离通常是直线距离的1.3-1.5倍
"""

import json
import math
import os

def haversine_distance(lat1, lon1, lat2, lon2):
    """计算两点间的直线距离（米）"""
    R = 6371000  # 地球半径（米）

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi/2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def estimate_distance(x1, y1, x2, y2, factor=1.4):
    """估算道路距离（直线距离 × 系数）"""
    straight_dist = haversine_distance(y1, x1, y2, x2)
    return int(straight_dist * factor)

def main():
    data_dir = os.path.dirname(os.path.abspath(__file__))

    # 加载景点数据
    with open(os.path.join(data_dir, 'attractions.json'), 'r', encoding='utf-8') as f:
        attractions = json.load(f)['attractions']

    # 建立ID到坐标的映射
    coords = {a['id']: (a['x'], a['y']) for a in attractions}

    # 已有的核心路径（从core_paths.json）
    with open(os.path.join(data_dir, 'core_paths.json'), 'r', encoding='utf-8') as f:
        core_paths = json.load(f)['paths']

    # 创建已有关联的集合
    existing_pairs = set()
    for p in core_paths:
        existing_pairs.add((p['from_id'], p['to_id']))
        existing_pairs.add((p['to_id'], p['from_id']))

    print(f"已有关联数: {len(existing_pairs)}")

    # 估算其他所有景点对之间的距离
    new_roads = []
    road_id = 1

    all_ids = list(coords.keys())
    total_pairs = len(all_ids) * (len(all_ids) - 1)
    print(f"总景点对数: {total_pairs}")
    print(f"需要估算: {total_pairs - len(existing_pairs)}")

    for i, from_id in enumerate(all_ids):
        if not from_id.startswith('ATTR_'):
            continue

        for j, to_id in enumerate(all_ids):
            if from_id == to_id:
                continue

            if not to_id.startswith('ATTR_'):
                continue

            # 跳过已有关联
            if (from_id, to_id) in existing_pairs:
                continue

            x1, y1 = coords[from_id]
            x2, y2 = coords[to_id]

            # 计算估算距离
            distance = estimate_distance(x1, y1, x2, y2, factor=1.4)

            # 双向添加
            new_roads.append({
                "id": f"EST_RD_{road_id:05d}",
                "from_node": from_id,
                "to_node": to_id,
                "distance": distance,
                "ideal_speed": 40,
                "congestion": 0.8,
                "road_types": ["步行", "自行车", "公交", "驾车"],
                "estimated": True  # 标记为估算距离
            })
            road_id += 1

            new_roads.append({
                "id": f"EST_RD_{road_id:05d}",
                "from_node": to_id,
                "to_node": from_id,
                "distance": distance,
                "ideal_speed": 40,
                "congestion": 0.8,
                "road_types": ["步行", "自行车", "公交", "驾车"],
                "estimated": True
            })
            road_id += 1

        if (i + 1) % 50 == 0:
            print(f"进度: {i+1}/{len(all_ids)}")

    print(f"\n估算道路边数: {len(new_roads)}")

    # 读取现有道路数据
    roads_file = os.path.join(data_dir, 'roads.json')
    with open(roads_file, 'r', encoding='utf-8') as f:
        existing_roads = json.load(f)

    original_count = len(existing_roads['roads'])

    # 去除旧的估算道路（EST_RD_）
    existing_roads['roads'] = [r for r in existing_roads['roads'] if not r.get('estimated', False)]
    removed = original_count - len(existing_roads['roads'])
    print(f"移除旧估算道路: {removed}")

    # 添加新估算道路
    existing_roads['roads'].extend(new_roads)

    with open(roads_file, 'w', encoding='utf-8') as f:
        json.dump(existing_roads, f, ensure_ascii=False, indent=2)

    print(f"\n更新后的roads.json: {len(existing_roads['roads'])} 条道路边")

    # 统计
    est_roads = [r for r in new_roads]
    total_dist = sum(r['distance'] for r in est_roads)
    avg_dist = total_dist / len(est_roads) if est_roads else 0
    print(f"\n估算道路统计:")
    print(f"  总边数: {len(est_roads)}")
    print(f"  总距离: {total_dist/1000:.1f}公里")
    print(f"  平均距离: {avg_dist:.0f}米")

if __name__ == "__main__":
    main()