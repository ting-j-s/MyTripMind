"""
场所查询路由 - 附近设施查找
"""

import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from flask import Blueprint, request, jsonify
import math

from backend.data import get_loader
from backend.core import sort_by_distance
from backend.algorithms import fuzzy_search

nearby_bp = Blueprint('nearby', __name__)


def calculate_distance(x1, y1, x2, y2):
    """
    计算两点间距离（米）

    使用简化的平面距离
    实际应用应使用高德/百度地图API的距离计算
    """
    # 经纬度差值（粗略估算）
    lat_diff = abs(y2 - y1) * 111000  # 纬度1度约111km
    lon_diff = abs(x2 - x1) * 111000 * math.cos(math.radians(y1))

    return math.sqrt(lat_diff ** 2 + lon_diff ** 2)


@nearby_bp.route('/nearby', methods=['GET'])
def get_nearby():
    """
    查找附近的设施

    查询参数:
        x: 参考点X坐标
        y: 参考点Y坐标
        range: 范围（米），默认500
        type: 设施类型（可选）
        campus_id: 校区ID
        limit: 返回数量
    """
    x = float(request.args.get('x', 0))
    y = float(request.args.get('y', 0))
    search_range = float(request.args.get('range', 500))
    facility_type = request.args.get('type')
    campus_id = request.args.get('campus_id')
    limit = int(request.args.get('limit', 10))

    loader = get_loader()
    facilities = loader.get_all_facilities()

    # 按校区过滤
    if campus_id:
        facilities = [f for f in facilities if f.campus_id == campus_id]

    # 按类型过滤
    if facility_type:
        facilities = [f for f in facilities if f.type == facility_type]

    # 计算距离并过滤
    nearby_facilities = []
    for f in facilities:
        dist = calculate_distance(x, y, f.x, f.y)
        if dist <= search_range:
            f.distance = dist
            nearby_facilities.append(f)

    # 按距离排序（转换为字典）
    nearby_items = [f.to_dict() for f in nearby_facilities]
    nearby_items = sorted(nearby_items, key=lambda f: f.get('distance', float('inf')))

    return jsonify({
        'code': 200,
        'data': {
            'items': nearby_items[:limit],
            'total': len(nearby_items),
            'reference': {'x': x, 'y': y, 'range': search_range}
        },
        'message': 'success'
    })


@nearby_bp.route('/facilities', methods=['GET'])
def get_facilities():
    """
    获取设施列表

    查询参数:
        campus_id: 校区ID
        type: 设施类型
    """
    campus_id = request.args.get('campus_id')
    facility_type = request.args.get('type')

    loader = get_loader()
    facilities = loader.get_all_facilities()

    # 按校区过滤
    if campus_id:
        facilities = [f for f in facilities if f.campus_id == campus_id]

    # 按类型过滤
    if facility_type:
        facilities = [f for f in facilities if f.type == facility_type]

    return jsonify({
        'code': 200,
        'data': {
            'items': [f.to_dict() for f in facilities],
            'total': len(facilities),
            'types': loader.get_facilities_by_type(facility_type) if facility_type else []
        },
        'message': 'success'
    })


@nearby_bp.route('/facilities/search', methods=['GET'])
def search_facilities():
    """
    搜索设施

    查询参数:
        q: 搜索关键词
        campus_id: 校区ID
        limit: 返回数量
    """
    query = request.args.get('q', '').strip()
    campus_id = request.args.get('campus_id')
    limit = int(request.args.get('limit', 10))

    if not query:
        return jsonify({
            'code': 200,
            'data': {'items': [], 'total': 0},
            'message': 'success'
        })

    loader = get_loader()
    facilities = loader.get_all_facilities()

    # 按校区过滤
    if campus_id:
        facilities = [f for f in facilities if f.campus_id == campus_id]

    # 转换为字典
    items = [f.to_dict() for f in facilities]

    # 模糊搜索
    results = fuzzy_search(items, query, fields=['name', 'type'], limit=limit)

    return jsonify({
        'code': 200,
        'data': {
            'items': results,
            'total': len(results),
            'query': query
        },
        'message': 'success'
    })


@nearby_bp.route('/facility-types', methods=['GET'])
def get_facility_types():
    """获取所有设施类型"""
    from backend.models.facility import Facility
    return jsonify({
        'code': 200,
        'data': {
            'types': Facility.FACILITY_TYPES
        },
        'message': 'success'
    })
