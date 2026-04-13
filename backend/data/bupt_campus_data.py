"""
北邮沙河校区详细数据
根据校园地图整理
"""

# 北邮沙河校区坐标范围：大约 x:116.34-116.36, y:40.02-40.03

# 建筑物数据
BUILDINGS = [
    # 主要教学楼
    {
        "id": "BUPT_LIB",
        "name": "图书馆",
        "type": "教学楼",
        "campus_id": "BUPT",
        "x": 116.3520,
        "y": 40.0255,
        "floors": 3,
        "rooms": ["一层", "二层", "三层", "自习室"],
        "elevators": ["A"],
        "entrances": ["东门", "西门"]
    },
    {
        "id": "BUPT_INFO",
        "name": "信息楼",
        "type": "教学楼",
        "campus_id": "BUPT",
        "x": 116.3510,
        "y": 40.0270,
        "floors": 4,
        "rooms": ["101-108", "201-208", "301-308", "401-408"],
        "elevators": ["A", "B"],
        "entrances": ["南门", "北门"]
    },
    {
        "id": "BUPT_TEACH",
        "name": "综合教学楼",
        "type": "教学楼",
        "campus_id": "BUPT",
        "x": 116.3490,
        "y": 40.0260,
        "floors": 4,
        "rooms": ["101-112", "201-212", "301-312", "401-412"],
        "elevators": ["A", "B", "C"],
        "entrances": ["东门", "西门", "南门"]
    },
    {
        "id": "BUPT_ADMIN",
        "name": "行政楼",
        "type": "行政",
        "campus_id": "BUPT",
        "x": 116.3500,
        "y": 40.0245,
        "floors": 4,
        "rooms": ["一层大厅", "二层办公室", "三层会议室", "四层档案室"],
        "elevators": ["A"],
        "entrances": ["正门"]
    },

    # 学生宿舍（6栋）
    {
        "id": "BUPT_DORM_1",
        "name": "学生宿舍1号楼",
        "type": "宿舍",
        "campus_id": "BUPT",
        "x": 116.3480,
        "y": 40.0280,
        "floors": 6,
        "rooms": ["101-612"],
        "elevators": [],
        "entrances": ["南门"]
    },
    {
        "id": "BUPT_DORM_2",
        "name": "学生宿舍2号楼",
        "type": "宿舍",
        "campus_id": "BUPT",
        "x": 116.3488,
        "y": 40.0280,
        "floors": 6,
        "rooms": ["101-612"],
        "elevators": [],
        "entrances": ["南门"]
    },
    {
        "id": "BUPT_DORM_3",
        "name": "学生宿舍3号楼",
        "type": "宿舍",
        "campus_id": "BUPT",
        "x": 116.3496,
        "y": 40.0280,
        "floors": 6,
        "rooms": ["101-612"],
        "elevators": [],
        "entrances": ["南门"]
    },
    {
        "id": "BUPT_DORM_4",
        "name": "学生宿舍4号楼",
        "type": "宿舍",
        "campus_id": "BUPT",
        "x": 116.3504,
        "y": 40.0280,
        "floors": 6,
        "rooms": ["101-612"],
        "elevators": [],
        "entrances": ["南门"]
    },
    {
        "id": "BUPT_DORM_5",
        "name": "学生宿舍5号楼",
        "type": "宿舍",
        "campus_id": "BUPT",
        "x": 116.3512,
        "y": 40.0280,
        "floors": 6,
        "rooms": ["101-612"],
        "elevators": [],
        "entrances": ["南门"]
    },
    {
        "id": "BUPT_DORM_6",
        "name": "学生宿舍6号楼",
        "type": "宿舍",
        "campus_id": "BUPT",
        "x": 116.3520,
        "y": 40.0280,
        "floors": 6,
        "rooms": ["101-612"],
        "elevators": [],
        "entrances": ["南门"]
    },

    # 食堂
    {
        "id": "BUPT_CAFETERIA",
        "name": "鸿通新空间（食堂）",
        "type": "食堂",
        "campus_id": "BUPT",
        "x": 116.3530,
        "y": 40.0265,
        "floors": 4,
        "rooms": ["一层风味餐厅", "二层基本伙食", "三层自助餐厅", "四层清真餐厅"],
        "elevators": ["A", "B"],
        "entrances": ["南门", "北门"]
    },
]

