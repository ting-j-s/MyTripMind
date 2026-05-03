"""
获取非核心景点到核心景点的路径
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error

AK = "5abeba63f349bf35b48bde5551efea34"
BASE_URL = "https://restapi.amap.com/v3/direction/driving"

# 39个核心景点
CORE_ATTRACTIONS = [
    'ATTR_BJ_001', 'ATTR_BJ_002', 'ATTR_BJ_003', 'ATTR_BJ_004', 'ATTR_BJ_005',
    'ATTR_BJ_006', 'ATTR_BJ_007', 'ATTR_BJ_008', 'ATTR_BJ_009', 'ATTR_BJ_017',
    'ATTR_BJ_018', 'ATTR_BJ_019', 'ATTR_BJ_020', 'ATTR_BJ_021', 'ATTR_BJ_022',
    'ATTR_BJ_023', 'ATTR_BJ_024', 'ATTR_BJ_025', 'ATTR_BJ_026', 'ATTR_BJ_027',
    'ATTR_BJ_028', 'ATTR_BJ_029', 'ATTR_BJ_030', 'ATTR_BJ_031', 'ATTR_BJ_032',
    'ATTR_BJ_033', 'ATTR_BJ_034', 'ATTR_BJ_037', 'ATTR_BJ_038', 'ATTR_BJ_039',
    'ATTR_BJ_040', 'ATTR_BJ_041', 'ATTR_BJ_042', 'ATTR_BJ_044', 'ATTR_BJ_045',
    'ATTR_BJ_048', 'ATTR_BJ_049', 'ATTR_BJ_055', 'ATTR_BJ_057',
]

def load_attractions():
    """加载所有景点坐标"""
    with open('backend/data/attractions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    coords = {}
    for a in data['attractions']:
        coords[a['id']] = {
            'name': a['name'],
            'x': a['x'],
            'y': a['y']
        }
    return coords

def get_distance(from_id, to_id, coords):
    """获取两点间驾车距离"""
    if from_id not in coords or to_id not in coords:
        return None

    from_coord = coords[from_id]
    to_coord = coords[to_id]

    origin = f"{from_coord['x']},{from_coord['y']}"
    destination = f"{to_coord['x']},{to_coord['y']}"

    url = f"{BASE_URL}?origin={origin}&destination={destination}&key={AK}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))

        if data['status'] == '1' and data['info'] == 'OK':
            route = data['route']
            if 'paths' in route and len(route['paths']) > 0:
                distance = int(route['paths'][0]['distance'])
                return distance
    except Exception as e:
        pass

    return None

def main():
    print("开始获取非核心景点到核心景点的路径...")
    print(f"核心景点数: {len(CORE_ATTRACTIONS)}")

    coords = load_attractions()

    # 找出非核心景点
    periphery = [aid for aid in coords.keys() if aid not in CORE_ATTRACTIONS]
    print(f"非核心景点数: {len(periphery)}")

    # 计算总任务数
    total = len(periphery) * len(CORE_ATTRACTIONS) * 2  # 双向
    print(f"预计获取: {total} 条路径")

    paths = []
    total_one_way = len(periphery) * len(CORE_ATTRACTIONS)
    count = 0
    success = 0
    failed = 0

    start_time = time.time()

    # 遍历所有非核心景点
    for p_id in periphery:
        for c_id in CORE_ATTRACTIONS:
            count += 1

            # 获取正向
            dist1 = get_distance(p_id, c_id, coords)
            if dist1 is not None:
                paths.append({'from_id': p_id, 'to_id': c_id, 'distance': dist1})
                success += 1
            else:
                failed += 1

            # 获取反向
            dist2 = get_distance(c_id, p_id, coords)
            if dist2 is not None:
                paths.append({'from_id': c_id, 'to_id': p_id, 'distance': dist2})
                success += 1
            else:
                failed += 1

            # 进度
            if count % 100 == 0:
                elapsed = time.time() - start_time
                rate = count / elapsed if elapsed > 0 else 0
                remaining = (total_one_way - count) / rate if rate > 0 else 0
                print(f"进度: {count}/{total_one_way} ({count*100/total_one_way:.1f}%) 成功:{success} 失败:{failed*2} 剩余:{remaining/60:.1f}分钟")

            time.sleep(0.08)  # 稍微快点

    print(f"\n获取完成!")
    print(f"总计: {count} 条")
    print(f"成功: {success} 条")
    print(f"失败: {failed * 2} 条")

    # 保存
    result = {'paths': paths}
    with open('backend/data/periphery_to_core_paths.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"已保存到: backend/data/periphery_to_core_paths.json")

if __name__ == "__main__":
    main()