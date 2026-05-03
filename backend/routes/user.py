"""
用户路由 - 个人信息、收藏
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Blueprint, request, jsonify

from backend.data import get_loader

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    获取用户信息

    查询参数:
        user_id: 用户ID
    """
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id不能为空', 'data': None})

    loader = get_loader()
    user = loader.get_user(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None})

    return jsonify({
        'code': 200,
        'data': user.to_dict(),
        'message': 'success'
    })


@user_bp.route('/profile', methods=['PUT'])
def update_profile():
    """
    更新用户信息

    请求:
        {
            "user_id": "用户ID",
            "interests": ["兴趣1", "兴趣2"],
            "username": "新用户名"  // 可选
        }
    """
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id不能为空', 'data': None})

    loader = get_loader()
    user = loader.get_user(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None})

    # 更新字段
    if 'interests' in data:
        user.interests = data['interests']

    if 'username' in data:
        # 检查用户名是否被占用
        existing = loader.get_user_by_username(data['username'])
        if existing and existing.id != user_id:
            return jsonify({'code': 400, 'message': '用户名已被占用', 'data': None})
        user.username = data['username']

    loader.save_users()

    return jsonify({
        'code': 200,
        'message': '更新成功',
        'data': user.to_dict()
    })


@user_bp.route('/favorites', methods=['GET'])
def get_favorites():
    """
    获取用户收藏列表

    查询参数:
        user_id: 用户ID
    """
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id不能为空', 'data': None})

    loader = get_loader()
    user = loader.get_user(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None})

    # 获取收藏的景点详情
    favorites = []
    for attr_id in user.favorites:
        attraction = loader.get_attraction(attr_id)
        if attraction:
            favorites.append(attraction.to_dict())

    return jsonify({
        'code': 200,
        'data': {
            'items': favorites,
            'total': len(favorites)
        },
        'message': 'success'
    })


@user_bp.route('/favorites', methods=['POST'])
def add_favorite():
    """
    添加收藏

    请求:
        {
            "user_id": "用户ID",
            "attraction_id": "景点ID"
        }
    """
    data = request.get_json()
    user_id = data.get('user_id')
    attraction_id = data.get('attraction_id')

    if not user_id or not attraction_id:
        return jsonify({'code': 400, 'message': '参数不完整', 'data': None})

    loader = get_loader()
    user = loader.get_user(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None})

    attraction = loader.get_attraction(attraction_id)
    if not attraction:
        return jsonify({'code': 404, 'message': '景点不存在', 'data': None})

    user.add_favorite(attraction_id)
    loader.save_users()

    return jsonify({
        'code': 200,
        'message': '收藏成功',
        'data': {'favorites_count': len(user.favorites)}
    })


@user_bp.route('/favorites/<attraction_id>', methods=['DELETE'])
def remove_favorite(attraction_id):
    """
    取消收藏

    查询参数:
        user_id: 用户ID
    """
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id不能为空', 'data': None})

    loader = get_loader()
    user = loader.get_user(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None})

    user.remove_favorite(attraction_id)
    loader.save_users()

    return jsonify({
        'code': 200,
        'message': '已取消收藏',
        'data': None
    })


@user_bp.route('/visited', methods=['GET'])
def get_visited():
    """
    获取用户去过的景点

    查询参数:
        user_id: 用户ID
    """
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id不能为空', 'data': None})

    loader = get_loader()
    user = loader.get_user(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None})

    # 获取去过的景点详情
    visited = []
    for attr_id in user.visited:
        attraction = loader.get_attraction(attr_id)
        if attraction:
            visited.append(attraction.to_dict())

    return jsonify({
        'code': 200,
        'data': {
            'items': visited,
            'total': len(visited)
        },
        'message': 'success'
    })


@user_bp.route('/diaries', methods=['GET'])
def get_user_diaries():
    """
    获取用户的日记列表

    查询参数:
        user_id: 用户ID
    """
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id不能为空', 'data': None})

    loader = get_loader()
    user = loader.get_user(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在', 'data': None})

    diaries = loader.get_all_diaries()
    user_diaries = [d for d in diaries if d.user_id == user_id]

    return jsonify({
        'code': 200,
        'data': {
            'items': [d.to_dict() for d in user_diaries],
            'total': len(user_diaries)
        },
        'message': 'success'
    })
