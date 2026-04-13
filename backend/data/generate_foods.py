"""
扩充美食数据
目标：≥50个美食
"""

FOODS = [
    # 故宫/王府井附近
    {"name": "北京烤鸭", "cuisine": "京菜", "restaurant": "全聚德", "x": 116.3975, "y": 39.9180, "heat": 5000, "rating": 4.8},
    {"name": "炸酱面", "cuisine": "京菜", "restaurant": "海碗居", "x": 116.4175, "y": 39.9140, "heat": 3500, "rating": 4.5},
    {"name": "豆汁儿", "cuisine": "京菜", "restaurant": "护国寺小吃", "x": 116.4075, "y": 39.9320, "heat": 2000, "rating": 4.0},
    {"name": "卤煮火烧", "cuisine": "京菜", "restaurant": "小肠陈", "x": 116.4075, "y": 39.8920, "heat": 1800, "rating": 4.3},
    {"name": "爆肚", "cuisine": "京菜", "restaurant": "爆肚冯", "x": 116.3975, "y": 39.8980, "heat": 1500, "rating": 4.4},

    # 川菜
    {"name": "宫保鸡丁", "cuisine": "川菜", "restaurant": "川菜馆", "x": 116.4075, "y": 39.9140, "heat": 4000, "rating": 4.5},
    {"name": "麻婆豆腐", "cuisine": "川菜", "restaurant": "川菜馆", "x": 116.4175, "y": 39.9140, "heat": 3500, "rating": 4.5},
    {"name": "水煮鱼", "cuisine": "川菜", "restaurant": "沸腾鱼乡", "x": 116.4075, "y": 39.9240, "heat": 3800, "rating": 4.6},
    {"name": "回锅肉", "cuisine": "川菜", "restaurant": "川菜馆", "x": 116.3975, "y": 39.9140, "heat": 3000, "rating": 4.4},
    {"name": "酸菜鱼", "cuisine": "川菜", "restaurant": "川菜馆", "x": 116.4275, "y": 39.9240, "heat": 2800, "rating": 4.3},

    # 粤菜
    {"name": "白切鸡", "cuisine": "粤菜", "restaurant": "粤菜馆", "x": 116.4075, "y": 39.9140, "heat": 2500, "rating": 4.5},
    {"name": "叉烧", "cuisine": "粤菜", "restaurant": "粤菜馆", "x": 116.4175, "y": 39.9240, "heat": 2200, "rating": 4.4},
    {"name": "虾饺", "cuisine": "粤菜", "restaurant": "点心王子", "x": 116.4575, "y": 39.9085, "heat": 3000, "rating": 4.6},
    {"name": "烧鹅", "cuisine": "粤菜", "restaurant": "粤菜馆", "x": 116.4675, "y": 39.9085, "heat": 2800, "rating": 4.5},
    {"name": "肠粉", "cuisine": "粤菜", "restaurant": "粤菜馆", "x": 116.4775, "y": 39.9085, "heat": 2600, "rating": 4.4},

    # 火锅
    {"name": "铜锅涮肉", "cuisine": "火锅", "restaurant": "东来顺", "x": 116.4075, "y": 39.9140, "heat": 4200, "rating": 4.7},
    {"name": "重庆火锅", "cuisine": "火锅", "restaurant": "海底捞", "x": 116.4575, "y": 39.9085, "heat": 5000, "rating": 4.8},
    {"name": "潮汕牛肉锅", "cuisine": "火锅", "restaurant": "八合里", "x": 116.3175, "y": 39.9825, "heat": 3500, "rating": 4.5},
    {"name": "羊蝎子", "cuisine": "火锅", "restaurant": "老城一锅", "x": 116.3875, "y": 39.9425, "heat": 3000, "rating": 4.4},
    {"name": "串串香", "cuisine": "火锅", "restaurant": "钢管五厂", "x": 116.3975, "y": 39.9325, "heat": 2800, "rating": 4.3},

    # 小吃/快餐
    {"name": "煎饼果子", "cuisine": "小吃", "restaurant": "煎饼侠", "x": 116.4075, "y": 39.9140, "heat": 2500, "rating": 4.2},
    {"name": "肉夹馍", "cuisine": "小吃", "restaurant": "腊牛肉", "x": 116.4175, "y": 39.9240, "heat": 2200, "rating": 4.3},
    {"name": "凉皮", "cuisine": "小吃", "restaurant": "凉皮店", "x": 116.4275, "y": 39.9140, "heat": 1800, "rating": 4.1},
    {"name": "臭豆腐", "cuisine": "小吃", "restaurant": "王府井小吃街", "x": 116.4175, "y": 39.9145, "heat": 2000, "rating": 4.0},
    {"name": "驴打滚", "cuisine": "小吃", "restaurant": "护国寺小吃", "x": 116.4075, "y": 39.9320, "heat": 1500, "rating": 4.2},

    # 西餐
    {"name": "牛排", "cuisine": "西餐", "restaurant": "必胜客", "x": 116.4075, "y": 39.9140, "heat": 3000, "rating": 4.3},
    {"name": "披萨", "cuisine": "西餐", "restaurant": "达美乐", "x": 116.4575, "y": 39.9085, "heat": 2800, "rating": 4.2},
    {"name": "汉堡", "cuisine": "西餐", "restaurant": "麦当劳", "x": 116.4175, "y": 39.9140, "heat": 3500, "rating": 4.1},
    {"name": "意面", "cuisine": "西餐", "restaurant": "萨莉亚", "x": 116.4675, "y": 39.9085, "heat": 2200, "rating": 4.2},

    # 日料/韩餐
    {"name": "寿司", "cuisine": "日料", "restaurant": "元气寿司", "x": 116.4075, "y": 39.9140, "heat": 2800, "rating": 4.5},
    {"name": "拉面", "cuisine": "日料", "restaurant": "一风堂", "x": 116.4575, "y": 39.9085, "heat": 3200, "rating": 4.6},
    {"name": "烤肉", "cuisine": "韩餐", "restaurant": "烤肉匠", "x": 116.4675, "y": 39.9085, "heat": 3500, "rating": 4.5},
    {"name": "石锅拌饭", "cuisine": "韩餐", "restaurant": "韩式拌饭", "x": 116.4775, "y": 39.9085, "heat": 2500, "rating": 4.3},
    {"name": "寿司拼盘", "cuisine": "日料", "restaurant": "筑地市场", "x": 116.4875, "y": 39.9025, "heat": 3000, "rating": 4.4},

    # 饮品/甜点
    {"name": "珍珠奶茶", "cuisine": "饮品", "restaurant": "喜茶", "x": 116.4075, "y": 39.9140, "heat": 4000, "rating": 4.5},
    {"name": "芋泥波波", "cuisine": "饮品", "restaurant": "一点点", "x": 116.4175, "y": 39.9140, "heat": 3500, "rating": 4.4},
    {"name": "提拉米苏", "cuisine": "甜点", "restaurant": "味多美", "x": 116.4075, "y": 39.9240, "heat": 2000, "rating": 4.3},
    {"name": "芝士蛋糕", "cuisine": "甜点", "restaurant": "巴黎贝甜", "x": 116.4575, "y": 39.9085, "heat": 2200, "rating": 4.4},
    {"name": "冰淇淋", "cuisine": "甜点", "restaurant": "哈根达斯", "x": 116.4675, "y": 39.9085, "heat": 2500, "rating": 4.5},

    # 高校周边美食
    {"name": "北门炸鸡", "cuisine": "快餐", "restaurant": "北邮北门", "x": 116.3455, "y": 40.0255, "heat": 1800, "rating": 4.0},
    {"name": "学五食堂", "cuisine": "食堂", "restaurant": "北大校内", "x": 116.3123, "y": 39.9993, "heat": 2000, "rating": 4.2},
    {"name": "清华麻辣香锅", "cuisine": "川菜", "restaurant": "清华西门", "x": 116.3223, "y": 39.9996, "heat": 2200, "rating": 4.3},
    {"name": "中关村咖啡", "cuisine": "饮品", "restaurant": "创业大街", "x": 116.3125, "y": 39.9835, "heat": 2500, "rating": 4.4},
    {"name": "五道口枣糕", "cuisine": "小吃", "restaurant": "五道口", "x": 116.3225, "y": 39.9985, "heat": 1800, "rating": 4.1},

    # 更多美食凑数
    {"name": "糖醋排骨", "cuisine": "浙菜", "restaurant": "浙菜馆", "x": 116.3975, "y": 39.9140, "heat": 2000, "rating": 4.3},
    {"name": "东坡肉", "cuisine": "浙菜", "restaurant": "浙菜馆", "x": 116.4075, "y": 39.9240, "heat": 2200, "rating": 4.4},
    {"name": "西湖醋鱼", "cuisine": "浙菜", "restaurant": "浙菜馆", "x": 116.4175, "y": 39.9140, "heat": 1800, "rating": 4.2},
    {"name": "小笼包", "cuisine": "浙菜", "restaurant": "南翔小笼", "x": 116.4275, "y": 39.9040, "heat": 2500, "rating": 4.5},
    {"name": "生煎包", "cuisine": "浙菜", "restaurant": "上海生煎", "x": 116.4375, "y": 39.9140, "heat": 2300, "rating": 4.4},
    {"name": "佛跳墙", "cuisine": "闽菜", "restaurant": "闽菜馆", "x": 116.4475, "y": 39.9040, "heat": 3000, "rating": 4.6},
    {"name": "肉燕", "cuisine": "闽菜", "restaurant": "闽菜馆", "x": 116.4575, "y": 39.9140, "heat": 1500, "rating": 4.2},
    {"name": "麻辣香锅", "cuisine": "川菜", "restaurant": "香锅居", "x": 116.4675, "y": 39.9240, "heat": 2800, "rating": 4.4},
    {"name": "东北饺子", "cuisine": "东北菜", "restaurant": "东北饺子馆", "x": 116.4775, "y": 39.9340, "heat": 2000, "rating": 4.3},
    {"name": "锅包肉", "cuisine": "东北菜", "restaurant": "东北菜馆", "x": 116.4875, "y": 39.9140, "heat": 2200, "rating": 4.4},
    {"name": "杀猪菜", "cuisine": "东北菜", "restaurant": "东北菜馆", "x": 116.4975, "y": 39.9240, "heat": 1800, "rating": 4.2},
    {"name": "烤冷面", "cuisine": "小吃", "restaurant": "路边摊", "x": 116.3275, "y": 39.9825, "heat": 1500, "rating": 4.0},
    {"name": "锅盔", "cuisine": "小吃", "restaurant": "锅盔店", "x": 116.3375, "y": 39.9925, "heat": 1200, "rating": 4.1},
    {"name": "鸡蛋灌饼", "cuisine": "小吃", "restaurant": "早餐摊", "x": 116.3475, "y": 40.0025, "heat": 1000, "rating": 4.0},
    {"name": "包子", "cuisine": "小吃", "restaurant": "庆丰包子", "x": 116.3575, "y": 40.0125, "heat": 1500, "rating": 4.2},
]

if __name__ == "__main__":
    import json
    import os

    data_dir = os.path.dirname(os.path.abspath(__file__))

    # 生成美食数据
    foods = []
    for i, f in enumerate(FOODS):
        foods.append({
            "id": f"FOOD_{i+1:03d}",
            "name": f["name"],
            "cuisine": f["cuisine"],
            "restaurant": f["restaurant"],
            "campus_id": "",
            "x": f["x"],
            "y": f["y"],
            "heat": f["heat"],
            "rating": f["rating"]
        })

    filepath = os.path.join(data_dir, 'foods.json')
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"foods": foods}, f, ensure_ascii=False, indent=2)

    print(f"美食数据已保存: {len(foods)} 个美食")
