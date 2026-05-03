"""
高德地图POI数据爬虫
用于爬取北京景点数据
"""

import requests
import json
import time

# ==================== 配置 ====================

# 替换成你的高德API Key
GAODE_API_KEY = "你的Key"

# 北京市区域编码
BEIJING_CITY_CODE = "110100"

# ==================== POI类型 ====================

# 旅游景点相关类型
TOURISM_TYPES = [
    ("风景名胜", "110000"),   # 旅游景点
    ("高等院校", "141200"),   # 大学
    ("博物馆", "110200"),     # 博物馆
    ("公园", "110101"),       # 公园
    ("寺庙道观", "110205"),   # 寺庙
    ("历史遗迹", "110207"),   # 历史遗迹
]

# ==================== 爬虫函数 ====================

def search_poi(keywords, city="北京", offset=20, page=1):
    """
    搜索POI

    参数:
        keywords: 关键词
        city: 城市
        offset: 每页数量
        page: 页码

    返回:
        POI列表
    """
    url = "https://restapi.amap.com/v3/place/text"
    params = {
        "key": GAODE_API_KEY,
        "keywords": keywords,
        "city": city,
        "citylimit": "true",  # 限制在该城市
        "offset": offset,
        "page": page,
        "extensions": "all"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data["status"] == "1" and int(data["count"]) > 0:
            return data["pois"]
        return []
    except Exception as e:
        print(f"请求失败: {e}")
        return []


def crawl_attractions(keywords, max_count=200):
    """
    爬取指定类型的景点

    参数:
        keywords: 景点类型关键词
        max_count: 最大数量

    返回:
        景点列表
    """
    all_pois = []
    page = 1

    while len(all_pois) < max_count:
        pois = search_poi(keywords, page=page)

        if not pois:
            break

        all_pois.extend(pois)
        print(f"  {keywords}: 已爬取 {len(all_pois)} 条...")

        if len(pois) < 20:  # 最后一页
            break

        page += 1
        time.sleep(0.3)  # 避免请求过快

    return all_pois[:max_count]


def convert_poi_format(poi):
    """
    转换POI格式为系统数据格式
    """
    # 解析坐标
    location = poi.get("location", "").split(",")
    x = float(location[0]) if len(location) >= 1 else 0
    y = float(location[1]) if len(location) >= 2 else 0

    # 获取评分（高德没有评分，用热度代替）
    heat = int(poi.get("biz_type", "0") or "0") * 100

    # 解析标签
    tag = poi.get("type", "").split(";")[0] if poi.get("type") else ""

    return {
        "id": f"ATTR_{poi.get('id', '')}",
        "name": poi.get("name", ""),
        "type": tag or "景点",
        "campus_id": "",  # 旅游景点没有campus_id
        "x": x,
        "y": y,
        "heat": heat,
        "rating": 4.0,  # 默认评分
        "tags": poi.get("type", "").split(";"),
        "description": poi.get("address", ""),
        "image_url": ""
    }


def crawl_beijing_tourism():
    """
    爬取北京旅游数据
    """
    print("=" * 50)
    print("开始爬取北京景点数据...")
    print("=" * 50)

    all_attractions = []
    seen_ids = set()  # 去重

    for type_name, type_code in TOURISM_TYPES:
        print(f"\n正在爬取: {type_name}")
        pois = crawl_attractions(type_name, max_count=50)

        for poi in pois:
            if poi.get("id") not in seen_ids:
                seen_ids.add(poi.get("id"))
                attraction = convert_poi_format(poi)
                all_attractions.append(attraction)

        time.sleep(0.5)

    print(f"\n总共爬取到 {len(all_attractions)} 个景点")

    return all_attractions


def save_data(attractions, filename="attractions_beijing.json"):
    """
    保存数据到文件
    """
    import os
    data_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(data_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"attractions": attractions}, f, ensure_ascii=False, indent=2)

    print(f"数据已保存到: {filepath}")


# ==================== 主程序 ====================

if __name__ == "__main__":
    print("""
    ================================================
    高德地图POI数据爬虫
    ================================================

    使用说明：
    1. 首先在高德开放平台申请API Key
       https://console.amap.com/dev/key/app

    2. 将API Key填入脚本中的 GAODE_API_KEY 变量

    3. 运行脚本：
       python backend/data/crawler.py

    ================================================
    """)

    if GAODE_API_KEY == "你的Key":
        print("错误：请先修改脚本中的 GAODE_API_KEY 为你的高德API Key")
        print("修改方法：编辑 backend/data/crawler.py 第10行")
    else:
        # 爬取数据
        attractions = crawl_beijing_tourism()

        # 保存数据
        if attractions:
            save_data(attractions)
            print("\n完成！")
        else:
            print("\n爬取失败，请检查API Key是否正确")
