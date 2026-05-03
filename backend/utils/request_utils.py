"""
请求参数解析工具

提供统一的参数解析和校验函数
"""

from flask import request, jsonify


def parse_json_body(required_fields=None, optional_fields=None):
    """
    解析 JSON 请求体

    参数:
        required_fields: 必填字段列表，如 ['username', 'password']
        optional_fields: 可选字段列表

    返回:
        (data, error_response) - data 为解析后的字典，error_response 为错误响应（如果有）
    """
    data = request.get_json(silent=True) or {}

    if required_fields:
        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            return None, jsonify({
                'code': 400,
                'message': f'缺少必填字段: {", ".join(missing)}',
                'data': None
            })

    return data, None


def parse_int_arg(name, default=None, min_value=None, max_value=None):
    """
    安全解析整数参数

    参数:
        name: 参数名
        default: 默认值
        min_value: 最小值
        max_value: 最大值

    返回:
        (value, error_response)
    """
    value = request.args.get(name)

    if value is None:
        if default is not None:
            return default, None
        return None, jsonify({
            'code': 400,
            'message': f'缺少参数: {name}',
            'data': None
        })

    try:
        int_val = int(value)
    except (ValueError, TypeError):
        return None, jsonify({
            'code': 400,
            'message': f'{name}必须是整数，当前值: {value}',
            'data': None
        })

    if min_value is not None and int_val < min_value:
        return None, jsonify({
            'code': 400,
            'message': f'{name}不能小于{min_value}，当前值: {int_val}',
            'data': None
        })

    if max_value is not None and int_val > max_value:
        return None, jsonify({
            'code': 400,
            'message': f'{name}不能大于{max_value}，当前值: {int_val}',
            'data': None
        })

    return int_val, None


def parse_float_arg(name, default=None, min_value=None, max_value=None):
    """
    安全解析浮点数参数

    参数:
        name: 参数名
        default: 默认值
        min_value: 最小值
        max_value: 最大值

    返回:
        (value, error_response)
    """
    value = request.args.get(name)

    if value is None:
        if default is not None:
            return default, None
        return None, jsonify({
            'code': 400,
            'message': f'缺少参数: {name}',
            'data': None
        })

    try:
        float_val = float(value)
    except (ValueError, TypeError):
        return None, jsonify({
            'code': 400,
            'message': f'{name}必须是数字，当前值: {value}',
            'data': None
        })

    if min_value is not None and float_val < min_value:
        return None, jsonify({
            'code': 400,
            'message': f'{name}不能小于{min_value}，当前值: {float_val}',
            'data': None
        })

    if max_value is not None and float_val > max_value:
        return None, jsonify({
            'code': 400,
            'message': f'{name}不能大于{max_value}，当前值: {float_val}',
            'data': None
        })

    return float_val, None


def success_response(data=None, message='success', status=200):
    """返回成功响应"""
    return jsonify({
        'code': 200,
        'data': data,
        'message': message
    }), status


def error_response(message, status=400, data=None):
    """返回错误响应"""
    return jsonify({
        'code': status,
        'message': message,
        'data': data
    }), status
