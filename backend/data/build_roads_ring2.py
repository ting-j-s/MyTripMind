"""
北京道路网络数据构建脚本
第2步：创建道路边（环路线）
"""

# 二环路道路边（顺时针）
# distance是估算的直线距离(米)，ideal_speed是理想步行速度(km/h)

RING2_ROADS = [
    # 西直门 -> 积水潭 -> 鼓楼桥 -> ... -> 雍和宫桥 -> 东直门 (北二环)
    {"id": "BJ_RD_001", "from": "BJ_NODE_001", "to": "BJ_NODE_002", "distance": 1200, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_002", "from": "BJ_NODE_002", "to": "BJ_NODE_003", "distance": 1100, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_003", "from": "BJ_NODE_003", "to": "BJ_NODE_004", "distance": 2300, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_004", "from": "BJ_NODE_004", "to": "BJ_NODE_005", "distance": 1100, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_005", "from": "BJ_NODE_005", "to": "BJ_NODE_006", "distance": 2200, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 东直门 -> 三元桥 -> 燕莎桥 (东二环北段)
    {"id": "BJ_RD_006", "from": "BJ_NODE_006", "to": "BJ_NODE_007", "distance": 2400, "ideal_speed": 50, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_007", "from": "BJ_NODE_007", "to": "BJ_NODE_008", "distance": 1200, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 燕莎桥 -> 长虹桥 -> 农展馆桥 -> 朝阳公园桥 -> 东风桥 (东二环南段)
    {"id": "BJ_RD_008", "from": "BJ_NODE_008", "to": "BJ_NODE_009", "distance": 1500, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_009", "from": "BJ_NODE_009", "to": "BJ_NODE_010", "distance": 1200, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_010", "from": "BJ_NODE_010", "to": "BJ_NODE_011", "distance": 1200, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_011", "from": "BJ_NODE_011", "to": "BJ_NODE_012", "distance": 2400, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 东风桥 -> 南磨房桥 -> 劲松桥 -> 潘家园桥 -> 十里河桥 (南二环东段)
    {"id": "BJ_RD_012", "from": "BJ_NODE_012", "to": "BJ_NODE_013", "distance": 1100, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_013", "from": "BJ_NODE_013", "to": "BJ_NODE_014", "distance": 1200, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_014", "from": "BJ_NODE_014", "to": "BJ_NODE_015", "distance": 2400, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_015", "from": "BJ_NODE_015", "to": "BJ_NODE_016", "distance": 1200, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 十里河桥 -> 左安门桥 -> 玉蜓桥 -> 景泰桥 -> 永定门桥 (南二环西段)
    {"id": "BJ_RD_016", "from": "BJ_NODE_016", "to": "BJ_NODE_017", "distance": 2300, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_017", "from": "BJ_NODE_017", "to": "BJ_NODE_018", "distance": 2400, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_018", "from": "BJ_NODE_018", "to": "BJ_NODE_019", "distance": 1100, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_019", "from": "BJ_NODE_019", "to": "BJ_NODE_020", "distance": 1100, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 永定门桥 -> 先农坛桥 -> 右安门桥 -> 菜户营桥 (南二环西段继续)
    {"id": "BJ_RD_020", "from": "BJ_NODE_020", "to": "BJ_NODE_021", "distance": 1200, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_021", "from": "BJ_NODE_021", "to": "BJ_NODE_022", "distance": 2400, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_022", "from": "BJ_NODE_022", "to": "BJ_NODE_023", "distance": 1100, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 菜户营桥 -> 白纸坊桥 -> 广安门桥 -> 天宁寺桥 -> 西便门桥 (西二环南段)
    {"id": "BJ_RD_023", "from": "BJ_NODE_023", "to": "BJ_NODE_024", "distance": 1200, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_024", "from": "BJ_NODE_024", "to": "BJ_NODE_025", "distance": 1100, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_025", "from": "BJ_NODE_025", "to": "BJ_NODE_026", "distance": 1200, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_026", "from": "BJ_NODE_026", "to": "BJ_NODE_027", "distance": 900, "ideal_speed": 40, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 西便门桥 -> 复兴门桥 -> 阜成门桥 -> 西直门 (西二环北段)
    {"id": "BJ_RD_027", "from": "BJ_NODE_027", "to": "BJ_NODE_028", "distance": 1200, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_028", "from": "BJ_NODE_028", "to": "BJ_NODE_029", "distance": 1100, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_029", "from": "BJ_NODE_029", "to": "BJ_NODE_001", "distance": 1100, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
]


if __name__ == "__main__":
    import json
    import os

    data_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(data_dir, 'beijing_roads_ring2.json')

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"roads": RING2_ROADS}, f, ensure_ascii=False, indent=2)

    print(f"二环路道路边已保存: {len(RING2_ROADS)} 条")
