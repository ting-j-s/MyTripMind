"""
景点路由 - 景点列表、搜索、推荐
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Blueprint, request, jsonify

from backend.data import get_loader
from backend.core import top_k
from backend.algorithms import fuzzy_search
from backend.utils.request_utils import parse_int_arg

attractions_bp = Blueprint('attractions', __name__)


@attractions_bp.route('/attractions', methods=['GET'])
def get_attractions():
    """
    获取景点列表

    查询参数:
        campus_id: 校园ID（可选）
        sort: 排序方式 heat/rating
        limit: 返回数量（默认10）
        offset: 偏移量（分页用）
    """
    campus_id = request.args.get('campus_id')
    sort_by = request.args.get('sort', 'heat')  # heat 或 rating

    # 安全解析 limit 和 offset
    limit, err = parse_int_arg('limit', default=10, min_value=1, max_value=100)
    if err:
        return err
    offset, err = parse_int_arg('offset', default=0, min_value=0, max_value=10000)
    if err:
        return err

    loader = get_loader()
    attractions = loader.get_all_attractions()

    # 按校园过滤
    if campus_id:
        attractions = [a for a in attractions if a.campus_id == campus_id]

    # 排序
    if sort_by == 'rating':
        attractions = top_k(attractions, limit,
                           key=lambda x: x.rating, reverse=True)
    else:  # 默认按热度
        attractions = top_k(attractions, limit,
                           key=lambda x: x.heat, reverse=True)

    # 分页
    total = len(attractions)
    attractions = attractions[offset:offset + limit]

    return jsonify({
        'code': 200,
        'data': {
            'items': [a.to_dict() for a in attractions],
            'total': total,
            'limit': limit,
            'offset': offset
        },
        'message': 'success'
    })


@attractions_bp.route('/attractions/<attraction_id>', methods=['GET'])
def get_attraction(attraction_id):
    """获取景点详情"""
    loader = get_loader()
    attraction = loader.get_attraction(attraction_id)

    if not attraction:
        return jsonify({'code': 404, 'message': '景点不存在', 'data': None})

    # 增加热度
    attraction.increment_heat()
    loader.save_attractions()

    return jsonify({
        'code': 200,
        'data': attraction.to_dict(),
        'message': 'success'
    })


@attractions_bp.route('/attractions/search', methods=['GET'])
def search_attractions():
    """
    搜索景点

    查询参数:
        q: 搜索关键词
        limit: 返回数量
    """
    query = request.args.get('q', '').strip()

    # 安全解析 limit
    limit, err = parse_int_arg('limit', default=10, min_value=1, max_value=100)
    if err:
        return err

    if not query:
        return jsonify({
            'code': 200,
            'data': {'items': [], 'total': 0},
            'message': 'success'
        })

    loader = get_loader()
    attractions = loader.get_all_attractions()

    # 转换为字典列表
    items = [a.to_dict() for a in attractions]

    # 模糊搜索
    results = fuzzy_search(items, query, fields=['name', 'tags', 'description'], limit=limit)

    return jsonify({
        'code': 200,
        'data': {
            'items': results,
            'total': len(results),
            'query': query
        },
        'message': 'success'
    })


@attractions_bp.route('/recommend', methods=['GET'])
def recommend():
    """
    个性化推荐

    根据用户兴趣推荐景点

    查询参数:
        user_id: 用户ID（可选，不登录则按热度推荐）
        strategy: 推荐策略 heat/rating/interest（默认heat）
        limit: 返回数量（默认10）
    """
    user_id = request.args.get('user_id')
    strategy = request.args.get('strategy', 'heat')
    limit = int(request.args.get('limit', 10))

    # 安全解析 limit
    if limit < 1:
        limit = 10
    if limit > 100:
        limit = 100

    loader = get_loader()
    attractions = loader.get_all_attractions()

    if not attractions:
        return jsonify({
            'code': 200,
            'data': {'items': [], 'total': 0},
            'message': 'success'
        })

    # 计算热度最大值用于归一化
    max_heat = max(a.heat for a in attractions) or 1

    # 如果有用户，按兴趣推荐
    if user_id:
        user = loader.get_user(user_id)
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在', 'data': None})
    else:
        user = None

    if strategy == 'interest' and user and user.interests:
        # 基于兴趣评分的推荐
        scored_attractions = []

        for a in attractions:
            # 计算兴趣匹配得分
            matched_tags = [tag for tag in user.interests if tag in a.tags]
            interest_match = len(matched_tags) / len(user.interests) if user.interests else 0

            # 归一化评分和热度
            rating_norm = a.rating / 5.0 if a.rating else 0
            heat_norm = a.heat / max_heat if max_heat > 0 else 0

            # 综合得分：0.45*兴趣匹配 + 0.30*评分 + 0.25*热度
            score = 0.45 * interest_match + 0.30 * rating_norm + 0.25 * heat_norm

            # 构建匹配原因说明
            match_reasons = []
            for tag in matched_tags:
                match_reasons.append(f"匹配兴趣: {tag}")

            scored_attractions.append({
                'attraction': a,
                'score': score,
                'interest_match': interest_match,
                'rating_norm': rating_norm,
                'heat_norm': heat_norm,
                'match_reasons': match_reasons
            })

        # 使用 Top-K 按 score 排序
        top_results = top_k(scored_attractions, limit,
                            key=lambda x: x['score'], reverse=True)

        items = []
        for result in top_results:
            a = result['attraction']
            item = a.to_dict()
            item['score'] = round(result['score'], 3)
            item['interest_match'] = round(result['interest_match'], 3)
            item['match_reasons'] = result['match_reasons']
            items.append(item)

        return jsonify({
            'code': 200,
            'data': {
                'items': items,
                'total': len(items),
                'strategy': 'interest'
            },
            'message': 'success'
        })

    elif strategy == 'rating':
        # 按评分推荐
        top_attractions = top_k(attractions, limit,
                                key=lambda x: x.rating, reverse=True)
        items = [a.to_dict() for a in top_attractions]
        return jsonify({
            'code': 200,
            'data': {
                'items': items,
                'total': len(items),
                'strategy': 'rating'
            },
            'message': 'success'
        })

    else:
        # 默认按热度推荐
        top_attractions = top_k(attractions, limit,
                                key=lambda x: x.heat, reverse=True)
        items = [a.to_dict() for a in top_attractions]
        return jsonify({
            'code': 200,
            'data': {
                'items': items,
                'total': len(items),
                'strategy': 'heat'
            },
            'message': 'success'
        })


@attractions_bp.route('/campuses', methods=['GET'])
def get_campuses():
    """获取校园列表"""
    loader = get_loader()
    campuses = loader.get_all_campuses()

    return jsonify({
        'code': 200,
        'data': {
            'items': [c.to_dict() for c in campuses],
            'total': len(campuses)
        },
        'message': 'success'
    })
