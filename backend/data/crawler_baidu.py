"""
百度地图POI数据爬虫
用于爬取北京景点数据
"""

import requests
import json
import time

# ==================== 配置 ====================

# 替换成你的百度地图AK
BAIDU_AK = "zPelSBptFgnYEpbCF8utY3UBYJHvmkE3"

# ==================== POI类型 ====================

# 搜索的关键词
SEARCH_KEYWORDS = [
    "景点",
    "博物馆",
    "公园",
    "高等院校",
    "寺庙",
    "古迹",
    "广场",
    "纪念馆",
    "动物园",
    "植物园",
]

# ==================== 爬虫函数 ====================

def search_poi(keyword, region="北京", page_size=20, page_num=0):
    """
    百度地图POI搜索

    参数:
        keyword: 关键词
        region: 地区
        page_size: 每页数量
        page_num: 页码

    返回:
        POI列表
    """
    url = "https://api.map.baidu.com/place/v2/search"

    params = {
        "query": keyword,
        "region": region,
        "city_limit": "true",
        "output": "json",
        "ak": BAIDU_AK,
        "page_size": page_size,
        "page_num": page_num
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == 0 and data.get("results"):
            return data["results"]
        return []

    except Exception as e:
        print(f"  请求失败: {e}")
        return []


def crawl_poi_by_keyword(keyword, max_count=50):
    """
    按关键词爬取POI
    """
    all_results = []
    page = 0

    while len(all_results) < max_count:
        pois = search_poi(keyword, page_size=20, page_num=page)

        if not pois:
            break

        all_results.extend(pois)
        print(f"  关键词'{keyword}': 已爬取 {len(all_results)} 条...")

        if len(pois) < 20:
            break

        page += 1
        time.sleep(0.3)

    return all_results[:max_count]


def convert_to_attraction(poi):
    """
    转换为系统数据格式
    """
    location = poi.get("location", {})

    return {
        "id": f"ATTR_{poi.get('uid', '')}",
        "name": poi.get("name", ""),
        "type": poi.get("tag", "景点") or "景点",
        "campus_id": "",
        "x": location.get("lng", 0),
        "y": location.get("lat", 0),
        "heat": poi.get("热度", 100) or 100,
        "rating": 4.0,
        "tags": [poi.get("tag", "")] if poi.get("tag") else [],
        "description": poi.get("address", ""),
        "image_url": ""
    }


def crawl_beijing():
    """
    爬取北京景点数据
    """
    print("=" * 50)
    print("开始爬取北京景点数据...")
    print("=" * 50)

    all_attractions = []
    seen_ids = set()

    for keyword in SEARCH_KEYWORDS:
        print(f"\n正在爬取: {keyword}")
        pois = crawl_poi_by_keyword(keyword, max_count=50)

        for poi in pois:
            uid = poi.get("uid", "")
            if uid and uid not in seen_ids:
                seen_ids.add(uid)
                attraction = convert_to_attraction(poi)
                all_attractions.append(attraction)

        time.sleep(0.5)

    print(f"\n总共爬取到 {len(all_attractions)} 个景点")

    return all_attractions


def save_to_file(attractions, filename="attractions_beijing.json"):
    """
    保存数据
    """
    import os
    data_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(data_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({"attractions": attractions}, f, ensure_ascii=False, indent=2)

    print(f"数据已保存到: {filepath}")


# ==================== 测试函数 ====================

def test_connection():
    """
    测试AK是否有效
    """
    print("测试百度地图API连接...")

    url = "https://api.map.baidu.com/place/v2/search"
    params = {
        "query": "天安门",
        "region": "北京",
        "output": "json",
        "ak": BAIDU_AK
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get("status") == 0:
            print("✓ API连接成功！")
            if data.get("results"):
                print(f"  测试结果: {data['results'][0].get('name')}")
            return True
        else:
            print(f"✗ API返回错误: {data.get('message', '未知错误')}")
            return False

    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False


# ==================== 主程序 ====================

if __name__ == "__main__":

    if BAIDU_AK == "你的AK":
        print("""
错误：请先修改脚本中的 BAIDU_AK

步骤：
1. 打开 https://lbsyun.baidu.com/
2. 注册/登录
3. 控制台 → 创建应用 → 类型选"浏览器端"
4. 复制AK到脚本第8行
        """)
    else:
        print("""
====================================================
百度地图POI数据爬虫
====================================================
        """)

        # 测试连接
        if test_connection():
            # 爬取数据
            attractions = crawl_beijing()

            # 保存
            if attractions:
                save_to_file(attractions)
                print("\n完成！")
