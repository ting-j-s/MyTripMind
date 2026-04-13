"""
AIGC路由 - AI动画生成
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flask import Blueprint, request, jsonify

from backend.services import get_aigc_service, generate_mock_animation

aigc_bp = Blueprint('aigc', __name__)


@aigc_bp.route('/animation', methods=['POST'])
def generate_animation():
    """
    生成旅游动画描述

    请求:
        {
            "location": "景点名称",
            "images": ["图片URL列表"],
            "description": "用户描述"
        }

    返回:
        {
            "code": 200,
            "data": {
                "description": "生成的动画描述",
                "mock": true/false
            }
        }
    """
    data = request.get_json()
    location = data.get('location', '')
    images = data.get('images', [])
    user_description = data.get('description', '')

    if not location:
        return jsonify({'code': 400, 'message': '景点名称不能为空', 'data': None})

    # 尝试使用真实的AIGC服务
    aigc_service = get_aigc_service()

    if aigc_service.available:
        result = aigc_service.generate_animation_description(
            location=location,
            images=images,
            user_description=user_description
        )
    else:
        # 使用模拟版本
        result = generate_mock_animation(
            location=location,
            images=images,
            user_description=user_description
        )

    if result['success']:
        return jsonify({
            'code': 200,
            'data': {
                'description': result['description'],
                'mock': result.get('mock', False)
            },
            'message': 'success'
        })
    else:
        return jsonify({
            'code': 500,
            'data': None,
            'message': result.get('error', '生成失败')
        })
