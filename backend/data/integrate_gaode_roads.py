"""
整合高德地图真实路径数据到道路网络
"""

import json
import os

def main():
    data_dir = os.path.dirname(os.path.abspath(__file__))

    # 读取之前获取的路径数据
    with open(os.path.join(data_dir, 'gaode_paths.json'), 'r', encoding='utf-8') as f:
        paths1 = json.load(f)['paths']

    with open(os.path.join(data_dir, 'gaode_paths_more.json'), 'r', encoding='utf-8') as f:
        paths2 = json.load(f)['paths']

    # 合并去重
    all_paths = paths1 + paths2
    print(f'合并后总路径数: {len(all_paths)}')

    # 转换为道路边格式
    # 从景点ID到景点坐标的映射
    attraction_ids = set()
    for p in all_paths:
        attraction_ids.add(p['from_id'])
        attraction_ids.add(p['to_id'])

    # 创建道路边
    roads = []
    road_id = 1

    for p in all_paths:
        # 双向道路
        roads.append({
            "id": f"GAODE_RD_{road_id:04d}",
            "from_node": p['from_id'],
            "to_node": p['to_id'],
            "distance": p['distance'],
            "ideal_speed": 40,  # 城市道路限速
            "congestion": 0.8,  # 默认拥堵度
            "road_types": ["步行", "自行车", "公交", "驾车"]
        })
        road_id += 1

        # 反向边
        roads.append({
            "id": f"GAODE_RD_{road_id:04d}",
            "from_node": p['to_id'],
            "to_node": p['from_id'],
            "distance": p['distance'],
            "ideal_speed": 40,
            "congestion": 0.8,
            "road_types": ["步行", "自行车", "公交", "驾车"]
        })
        road_id += 1

    print(f'生成道路边数: {len(roads)} (双向)')

    # 保存高德道路数据
    filepath = os.path.join(data_dir, 'gaode_roads.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"roads": roads}, f, ensure_ascii=False, indent=2)

    print(f'已保存到: {filepath}')

    # 更新主道路数据文件
    # 读取现有道路数据
    roads_file = os.path.join(data_dir, 'roads.json')
    with open(roads_file, 'r', encoding='utf-8') as f:
        existing_roads = json.load(f)

    # 添加高德数据
    existing_roads['roads'].extend(roads)

    with open(roads_file, 'w', encoding='utf-8') as f:
        json.dump(existing_roads, f, ensure_ascii=False, indent=2)

    print(f'\n更新后的roads.json: {len(existing_roads["roads"])} 条道路边')

    # 统计
    total_distance = sum(r['distance'] for r in roads)
    avg_distance = total_distance / len(roads) if roads else 0
    print(f'\\n高德道路统计:')
    print(f'  总边数: {len(roads)}')
    print(f'  总距离: {total_distance/1000:.1f}公里')
    print(f'  平均距离: {avg_distance:.0f}米')

if __name__ == "__main__":
    main()
