"""
整合核心景点路径数据到道路网络
"""

import json
import os

def main():
    data_dir = os.path.dirname(os.path.abspath(__file__))

    # 读取核心路径数据
    with open(os.path.join(data_dir, 'core_paths.json'), 'r', encoding='utf-8') as f:
        core_data = json.load(f)
    core_paths = core_data['paths']
    print(f'核心路径数: {len(core_paths)}')

    # 创建道路边
    roads = []
    road_id = 1

    for p in core_paths:
        # 双向道路
        roads.append({
            "id": f"CORE_RD_{road_id:04d}",
            "from_node": p['from_id'],
            "to_node": p['to_id'],
            "distance": p['distance'],
            "ideal_speed": 40,
            "congestion": 0.8,
            "road_types": ["步行", "自行车", "公交", "驾车"]
        })
        road_id += 1

        roads.append({
            "id": f"CORE_RD_{road_id:04d}",
            "from_node": p['to_id'],
            "to_node": p['from_id'],
            "distance": p['distance'],
            "ideal_speed": 40,
            "congestion": 0.8,
            "road_types": ["步行", "自行车", "公交", "驾车"]
        })
        road_id += 1

    print(f'生成道路边数: {len(roads)} (双向)')

    # 读取现有道路数据
    roads_file = os.path.join(data_dir, 'roads.json')
    with open(roads_file, 'r', encoding='utf-8') as f:
        existing_roads = json.load(f)

    # 检查并去除已有的CORE_RD边（避免重复）
    original_count = len(existing_roads['roads'])
    existing_roads['roads'] = [r for r in existing_roads['roads'] if not r['id'].startswith('CORE_')]
    removed = original_count - len(existing_roads['roads'])
    print(f'移除旧CORE道路边: {removed}')

    # 添加新核心数据
    existing_roads['roads'].extend(roads)

    with open(roads_file, 'w', encoding='utf-8') as f:
        json.dump(existing_roads, f, ensure_ascii=False, indent=2)

    print(f'\n更新后的roads.json: {len(existing_roads["roads"])} 条道路边')

    # 统计
    total_distance = sum(r['distance'] for r in roads)
    avg_distance = total_distance / len(roads) if roads else 0
    print(f'\n核心道路统计:')
    print(f'  总边数: {len(roads)}')
    print(f'  总距离: {total_distance/1000:.1f}公里')
    print(f'  平均距离: {avg_distance:.0f}米')

if __name__ == "__main__":
    main()