# 设施数据
FACILITIES = [
    # 运动场地
    {"id": "FAC_BASKET_1", "name": "篮球场1", "type": "运动场", "campus_id": "BUPT", "x": 116.3475, "y": 40.0290},
    {"id": "FAC_BASKET_2", "name": "篮球场2", "type": "运动场", "campus_id": "BUPT", "x": 116.3475, "y": 40.0295},
    {"id": "FAC_BASKET_3", "name": "篮球场3", "type": "运动场", "campus_id": "BUPT", "x": 116.3483, "y": 40.0290},
    {"id": "FAC_BASKET_4", "name": "篮球场4", "type": "运动场", "campus_id": "BUPT", "x": 116.3483, "y": 40.0295},
    {"id": "FAC_TENNIS", "name": "网球场", "type": "运动场", "campus_id": "BUPT", "x": 116.3470, "y": 40.0300},
    {"id": "FAC_BADMINTON", "name": "羽毛球场", "type": "运动场", "campus_id": "BUPT", "x": 116.3470, "y": 40.0305},
    {"id": "FAC_PINGPANG", "name": "乒乓球场", "type": "运动场", "campus_id": "BUPT", "x": 116.3470, "y": 40.0310},
    {"id": "FAC_VOLLEYBALL", "name": "排球场", "type": "运动场", "campus_id": "BUPT", "x": 116.3465, "y": 40.0295},

    # 生活设施
    {"id": "FAC_MARKET_1", "name": "校内超市", "type": "超市", "campus_id": "BUPT", "x": 116.3525, "y": 40.0258},
    {"id": "FAC_MARKET_2", "name": "食堂超市", "type": "超市", "campus_id": "BUPT", "x": 116.3532, "y": 40.0268},
    {"id": "FAC_CAFE", "name": "校园咖啡厅", "type": "咖啡馆", "campus_id": "BUPT", "x": 116.3522, "y": 40.0252},
    {"id": "FAC_ATM_1", "name": "工商银行ATM", "type": "ATM", "campus_id": "BUPT", "x": 116.3528, "y": 40.0248},
    {"id": "FAC_ATM_2", "name": "建设银行ATM", "type": "ATM", "campus_id": "BUPT", "x": 116.3530, "y": 40.0260},
    {"id": "FAC_PHARMACY", "name": "校医院", "type": "医院", "campus_id": "BUPT", "x": 116.3505, "y": 40.0278},
    {"id": "FAC_POST", "name": "快递驿站", "type": "快递", "campus_id": "BUPT", "x": 116.3485, "y": 40.0285},
    {"id": "FAC_PRINT", "name": "打印店", "type": "打印", "campus_id": "BUPT", "x": 116.3515, "y": 40.0265},
    {"id": "FAC_GYM", "name": "体育馆", "type": "体育馆", "campus_id": "BUPT", "x": 116.3460, "y": 40.0280},

    # 出入口
    {"id": "FAC_GATE_NORTH", "name": "北门", "type": "校门", "campus_id": "BUPT", "x": 116.3505, "y": 40.0315},
    {"id": "FAC_GATE_WEST", "name": "西门", "type": "校门", "campus_id": "BUPT", "x": 116.3455, "y": 40.0255},
    {"id": "FAC_GATE_SOUTH", "name": "南门（在建）", "type": "校门", "campus_id": "BUPT", "x": 116.3505, "y": 40.0235},
    {"id": "FAC_GATE_EAST_1", "name": "东侧人行门1", "type": "校门", "campus_id": "BUPT", "x": 116.3545, "y": 40.0260},
    {"id": "FAC_GATE_EAST_2", "name": "东侧人行门2", "type": "校门", "campus_id": "BUPT", "x": 116.3545, "y": 40.0275},

    # 景观
    {"id": "FAC_LAKE", "name": "校园湖泊", "type": "景观", "campus_id": "BUPT", "x": 116.3535, "y": 40.0245},
    {"id": "FAC_GARDEN", "name": "中心花园", "type": "景观", "campus_id": "BUPT", "x": 116.3515, "y": 40.0255},
]

