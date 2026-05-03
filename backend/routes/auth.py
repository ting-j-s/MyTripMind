"""
认证路由 - 注册、登录
"""

import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import uuid
from flask import Blueprint, request, jsonify, session
from datetime import datetime

from backend.data import get_loader
from backend.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    用户注册

    请求:
        {
            "username": "用户名",
            "password": "密码",
            "interests": ["历史", "美食"]  // 可选
        }

    返回:
        {
            "code": 200,
            "message": "注册成功",
            "data": {"user_id": "xxx"}
        }
    """
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')
    interests = data.get('interests', [])

    # 验证
    if not username or len(username) < 2:
        return jsonify({'code': 400, 'message': '用户名至少2个字符', 'data': None})

    if not password or len(password) < 6:
        return jsonify({'code': 400, 'message': '密码至少6位', 'data': None})

    loader = get_loader()

    # 检查用户名是否已存在
    if loader.get_user_by_username(username):
        return jsonify({'code': 400, 'message': '用户名已存在', 'data': None})

    # 创建用户
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    user = User(
        id=user_id,
        username=username,
        password=password,
        interests=interests,
        create_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    loader.add_user(user)

    return jsonify({
        'code': 200,
        'message': '注册成功',
        'data': {'user_id': user_id}
    })


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    用户登录

    请求:
        {
            "username": "用户名",
            "password": "密码"
        }

    返回:
        {
            "code": 200,
            "message": "登录成功",
            "data": {
                "user_id": "xxx",
                "username": "用户名",
                "token": "xxx"  // 简单模拟token
            }
        }
    """
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空', 'data': None})

    loader = get_loader()
    user = loader.get_user_by_username(username)

    if not user:
        return jsonify({'code': 401, 'message': '用户不存在', 'data': None})

    if not user.check_password(password):
        return jsonify({'code': 401, 'message': '密码错误', 'data': None})

    # 生成简单token（实际应用应使用JWT等）
    token = f"token_{uuid.uuid4().hex}"

    return jsonify({
        'code': 200,
        'message': '登录成功',
        'data': {
            'user_id': user.id,
            'username': user.username,
            'token': token
        }
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """退出登录"""
    return jsonify({
        'code': 200,
        'message': '退出成功',
        'data': None
    })
