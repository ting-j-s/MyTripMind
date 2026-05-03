"""
北京道路网络数据构建脚本
第3步：创建道路边（三环路线）
"""

# 三环路道路边
RING3_ROADS = [
    # 西三环：花园村 -> 航天桥 (北段)
    {"id": "BJ_RD_030", "from": "BJ_NODE_030", "to": "BJ_NODE_031", "distance": 1200, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 北三环：马甸桥 -> 安华桥 -> 安贞桥 -> 和平西桥 -> 和平东桥
    {"id": "BJ_RD_031", "from": "BJ_NODE_032", "to": "BJ_NODE_033", "distance": 1200, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_032", "from": "BJ_NODE_033", "to": "BJ_NODE_034", "distance": 1200, "ideal_speed": 50, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_033", "from": "BJ_NODE_034", "to": "BJ_NODE_035", "distance": 1200, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_034", "from": "BJ_NODE_035", "to": "BJ_NODE_036", "distance": 1200, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 东三环北段：和平东桥 -> 雍和宫桥 (与二环交叉)
    {"id": "BJ_RD_035", "from": "BJ_NODE_036", "to": "BJ_NODE_037", "distance": 1500, "ideal_speed": 50, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 东三环南段：长虹桥 -> 小武基桥 -> 十里河桥 -> 方庄桥 -> 刘家窑桥
    {"id": "BJ_RD_036", "from": "BJ_NODE_009", "to": "BJ_NODE_038", "distance": 3600, "ideal_speed": 50, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_037", "from": "BJ_NODE_038", "to": "BJ_NODE_039", "distance": 1200, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_038", "from": "BJ_NODE_039", "to": "BJ_NODE_040", "distance": 1500, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_039", "from": "BJ_NODE_040", "to": "BJ_NODE_041", "distance": 2400, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_040", "from": "BJ_NODE_041", "to": "BJ_NODE_042", "distance": 1200, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 南三环：赵公口桥 -> 木樨园桥 -> 洋桥 -> 右安门桥
    {"id": "BJ_RD_041", "from": "BJ_NODE_042", "to": "BJ_NODE_043", "distance": 1500, "ideal_speed": 50, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_042", "from": "BJ_NODE_043", "to": "BJ_NODE_044", "distance": 2400, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_043", "from": "BJ_NODE_044", "to": "BJ_NODE_045", "distance": 1200, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 西三环南段：玉泉营桥 -> 西铁营桥 -> 菜户营桥
    {"id": "BJ_RD_044", "from": "BJ_NODE_046", "to": "BJ_NODE_047", "distance": 2400, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_045", "from": "BJ_NODE_047", "to": "BJ_NODE_048", "distance": 1200, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 西三环北段：航天桥 -> 花园村 (回西三环)
    {"id": "BJ_RD_046", "from": "BJ_NODE_031", "to": "BJ_NODE_030", "distance": 1200, "ideal_speed": 50, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # 三环与二环连接线
    {"id": "BJ_RD_047", "from": "BJ_NODE_029", "to": "BJ_NODE_030", "distance": 5000, "ideal_speed": 50, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_048", "from": "BJ_NODE_001", "to": "BJ_NODE_031", "distance": 5500, "ideal_speed": 50, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_049", "from": "BJ_NODE_009", "to": "BJ_NODE_009", "distance": 0, "ideal_speed": 0, "congestion": 1.0, "road_types": []},  # 自环，占位
]


if __name__ == "__main__":
    import json
    import os

    data_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(data_dir, 'beijing_roads_ring3.json')

    # 过滤掉无效数据
    valid_roads = [r for r in RING3_ROADS if r["distance"] > 0]

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"roads": valid_roads}, f, ensure_ascii=False, indent=2)

    print(f"三环路道路边已保存: {len(valid_roads)} 条")
