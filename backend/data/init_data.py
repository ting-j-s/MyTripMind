"""
数据初始化脚本
生成测试数据
"""

import json
import os
from datetime import datetime


def generate_test_data():
    """生成测试数据"""

    # 1. 用户数据
    users = {
        "users": [
            {
                "id": "user_001",
                "username": "张三",
                "password": "123456",
                "interests": ["历史", "校园"],
                "favorites": ["BUPT_LIB"],
                "visited": ["BUPT_LIB", "BUPT_CAFETERIA"],
                "create_time": "2026-03-01"
            },
            {
                "id": "user_002",
                "username": "李四",
                "password": "123456",
                "interests": ["美食", "自然"],
                "favorites": [],
                "visited": [],
                "create_time": "2026-03-02"
            }
        ]
    }

    # 2. 景点/校园数据
    attractions = {
        "attractions": [
            {
                "id": "BUPT",
                "name": "北京邮电大学（沙河校区）",
                "type": "校园",
                "x": 116.352,
                "y": 40.025,
                "description": "北京邮电大学沙河校区位于北京市昌平区沙河高教园区"
            },
            {
                "id": "BUPT_LIB",
                "name": "图书馆",
                "type": "景点",
                "campus_id": "BUPT",
                "x": 116.352,
                "y": 40.025,
                "heat": 5000,
                "rating": 4.8,
                "tags": ["学习", "安静", "图书馆"],
                "description": "沙河校区主图书馆，设施完善"
            },
            {
                "id": "BUPT_CAFETERIA",
                "name": "学生食堂",
                "type": "景点",
                "campus_id": "BUPT",
                "x": 116.353,
                "y": 40.026,
                "heat": 3000,
                "rating": 4.5,
                "tags": ["美食", "食堂"],
                "description": "学生食堂，饭菜种类丰富"
            },
            {
                "id": "BUPT_DORM_A",
                "name": "学生宿舍A栋",
                "type": "景点",
                "campus_id": "BUPT",
                "x": 116.351,
                "y": 40.024,
                "heat": 1000,
                "rating": 4.2,
                "tags": ["宿舍", "生活"],
                "description": "本科学生宿舍"
            },
            {
                "id": "BUPT_GYM",
                "name": "体育馆",
                "type": "景点",
                "campus_id": "BUPT",
                "x": 116.354,
                "y": 40.027,
                "heat": 2000,
                "rating": 4.6,
                "tags": ["运动", "健身"],
                "description": "室内体育馆，篮球场、羽毛球场等"
            }
        ]
    }

    # 3. 建筑数据
    buildings = {
        "buildings": [
            {
                "id": "BUPT_LIB",
                "name": "图书馆",
                "type": "教学楼",
                "campus_id": "BUPT",
                "x": 116.352,
                "y": 40.025,
                "floors": 5,
                "rooms": ["101", "102", "201", "202", "301", "自息室"],
                "elevators": ["A"],
                "entrances": ["东门", "西门"]
            },
            {
                "id": "BUPT_CAFETERIA",
                "name": "学生食堂",
                "type": "食堂",
                "campus_id": "BUPT",
                "x": 116.353,
                "y": 40.026,
                "floors": 3,
                "rooms": ["一层", "二层", "三层"],
                "elevators": [],
                "entrances": ["南门", "北门"]
            }
        ]
    }

    # 4. 设施数据
    facilities = {
        "facilities": [
            {"id": "FAC_001", "name": "图书馆超市", "type": "超市", "campus_id": "BUPT", "x": 116.3521, "y": 40.0251},
            {"id": "FAC_002", "name": "图书馆洗手间", "type": "洗手间", "campus_id": "BUPT", "x": 116.3522, "y": 40.0252},
            {"id": "FAC_003", "name": "咖啡厅", "type": "咖啡馆", "campus_id": "BUPT", "x": 116.3523, "y": 40.0253},
            {"id": "FAC_004", "name": "食堂洗手间", "type": "洗手间", "campus_id": "BUPT", "x": 116.3531, "y": 40.0261},
            {"id": "FAC_005", "name": "食堂超市", "type": "超市", "campus_id": "BUPT", "x": 116.3532, "y": 40.0262},
            {"id": "FAC_006", "name": "体育馆器材室", "type": "服务中心", "campus_id": "BUPT", "x": 116.354, "y": 40.027},
            {"id": "FAC_007", "name": "ATM机", "type": "ATM", "campus_id": "BUPT", "x": 116.3525, "y": 40.0255},
        ]
    }

    # 5. 道路数据
    roads = {
        "roads": [
            {"id": "RD_001", "from": "BUPT_LIB", "to": "BUPT_CAFETERIA", "distance": 150, "ideal_speed": 5, "congestion": 1.0, "road_types": ["步行", "自行车"]},
            {"id": "RD_002", "from": "BUPT_LIB", "to": "BUPT_DORM_A", "distance": 120, "ideal_speed": 5, "congestion": 0.8, "road_types": ["步行", "自行车"]},
            {"id": "RD_003", "from": "BUPT_CAFETERIA", "to": "BUPT_GYM", "distance": 180, "ideal_speed": 5, "congestion": 1.0, "road_types": ["步行"]},
            {"id": "RD_004", "from": "BUPT_DORM_A", "to": "BUPT_GYM", "distance": 200, "ideal_speed": 5, "congestion": 0.6, "road_types": ["步行", "自行车"]},
            {"id": "RD_005", "from": "BUPT_LIB", "to": "BUPT_GYM", "distance": 250, "ideal_speed": 5, "congestion": 0.5, "road_types": ["步行", "自行车"]},
            # 设施连接道路
            {"id": "RD_006", "from": "BUPT_LIB", "to": "FAC_001", "distance": 30, "ideal_speed": 3, "congestion": 1.0, "road_types": ["步行"]},
            {"id": "RD_007", "from": "BUPT_LIB", "to": "FAC_002", "distance": 20, "ideal_speed": 3, "congestion": 1.0, "road_types": ["步行"]},
            {"id": "RD_008", "from": "BUPT_LIB", "to": "FAC_003", "distance": 40, "ideal_speed": 3, "congestion": 0.8, "road_types": ["步行"]},
            {"id": "RD_009", "from": "BUPT_CAFETERIA", "to": "FAC_004", "distance": 25, "ideal_speed": 3, "congestion": 1.0, "road_types": ["步行"]},
            {"id": "RD_010", "from": "BUPT_CAFETERIA", "to": "FAC_005", "distance": 35, "ideal_speed": 3, "congestion": 0.9, "road_types": ["步行"]},
        ]
    }

    # 6. 日记数据
    diaries = {
        "diaries": [
            {
                "id": "diary_001",
                "user_id": "user_001",
                "title": "北邮沙河一日游",
                "content": "今天参观了北京邮电大学沙河校区，校园很大，图书馆很气派，食堂饭菜也很好吃。",
                "images": [],
                "videos": [],
                "location_id": "BUPT",
                "create_time": "2026-03-15",
                "view_count": 100,
                "ratings": [5.0, 4.5]
            },
            {
                "id": "diary_002",
                "user_id": "user_001",
                "title": "图书馆学习记",
                "content": "在图书馆待了一整天，学习效率很高。图书馆设施很好，有空调和饮水机。",
                "images": [],
                "videos": [],
                "location_id": "BUPT_LIB",
                "create_time": "2026-03-10",
                "view_count": 50,
                "ratings": [4.8]
            }
        ]
    }

    # 7. 美食数据
    foods = {
        "foods": [
            {"id": "FOOD_001", "name": "红烧肉", "cuisine": "川菜", "restaurant": "食堂一层", "campus_id": "BUPT", "x": 116.353, "y": 40.026, "heat": 500, "rating": 4.5},
            {"id": "FOOD_002", "name": "宫保鸡丁", "cuisine": "川菜", "restaurant": "食堂一层", "campus_id": "BUPT", "x": 116.353, "y": 40.026, "heat": 450, "rating": 4.6},
            {"id": "FOOD_003", "name": "麻辣烫", "cuisine": "川菜", "restaurant": "食堂二层", "campus_id": "BUPT", "x": 116.353, "y": 40.026, "heat": 600, "rating": 4.7},
            {"id": "FOOD_004", "name": "糖醋里脊", "cuisine": "鲁菜", "restaurant": "食堂一层", "campus_id": "BUPT", "x": 116.353, "y": 40.026, "heat": 400, "rating": 4.4},
            {"id": "FOOD_005", "name": "清蒸鱼", "cuisine": "粤菜", "restaurant": "食堂三层", "campus_id": "BUPT", "x": 116.353, "y": 40.026, "heat": 350, "rating": 4.8},
        ]
    }

    return {
        'users.json': users,
        'attractions.json': attractions,
        'buildings.json': buildings,
        'facilities.json': facilities,
        'roads.json': roads,
        'diaries.json': diaries,
        'foods.json': foods
    }


def init_data_files():
    """初始化数据文件"""
    # 获取数据目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')

    # 确保目录存在
    os.makedirs(data_dir, exist_ok=True)

    # 生成数据
    data = generate_test_data()

    # 写入文件
    for filename, content in data.items():
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        print(f"Created: {filepath}")

    print("\nData initialization completed!")
    print(f"Files saved to: {data_dir}")


if __name__ == '__main__':
    init_data_files()
