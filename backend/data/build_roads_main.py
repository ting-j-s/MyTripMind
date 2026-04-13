"""
北京道路网络数据构建脚本
第4步：创建道路边（主干道：长安街、平安大街、中轴路等）
"""

MAIN_ROADS = [
    # === 长安街及延长线 ===
    {"id": "BJ_RD_050", "from": "BJ_NODE_027", "to": "BJ_NODE_061", "distance": 4500, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_051", "from": "BJ_NODE_061", "to": "BJ_NODE_062", "distance": 900, "ideal_speed": 40, "congestion": 0.9, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_052", "from": "BJ_NODE_062", "to": "BJ_NODE_063", "distance": 1000, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_053", "from": "BJ_NODE_063", "to": "BJ_NODE_064", "distance": 600, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_054", "from": "BJ_NODE_064", "to": "BJ_NODE_065", "distance": 1800, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_055", "from": "BJ_NODE_065", "to": "BJ_NODE_066", "distance": 2400, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_056", "from": "BJ_NODE_066", "to": "BJ_NODE_067", "distance": 2200, "ideal_speed": 50, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_057", "from": "BJ_NODE_067", "to": "BJ_NODE_068", "distance": 1500, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # === 平安大街 ===
    {"id": "BJ_RD_060", "from": "BJ_NODE_027", "to": "BJ_NODE_069", "distance": 5500, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_061", "from": "BJ_NODE_069", "to": "BJ_NODE_070", "distance": 1500, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_062", "from": "BJ_NODE_070", "to": "BJ_NODE_071", "distance": 1000, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_063", "from": "BJ_NODE_071", "to": "BJ_NODE_004", "distance": 1500, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # === 中轴路 ===
    {"id": "BJ_RD_065", "from": "BJ_NODE_072", "to": "BJ_NODE_073", "distance": 2500, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_066", "from": "BJ_NODE_073", "to": "BJ_NODE_074", "distance": 1200, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_067", "from": "BJ_NODE_074", "to": "BJ_NODE_075", "distance": 1500, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_068", "from": "BJ_NODE_075", "to": "BJ_NODE_062", "distance": 1200, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # === 西单-崇文门一线 ===
    {"id": "BJ_RD_070", "from": "BJ_NODE_027", "to": "BJ_NODE_076", "distance": 1800, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_071", "from": "BJ_NODE_076", "to": "BJ_NODE_077", "distance": 1200, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_072", "from": "BJ_NODE_077", "to": "BJ_NODE_078", "distance": 1200, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_073", "from": "BJ_NODE_078", "to": "BJ_NODE_020", "distance": 600, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_074", "from": "BJ_NODE_078", "to": "BJ_NODE_079", "distance": 4500, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_075", "from": "BJ_NODE_079", "to": "BJ_NODE_080", "distance": 600, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_076", "from": "BJ_NODE_080", "to": "BJ_NODE_065", "distance": 1200, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # === 学院路 ===
    {"id": "BJ_RD_080", "from": "BJ_NODE_051", "to": "BJ_NODE_052", "distance": 1200, "ideal_speed": 40, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_081", "from": "BJ_NODE_052", "to": "BJ_NODE_053", "distance": 1200, "ideal_speed": 40, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_082", "from": "BJ_NODE_053", "to": "BJ_NODE_054", "distance": 1200, "ideal_speed": 40, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_083", "from": "BJ_NODE_054", "to": "BJ_NODE_055", "distance": 1200, "ideal_speed": 40, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_084", "from": "BJ_NODE_055", "to": "BJ_NODE_056", "distance": 2400, "ideal_speed": 40, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # === 四环路连接 ===
    {"id": "BJ_RD_085", "from": "BJ_NODE_052", "to": "BJ_NODE_049", "distance": 3500, "ideal_speed": 60, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_086", "from": "BJ_NODE_051", "to": "BJ_NODE_050", "distance": 2500, "ideal_speed": 60, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_087", "from": "BJ_NODE_050", "to": "BJ_NODE_057", "distance": 3500, "ideal_speed": 60, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_088", "from": "BJ_NODE_057", "to": "BJ_NODE_058", "distance": 2500, "ideal_speed": 60, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # === 横向连接：长安街与平安大街之间 ===
    {"id": "BJ_RD_090", "from": "BJ_NODE_076", "to": "BJ_NODE_069", "distance": 4000, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_091", "from": "BJ_NODE_062", "to": "BJ_NODE_069", "distance": 2500, "ideal_speed": 40, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},

    # === 环路之间连接 ===
    {"id": "BJ_RD_092", "from": "BJ_NODE_003", "to": "BJ_NODE_032", "distance": 800, "ideal_speed": 40, "congestion": 0.6, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_093", "from": "BJ_NODE_063", "to": "BJ_NODE_008", "distance": 5000, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_094", "from": "BJ_NODE_075", "to": "BJ_NODE_061", "distance": 1000, "ideal_speed": 40, "congestion": 0.8, "road_types": ["步行", "自行车", "公交", "驾车"]},
    {"id": "BJ_RD_095", "from": "BJ_NODE_030", "to": "BJ_NODE_059", "distance": 5000, "ideal_speed": 50, "congestion": 0.7, "road_types": ["步行", "自行车", "公交", "驾车"]},
]


if __name__ == "__main__":
    import json
    import os

    data_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(data_dir, 'beijing_roads_main.json')

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"roads": MAIN_ROADS}, f, ensure_ascii=False, indent=2)

    print(f"主干道道路边已保存: {len(MAIN_ROADS)} 条")
