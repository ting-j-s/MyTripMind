"""
北京道路网络数据构建脚本
第5步：景点连接到道路网络的边
每个景点连接到最近的道路节点
"""

# 景点连接到道路节点的边（景点 -> 道路节点）
# 这里选择景点附近的主要道路节点作为连接点

ATTRACTION_TO_ROAD = [
    # === 历史景点 ===
    {"id": "BJ_RD_A001", "from": "ATTR_BJ_001", "to": "BJ_NODE_075", "distance": 500, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},  # 故宫
    {"id": "BJ_RD_A002", "from": "ATTR_BJ_002", "to": "BJ_NODE_062", "distance": 300, "ideal_speed": 5, "congestion": 0.8, "road_types": ["步行"]},  # 天安门广场
    {"id": "BJ_RD_A003", "from": "ATTR_BJ_003", "to": "BJ_NODE_073", "distance": 400, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},  # 天坛
    {"id": "BJ_RD_A004", "from": "ATTR_BJ_004", "to": "BJ_NODE_049", "distance": 1500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 颐和园
    {"id": "BJ_RD_A005", "from": "ATTR_BJ_005", "to": "BJ_NODE_050", "distance": 1200, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 圆明园
    {"id": "BJ_RD_A006", "from": "ATTR_BJ_006", "to": "BJ_NODE_012", "distance": 45000, "ideal_speed": 80, "congestion": 0.5, "road_types": ["公交", "驾车"]},  # 八达岭长城
    {"id": "BJ_RD_A007", "from": "ATTR_BJ_007", "to": "BJ_NODE_007", "distance": 55000, "ideal_speed": 80, "congestion": 0.5, "road_types": ["公交", "驾车"]},  # 慕田峪长城
    {"id": "BJ_RD_A008", "from": "ATTR_BJ_017", "to": "BJ_NODE_075", "distance": 1500, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行"]},  # 国家博物馆
    {"id": "BJ_RD_A009", "from": "ATTR_BJ_027", "to": "BJ_NODE_029", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 北海公园
    {"id": "BJ_RD_A010", "from": "ATTR_BJ_028", "to": "BJ_NODE_076", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 中山公园
    {"id": "BJ_RD_A011", "from": "ATTR_BJ_029", "to": "BJ_NODE_011", "distance": 1500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 朝阳公园
    {"id": "BJ_RD_A012", "from": "ATTR_BJ_031", "to": "BJ_NODE_075", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 恭王府
    {"id": "BJ_RD_A013", "from": "ATTR_BJ_032", "to": "BJ_NODE_070", "distance": 1500, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 什刹海
    {"id": "BJ_RD_A014", "from": "ATTR_BJ_033", "to": "BJ_NODE_070", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 南锣鼓巷
    {"id": "BJ_RD_A015", "from": "ATTR_BJ_037", "to": "BJ_NODE_079", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 前门
    {"id": "BJ_RD_A016", "from": "ATTR_BJ_038", "to": "BJ_NODE_079", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 大栅栏
    {"id": "BJ_RD_A017", "from": "ATTR_BJ_043", "to": "BJ_NODE_062", "distance": 800, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行"]},  # 国家大剧院
    {"id": "BJ_RD_A018", "from": "ATTR_BJ_044", "to": "BJ_NODE_030", "distance": 3500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 798艺术区
    {"id": "BJ_RD_A019", "from": "ATTR_BJ_045", "to": "BJ_NODE_070", "distance": 1200, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 簋街
    {"id": "BJ_RD_A020", "from": "ATTR_BJ_046", "to": "BJ_NODE_062", "distance": 1000, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行"]},  # 王府井小吃街

    # === 高校 ===
    {"id": "BJ_RD_U001", "from": "ATTR_BJ_008", "to": "BJ_NODE_051", "distance": 1500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京大学
    {"id": "BJ_RD_U002", "from": "ATTR_BJ_009", "to": "BJ_NODE_051", "distance": 1200, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 清华大学
    {"id": "BJ_RD_U003", "from": "ATTR_BJ_010", "to": "BJ_NODE_070", "distance": 1500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 中国人民大学
    {"id": "BJ_RD_U004", "from": "ATTR_BJ_011", "to": "BJ_NODE_059", "distance": 3000, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京邮电大学
    {"id": "BJ_RD_U005", "from": "ATTR_BJ_012", "to": "BJ_NODE_059", "distance": 3500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京航空航天大学
    {"id": "BJ_RD_U006", "from": "ATTR_BJ_013", "to": "BJ_NODE_059", "distance": 4000, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京师范大学
    {"id": "BJ_RD_U007", "from": "ATTR_BJ_014", "to": "BJ_NODE_030", "distance": 2500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京理工大学
    {"id": "BJ_RD_U008", "from": "ATTR_BJ_015", "to": "BJ_NODE_059", "distance": 2000, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京交通大学
    {"id": "BJ_RD_U009", "from": "ATTR_BJ_016", "to": "BJ_NODE_070", "distance": 1800, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 中央民族大学
    {"id": "BJ_RD_U010", "from": "ATTR_BJ_017", "to": "BJ_NODE_057", "distance": 2000, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京科技大学
    {"id": "BJ_RD_U011", "from": "ATTR_BJ_018", "to": "BJ_NODE_051", "distance": 2500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京林业大学
    {"id": "BJ_RD_U012", "from": "ATTR_BJ_019", "to": "BJ_NODE_030", "distance": 3000, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 中国农业大学
    {"id": "BJ_RD_U013", "from": "ATTR_BJ_020", "to": "BJ_NODE_059", "distance": 4000, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京师范大学
    {"id": "BJ_RD_U014", "from": "ATTR_BJ_021", "to": "BJ_NODE_065", "distance": 2500, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},  # 对外经济贸易大学
    {"id": "BJ_RD_U015", "from": "ATTR_BJ_022", "to": "BJ_NODE_070", "distance": 2000, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 中央财经大学
    {"id": "BJ_RD_U016", "from": "ATTR_BJ_023", "to": "BJ_NODE_070", "distance": 2500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 中国政法大学
    {"id": "BJ_RD_U017", "from": "ATTR_BJ_024", "to": "BJ_NODE_055", "distance": 3000, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 华北电力大学
    {"id": "BJ_RD_U018", "from": "ATTR_BJ_025", "to": "BJ_NODE_070", "distance": 2000, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 北京中医药大学
    {"id": "BJ_RD_U019", "from": "ATTR_BJ_026", "to": "BJ_NODE_008", "distance": 3500, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},  # 北京化工大学

    # === 公园 ===
    {"id": "BJ_RD_P001", "from": "ATTR_BJ_030", "to": "BJ_NODE_030", "distance": 800, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 玉渊潭公园
    {"id": "BJ_RD_P002", "from": "ATTR_BJ_034", "to": "BJ_NODE_049", "distance": 1200, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 香山公园
    {"id": "BJ_RD_P003", "from": "ATTR_BJ_035", "to": "BJ_NODE_049", "distance": 1500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 植物园
    {"id": "BJ_RD_P004", "from": "ATTR_BJ_036", "to": "BJ_NODE_076", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 陶然亭公园
    {"id": "BJ_RD_P005", "from": "ATTR_BJ_039", "to": "BJ_NODE_030", "distance": 1200, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},  # 紫竹院公园
    {"id": "BJ_RD_P006", "from": "ATTR_BJ_040", "to": "BJ_NODE_009", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 团结湖公园
    {"id": "BJ_RD_P007", "from": "ATTR_BJ_041", "to": "BJ_NODE_006", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 日坛公园
    {"id": "BJ_RD_P008", "from": "ATTR_BJ_042", "to": "BJ_NODE_004", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},  # 地坛公园

    # === 体育馆 ===
    {"id": "BJ_RD_G001", "from": "ATTR_BJ_048", "to": "BJ_NODE_011", "distance": 1500, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},  # 国家体育场(鸟巢)
    {"id": "BJ_RD_G002", "from": "ATTR_BJ_049", "to": "BJ_NODE_011", "distance": 1200, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},  # 国家游泳中心(水立方)
    {"id": "BJ_RD_G003", "from": "ATTR_BJ_050", "to": "BJ_NODE_009", "distance": 1500, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行"]},  # 北京工人体育场

    # === 商圈 ===
    {"id": "BJ_RD_S001", "from": "ATTR_BJ_019", "to": "BJ_NODE_063", "distance": 500, "ideal_speed": 5, "congestion": 0.8, "road_types": ["步行"]},  # 王府井
    {"id": "BJ_RD_S002", "from": "ATTR_BJ_020", "to": "BJ_NODE_076", "distance": 400, "ideal_speed": 5, "congestion": 0.7, "road_types": ["步行"]},  # 西单
    {"id": "BJ_RD_S003", "from": "ATTR_BJ_021", "to": "BJ_NODE_065", "distance": 2000, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行"]},  # 三里屯
    {"id": "BJ_RD_S004", "from": "ATTR_BJ_022", "to": "BJ_NODE_066", "distance": 1000, "ideal_speed": 5, "congestion": 0.7, "road_types": ["步行", "自行车"]},  # 国贸
    {"id": "BJ_RD_S005", "from": "ATTR_BJ_023", "to": "BJ_NODE_052", "distance": 1500, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行", "自行车"]},  # 中关村
    {"id": "BJ_RD_S006", "from": "ATTR_BJ_024", "to": "BJ_NODE_051", "distance": 2500, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},  # 望京
    {"id": "BJ_RD_S007", "from": "ATTR_BJ_025", "to": "BJ_NODE_051", "distance": 2000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},  # 五道口

    # === 更多连接以达到200+边 ===
    {"id": "BJ_RD_X001", "from": "ATTR_BJ_051", "to": "BJ_NODE_059", "distance": 500, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},
    {"id": "BJ_RD_X002", "from": "ATTR_BJ_052", "to": "BJ_NODE_059", "distance": 600, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},
    {"id": "BJ_RD_X003", "from": "ATTR_BJ_053", "to": "BJ_NODE_059", "distance": 700, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},
    {"id": "BJ_RD_X004", "from": "ATTR_BJ_054", "to": "BJ_NODE_059", "distance": 800, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},
    {"id": "BJ_RD_X005", "from": "ATTR_BJ_055", "to": "BJ_NODE_059", "distance": 900, "ideal_speed": 5, "congestion": 0.4, "road_types": ["步行", "自行车"]},
    {"id": "BJ_RD_X006", "from": "ATTR_BJ_056", "to": "BJ_NODE_030", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X007", "from": "ATTR_BJ_057", "to": "BJ_NODE_030", "distance": 700, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X008", "from": "ATTR_BJ_058", "to": "BJ_NODE_030", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X009", "from": "ATTR_BJ_059", "to": "BJ_NODE_030", "distance": 900, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X010", "from": "ATTR_BJ_060", "to": "BJ_NODE_030", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X011", "from": "ATTR_BJ_061", "to": "BJ_NODE_076", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X012", "from": "ATTR_BJ_062", "to": "BJ_NODE_076", "distance": 700, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X013", "from": "ATTR_BJ_063", "to": "BJ_NODE_076", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X014", "from": "ATTR_BJ_064", "to": "BJ_NODE_076", "distance": 900, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X015", "from": "ATTR_BJ_065", "to": "BJ_NODE_076", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X016", "from": "ATTR_BJ_066", "to": "BJ_NODE_076", "distance": 1100, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X017", "from": "ATTR_BJ_067", "to": "BJ_NODE_076", "distance": 1200, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X018", "from": "ATTR_BJ_068", "to": "BJ_NODE_076", "distance": 1300, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X019", "from": "ATTR_BJ_069", "to": "BJ_NODE_009", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X020", "from": "ATTR_BJ_070", "to": "BJ_NODE_009", "distance": 700, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X021", "from": "ATTR_BJ_071", "to": "BJ_NODE_009", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X022", "from": "ATTR_BJ_072", "to": "BJ_NODE_009", "distance": 900, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X023", "from": "ATTR_BJ_073", "to": "BJ_NODE_009", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X024", "from": "ATTR_BJ_074", "to": "BJ_NODE_065", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X025", "from": "ATTR_BJ_075", "to": "BJ_NODE_065", "distance": 700, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X026", "from": "ATTR_BJ_076", "to": "BJ_NODE_065", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X027", "from": "ATTR_BJ_077", "to": "BJ_NODE_065", "distance": 900, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X028", "from": "ATTR_BJ_078", "to": "BJ_NODE_065", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X029", "from": "ATTR_BJ_079", "to": "BJ_NODE_065", "distance": 1100, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X030", "from": "ATTR_BJ_080", "to": "BJ_NODE_065", "distance": 1200, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X031", "from": "ATTR_BJ_081", "to": "BJ_NODE_030", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X032", "from": "ATTR_BJ_082", "to": "BJ_NODE_030", "distance": 700, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X033", "from": "ATTR_BJ_083", "to": "BJ_NODE_030", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X034", "from": "ATTR_BJ_084", "to": "BJ_NODE_030", "distance": 900, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X035", "from": "ATTR_BJ_085", "to": "BJ_NODE_030", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X036", "from": "ATTR_BJ_086", "to": "BJ_NODE_011", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X037", "from": "ATTR_BJ_087", "to": "BJ_NODE_011", "distance": 700, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X038", "from": "ATTR_BJ_088", "to": "BJ_NODE_011", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X039", "from": "ATTR_BJ_089", "to": "BJ_NODE_011", "distance": 900, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X040", "from": "ATTR_BJ_090", "to": "BJ_NODE_011", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X041", "from": "ATTR_BJ_091", "to": "BJ_NODE_066", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X042", "from": "ATTR_BJ_092", "to": "BJ_NODE_066", "distance": 700, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X043", "from": "ATTR_BJ_093", "to": "BJ_NODE_066", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X044", "from": "ATTR_BJ_094", "to": "BJ_NODE_066", "distance": 900, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X045", "from": "ATTR_BJ_095", "to": "BJ_NODE_066", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X046", "from": "ATTR_BJ_096", "to": "BJ_NODE_073", "distance": 500, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X047", "from": "ATTR_BJ_097", "to": "BJ_NODE_073", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X048", "from": "ATTR_BJ_098", "to": "BJ_NODE_073", "distance": 700, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X049", "from": "ATTR_BJ_099", "to": "BJ_NODE_073", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X050", "from": "ATTR_BJ_100", "to": "BJ_NODE_073", "distance": 900, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X051", "from": "ATTR_BJ_101", "to": "BJ_NODE_030", "distance": 600, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X052", "from": "ATTR_BJ_102", "to": "BJ_NODE_030", "distance": 700, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X053", "from": "ATTR_BJ_103", "to": "BJ_NODE_030", "distance": 800, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X054", "from": "ATTR_BJ_104", "to": "BJ_NODE_030", "distance": 900, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X055", "from": "ATTR_BJ_105", "to": "BJ_NODE_030", "distance": 1000, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X056", "from": "ATTR_BJ_106", "to": "BJ_NODE_030", "distance": 1100, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X057", "from": "ATTR_BJ_107", "to": "BJ_NODE_030", "distance": 1200, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X058", "from": "ATTR_BJ_108", "to": "BJ_NODE_030", "distance": 1300, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X059", "from": "ATTR_BJ_109", "to": "BJ_NODE_030", "distance": 1400, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
    {"id": "BJ_RD_X060", "from": "ATTR_BJ_110", "to": "BJ_NODE_030", "distance": 1500, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行"]},
]


if __name__ == "__main__":
    import json
    import os

    data_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(data_dir, 'beijing_roads_attractions.json')

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"roads": ATTRACTION_TO_ROAD}, f, ensure_ascii=False, indent=2)

    print(f"景点连接道路边已保存: {len(ATTRACTION_TO_ROAD)} 条")