# 道路数据（连接各建筑物的路径）
ROADS = [
    # 主干道（东西向）
    {"id": "RD_MAIN_EAST_1", "from_node": "BUPT_GATE_WEST", "to_node": "BUPT_DORM_1", "distance": 250, "ideal_speed": 5, "congestion": 0.8, "road_types": ["步行", "自行车"]},
    {"id": "RD_MAIN_EAST_2", "from_node": "BUPT_DORM_1", "to_node": "BUPT_DORM_2", "distance": 80, "ideal_speed": 5, "congestion": 1.0, "road_types": ["步行"]},
    {"id": "RD_MAIN_EAST_3", "from_node": "BUPT_DORM_2", "to_node": "BUPT_DORM_3", "distance": 80, "ideal_speed": 5, "congestion": 1.0, "road_types": ["步行"]},
    {"id": "RD_MAIN_EAST_4", "from_node": "BUPT_DORM_3", "to_node": "BUPT_DORM_4", "distance": 80, "ideal_speed": 5, "congestion": 0.9, "road_types": ["步行"]},
    {"id": "RD_MAIN_EAST_5", "from_node": "BUPT_DORM_4", "to_node": "BUPT_DORM_5", "distance": 80, "ideal_speed": 5, "congestion": 0.8, "road_types": ["步行"]},
    {"id": "RD_MAIN_EAST_6", "from_node": "BUPT_DORM_5", "to_node": "BUPT_DORM_6", "distance": 80, "ideal_speed": 5, "congestion": 0.7, "road_types": ["步行"]},
    {"id": "RD_MAIN_EAST_7", "from_node": "BUPT_DORM_6", "to_node": "BUPT_INFO", "distance": 100, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行", "自行车"]},
    {"id": "RD_MAIN_EAST_8", "from_node": "BUPT_INFO", "to_node": "BUPT_GATE_NORTH", "distance": 450, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},

    # 南北向道路
    {"id": "RD_SOUTH_1", "from_node": "BUPT_GATE_WEST", "to_node": "BUPT_TEACH", "distance": 350, "ideal_speed": 5, "congestion": 0.7, "road_types": ["步行", "自行车"]},
    {"id": "RD_SOUTH_2", "from_node": "BUPT_TEACH", "to_node": "BUPT_ADMIN", "distance": 100, "ideal_speed": 5, "congestion": 0.8, "road_types": ["步行"]},
    {"id": "RD_SOUTH_3", "from_node": "BUPT_ADMIN", "to_node": "BUPT_LIB", "distance": 150, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行"]},
    {"id": "RD_SOUTH_4", "from_node": "BUPT_LIB", "to_node": "BUPT_CAFETERIA", "distance": 120, "ideal_speed": 5, "congestion": 0.9, "road_types": ["步行"]},
    {"id": "RD_SOUTH_5", "from_node": "BUPT_CAFETERIA", "to_node": "BUPT_GATE_SOUTH", "distance": 300, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},

    # 到教学楼的路
    {"id": "RD_TO_TEACH_1", "from_node": "BUPT_DORM_1", "to_node": "BUPT_TEACH", "distance": 150, "ideal_speed": 5, "congestion": 0.8, "road_types": ["步行"]},
    {"id": "RD_TO_TEACH_2", "from_node": "BUPT_DORM_2", "to_node": "BUPT_TEACH", "distance": 100, "ideal_speed": 5, "congestion": 0.9, "road_types": ["步行"]},
    {"id": "RD_TO_TEACH_3", "from_node": "BUPT_DORM_3", "to_node": "BUPT_TEACH", "distance": 80, "ideal_speed": 5, "congestion": 1.0, "road_types": ["步行"]},

    # 到图书馆的路
    {"id": "RD_TO_LIB_1", "from_node": "BUPT_DORM_4", "to_node": "BUPT_LIB", "distance": 150, "ideal_speed": 5, "congestion": 0.7, "road_types": ["步行"]},
    {"id": "RD_TO_LIB_2", "from_node": "BUPT_DORM_5", "to_node": "BUPT_LIB", "distance": 100, "ideal_speed": 5, "congestion": 0.8, "road_types": ["步行"]},
    {"id": "RD_TO_LIB_3", "from_node": "BUPT_DORM_6", "to_node": "BUPT_LIB", "distance": 80, "ideal_speed": 5, "congestion": 0.9, "road_types": ["步行"]},

    # 到食堂的路
    {"id": "RD_TO_CAF_1", "from_node": "BUPT_DORM_6", "to_node": "BUPT_CAFETERIA", "distance": 120, "ideal_speed": 5, "congestion": 0.9, "road_types": ["步行"]},
    {"id": "RD_TO_CAF_2", "from_node": "BUPT_INFO", "to_node": "BUPT_CAFETERIA", "distance": 150, "ideal_speed": 5, "congestion": 0.7, "road_types": ["步行", "自行车"]},
    {"id": "RD_TO_CAF_3", "from_node": "BUPT_TEACH", "to_node": "BUPT_CAFETERIA", "distance": 300, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行", "自行车"]},

    # 到运动场的路
    {"id": "RD_TO_SPORT_1", "from_node": "BUPT_DORM_1", "to_node": "FAC_BASKET_1", "distance": 50, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "RD_TO_SPORT_2", "from_node": "FAC_BASKET_1", "to_node": "FAC_TENNIS", "distance": 50, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行"]},
    {"id": "RD_TO_GYM", "from_node": "FAC_TENNIS", "to_node": "FAC_GYM", "distance": 100, "ideal_speed": 5, "congestion": 0.3, "road_types": ["步行"]},

    # 东侧门连接
    {"id": "RD_TO_EAST_1", "from_node": "BUPT_LIB", "to_node": "FAC_GATE_EAST_1", "distance": 200, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},
    {"id": "RD_TO_EAST_2", "from_node": "BUPT_INFO", "to_node": "FAC_GATE_EAST_2", "distance": 200, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},

    # 景观道路
    {"id": "RD_TO_LAKE", "from_node": "BUPT_ADMIN", "to_node": "FAC_LAKE", "distance": 400, "ideal_speed": 3, "congestion": 0.3, "road_types": ["步行"]},
    {"id": "RD_TO_GARDEN", "from_node": "BUPT_LIB", "to_node": "FAC_GARDEN", "distance": 80, "ideal_speed": 3, "congestion": 0.4, "road_types": ["步行"]},
]

# 景点数据（校园内的景点）
ATTRCATIONS = [
    {
        "id": "BUPT",
        "name": "北京邮电大学（沙河校区）",
        "type": "校园",
        "campus_id": "",
        "x": 116.3500,
        "y": 40.0265,
        "heat": 5000,
        "rating": 4.7,
        "tags": ["大学", "校园", "沙河"],
        "description": "北京邮电大学沙河校区位于北京市昌平区沙河高教园区，是一所以信息科技为特色的全国重点大学"
    },
    {
        "id": "BUPT_LIB",
        "name": "图书馆",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3520,
        "y": 40.0255,
        "heat": 5000,
        "rating": 4.8,
        "tags": ["学习", "安静", "图书馆"],
        "description": "沙河校区主图书馆，3层建筑，设施完善，有自习室"
    },
    {
        "id": "BUPT_INFO",
        "name": "信息楼",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3510,
        "y": 40.0270,
        "heat": 3000,
        "rating": 4.5,
        "tags": ["教学", "上课", "信息"],
        "description": "信息学院教学楼，4层高，主要用于日常教学"
    },
    {
        "id": "BUPT_TEACH",
        "name": "综合教学楼",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3490,
        "y": 40.0260,
        "heat": 3500,
        "rating": 4.6,
        "tags": ["教学", "上课"],
        "description": "综合教学楼，4层高，教室众多"
    },
    {
        "id": "BUPT_ADMIN",
        "name": "行政楼",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3500,
        "y": 40.0245,
        "heat": 1500,
        "rating": 4.3,
        "tags": ["行政", "办公"],
        "description": "学校行政办公楼"
    },
    {
        "id": "BUPT_CAFETERIA",
        "name": "鸿通新空间",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3530,
        "y": 40.0265,
        "heat": 4500,
        "rating": 4.5,
        "tags": ["美食", "食堂"],
        "description": "学生食堂，4层建筑，一层风味餐厅、二层基本伙食、三层自助餐厅、四层清真餐厅"
    },
    {
        "id": "BUPT_DORM",
        "name": "学生宿舍区",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3505,
        "y": 40.0280,
        "heat": 2000,
        "rating": 4.2,
        "tags": ["宿舍", "生活"],
        "description": "学生宿舍区，共6栋宿舍楼，每栋6层"
    },
    {
        "id": "BUPT_GYM",
        "name": "体育馆",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3460,
        "y": 40.0280,
        "heat": 2500,
        "rating": 4.6,
        "tags": ["运动", "健身", "体育"],
        "description": "室内体育馆，提供多种运动设施"
    },
    {
        "id": "BUPT_SPORT",
        "name": "运动场",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3475,
        "y": 40.0295,
        "heat": 2000,
        "rating": 4.4,
        "tags": ["运动", "篮球", "网球", "排球"],
        "description": "室外运动场，有篮球场、网球场、排球场等"
    },
    {
        "id": "BUPT_LAKE",
        "name": "校园湖泊",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3535,
        "y": 40.0245,
        "heat": 1000,
        "rating": 4.5,
        "tags": ["景观", "湖泊", "休闲"],
        "description": "校园内的美丽湖泊，环境优雅"
    },
    {
        "id": "BUPT_GARDEN",
        "name": "中心花园",
        "type": "景点",
        "campus_id": "BUPT",
        "x": 116.3515,
        "y": 40.0255,
        "heat": 800,
        "rating": 4.3,
        "tags": ["景观", "花园", "休闲"],
        "description": "位于校园中心的花园绿地"
    },
]


if __name__ == "__main__":
    import json
    import os

    data_dir = os.path.dirname(os.path.abspath(__file__))

    # 保存建筑数据
    with open(os.path.join(data_dir, 'bupt_buildings.json'), 'w', encoding='utf-8') as f:
        json.dump({"buildings": BUILDINGS}, f, ensure_ascii=False, indent=2)

    # 保存设施数据
    with open(os.path.join(data_dir, 'bupt_facilities.json'), 'w', encoding='utf-8') as f:
        json.dump({"facilities": FACILITIES}, f, ensure_ascii=False, indent=2)

    # 保存道路数据
    with open(os.path.join(data_dir, 'bupt_roads.json'), 'w', encoding='utf-8') as f:
        json.dump({"roads": ROADS}, f, ensure_ascii=False, indent=2)

    # 保存景点数据
    with open(os.path.join(data_dir, 'bupt_attractions.json'), 'w', encoding='utf-8') as f:
        json.dump({"attractions": ATTRCATIONS}, f, ensure_ascii=False, indent=2)

    print("北邮沙河校区数据已保存！")
    print(f"建筑: {len(BUILDINGS)} 个")
    print(f"设施: {len(FACILITIES)} 个")
    print(f"道路: {len(ROADS)} 条")
    print(f"景点: {len(ATTRCATIONS)} 个")
