"""
扩充用户数据
目标：≥10个用户
"""

USERS = [
    {"username": "旅游达人", "password": "123456", "interests": ["历史", "美食", "自然风光"]},
    {"username": "校园探索", "password": "123456", "interests": ["校园", "建筑", "摄影"]},
    {"username": "吃货小王", "password": "123456", "interests": ["美食", "购物"]},
    {"username": "历史爱好者", "password": "123456", "interests": ["历史", "博物馆", "古迹"]},
    {"username": "户外运动", "password": "123456", "interests": ["运动", "自然风光", "公园"]},
    {"username": "文艺青年", "password": "123456", "interests": ["艺术", "博物馆", "建筑"]},
    {"username": "科技迷", "password": "123456", "interests": ["科技", "高校", "建筑"]},
    {"username": "购物狂", "password": "123456", "interests": ["购物", "商圈", "美食"]},
    {"username": "摄影爱好者", "password": "123456", "interests": ["建筑", "自然风光", "历史"]},
    {"username": "周末游客", "password": "123456", "interests": ["公园", "美食", "购物"]},
    {"username": "长城爱好者", "password": "123456", "interests": ["历史", "古迹", "自然风光"]},
    {"username": "博物馆打卡", "password": "123456", "interests": ["博物馆", "历史", "艺术"]},
]

if __name__ == "__main__":
    import json
    import os
    from datetime import datetime

    data_dir = os.path.dirname(os.path.abspath(__file__))

    # 生成用户数据
    users = []
    for i, u in enumerate(USERS):
        users.append({
            "id": f"user_{i+1:03d}",
            "username": u["username"],
            "password": u["password"],
            "interests": u["interests"],
            "favorites": [],
            "visited": [],
            "create_time": f"2026-03-{10+i%20+1:02d}"
        })

    filepath = os.path.join(data_dir, 'users.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"users": users}, f, ensure_ascii=False, indent=2)

    print(f"用户数据已保存: {len(users)} 个用户")
