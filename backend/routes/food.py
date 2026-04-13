"""
美食路由 - 美食列表、搜索、推荐
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Blueprint, request, jsonify

from backend.data import get_loader
from backend.core import top_k
from backend.algorithms import fuzzy_search

food_bp = Blueprint('food', __name__)


@food_bp.route('/foods', methods=['GET'])
def get_foods():
    """
    获取美食列表

    查询参数:
        campus_id: 校区ID
        cuisine: 菜系
        sort: 排序方式 heat/rating/distance
        limit: 返回数量
        offset: 偏移量
    """
    campus_id = request.args.get('campus_id')
    cuisine = request.args.get('cuisine')
    sort_by = request.args.get('sort', 'heat')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    loader = get_loader()
    foods = loader.get_all_foods()

    # 按校区过滤
    if campus_id:
        foods = [f for f in foods if f.campus_id == campus_id]

    # 按菜系过滤
    if cuisine:
        foods = [f for f in foods if f.cuisine == cuisine]

    # 排序
    if sort_by == 'rating':
        foods = top_k(foods, len(foods), key=lambda x: x.rating, reverse=True)
    elif sort_by == 'distance' and campus_id:
        # 按距离排序需要参考点，这里简化处理
        foods = sorted(foods, key=lambda x: x.distance if hasattr(x, 'distance') else float('inf'))
    else:  # 默认按热度
        foods = top_k(foods, len(foods), key=lambda x: x.heat, reverse=True)

    total = len(foods)
    foods = foods[offset:offset + limit]

    return jsonify({
        'code': 200,
        'data': {
            'items': [f.to_dict() for f in foods],
            'total': total,
            'limit': limit,
            'offset': offset
        },
        'message': 'success'
    })


@food_bp.route('/foods/search', methods=['GET'])
def search_foods():
    """
    搜索美食

    查询参数:
        q: 搜索关键词
        campus_id: 校区ID
        cuisine: 菜系过滤
        limit: 返回数量
    """
    query = request.args.get('q', '').strip()
    campus_id = request.args.get('campus_id')
    cuisine = request.args.get('cuisine')
    limit = int(request.args.get('limit', 10))

    loader = get_loader()
    foods = loader.get_all_foods()

    # 按校区过滤
    if campus_id:
        foods = [f for f in foods if f.campus_id == campus_id]

    # 按菜系过滤
    if cuisine:
        foods = [f for f in foods if f.cuisine == cuisine]

    # 转换为字典
    items = [f.to_dict() for f in foods]

    if not query:
        # 无搜索词，返回按热度排序的结果
        items = top_k(items, len(items), key=lambda x: x.get('heat', 0), reverse=True)
        return jsonify({
            'code': 200,
            'data': {
                'items': items[:limit],
                'total': len(items),
                'query': ''
            },
            'message': 'success'
        })

    # 模糊搜索
    results = fuzzy_search(items, query, fields=['name', 'cuisine', 'restaurant'], limit=limit)

    return jsonify({
        'code': 200,
        'data': {
            'items': results,
            'total': len(results),
            'query': query
        },
        'message': 'success'
    })


@food_bp.route('/foods/recommend', methods=['GET'])
def recommend_foods():
    """
    美食推荐

    查询参数:
        campus_id: 校区ID
        user_id: 用户ID（可选）
        limit: 返回数量
    """
    campus_id = request.args.get('campus_id')
    user_id = request.args.get('user_id')
    limit = int(request.args.get('limit', 10))

    loader = get_loader()
    foods = loader.get_all_foods()

    # 按校区过滤
    if campus_id:
        foods = [f for f in foods if f.campus_id == campus_id]

    # 如果有用户，根据用户之前喜欢的菜系推荐
    if user_id:
        user = loader.get_user(user_id)
        if user and user.interests:
            # 简单实现：用户兴趣作为菜系推荐
            recommended = []
            others = []
            for f in foods:
                if f.cuisine in user.interests:
                    recommended.append(f)
                else:
                    others.append(f)

            # 推荐排前面，按热度排序
            recommended = top_k(recommended, len(recommended), key=lambda x: x.heat, reverse=True)
            others = top_k(others, len(others), key=lambda x: x.heat, reverse=True)

            foods = recommended + others
        else:
            foods = top_k(foods, len(foods), key=lambda x: x.heat, reverse=True)
    else:
        foods = top_k(foods, len(foods), key=lambda x: x.heat, reverse=True)

    return jsonify({
        'code': 200,
        'data': {
            'items': [f.to_dict() for f in foods[:limit]],
            'total': len(foods[:limit])
        },
        'message': 'success'
    })


@food_bp.route('/cuisines', methods=['GET'])
def get_cuisines():
    """获取所有菜系"""
    from backend.models.food import Food
    return jsonify({
        'code': 200,
        'data': {
            'cuisines': Food.CUISINES
        },
        'message': 'success'
    })
