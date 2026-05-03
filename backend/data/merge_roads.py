"""
北京道路网络数据构建脚本
第6步：整合所有道路数据到roads.json
"""

import json
import os

def main():
    data_dir = os.path.dirname(os.path.abspath(__file__))

    # 读取所有道路数据文件
    road_files = [
        'beijing_roads_ring2.json',      # 二环路 29条
        'beijing_roads_ring3.json',      # 三环路 19条
        'beijing_roads_main.json',       # 主干道 38条
        'beijing_roads_attractions.json', # 景点连接 117条
    ]

    all_roads = []
    total = 0

    for filename in road_files:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                roads = data.get('roads', [])
                all_roads.extend(roads)
                print(f"{filename}: {len(roads)} 条")
                total += len(roads)
        else:
            print(f"文件不存在: {filename}")

    print(f"\n总计: {total} 条道路边")

    # 保存整合后的道路数据
    output_file = os.path.join(data_dir, 'roads.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"roads": all_roads}, f, ensure_ascii=False, indent=2)

    print(f"\n已保存到: {output_file}")

    # 验证
    with open(output_file, 'r', encoding='utf-8') as f:
        verify = json.load(f)
        print(f"验证: {len(verify['roads'])} 条道路")

if __name__ == "__main__":
    main()
