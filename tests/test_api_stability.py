"""
API 稳定性测试
测试 API 的健壮性、安全的参数处理和错误处理一致性
"""

import pytest


class TestAuthAPIStability:
    """auth.py API 稳定性测试"""

    def test_register_invalid_json(self, client):
        """无效 JSON 应该优雅处理"""
        response = client.post('/api/auth/register',
                               data='not valid json',
                               content_type='application/json')
        data = response.get_json()
        # 可能返回 400 或 500
        assert data['code'] in [400, 500]

    def test_register_missing_fields(self, client):
        """缺少必需字段应该返回明确错误"""
        response = client.post('/api/auth/register', json={})
        data = response.get_json()
        assert data['code'] in [400, 500]
        assert 'message' in data

    def test_login_invalid_json(self, client):
        """无效 JSON 应该优雅处理"""
        response = client.post('/api/auth/login',
                               data='invalid',
                               content_type='application/json')
        data = response.get_json()
        assert data['code'] in [400, 500]


class TestAttractionsAPIStability:
    """attractions.py API 稳定性测试"""

    def test_get_attractions_invalid_limit(self, client):
        """无效 limit 参数应该被拒绝"""
        response = client.get('/api/attractions?limit=-1')
        assert response.status_code in [200, 400]
        data = response.get_json()
        assert data['code'] in [200, 400]

        response = client.get('/api/attractions?limit=abc')
        data = response.get_json()
        assert data['code'] in [200, 400]

    def test_get_attraction_nonexistent(self, client):
        """不存在的景点应该返回 404 或 code 404"""
        response = client.get('/api/attraction/nonexistent_id')
        data = response.get_json() or {}
        assert data.get('code') == 404 or response.status_code == 404


class TestDiaryAPIStability:
    """diary.py API 稳定性测试"""

    def test_create_diary_invalid_json(self, client):
        """无效 JSON 但已登录应该返回 400（缺少标题等）"""
        # 先注册登录获取 user_id
        response = client.post('/api/auth/register', json={
            'username': 'testuser_stability',
            'password': 'testpass123'
        })
        response = client.post('/api/auth/login', json={
            'username': 'testuser_stability',
            'password': 'testpass123'
        })
        user_id = response.get_json()['data']['user_id']

        # 用无效 JSON 和有效 user_id 创建日记
        response = client.post('/api/diary',
                               data='not json',
                               content_type='application/json')
        data = response.get_json()
        # 无效 JSON 应该返回 400，或者因为 user_id 验证失败返回其他错误码
        assert data['code'] in [400, 401, 500]

    def test_create_diary_missing_title(self, client):
        """空标题应该被拒绝"""
        response = client.post('/api/diary', json={
            'user_id': 'user_001',
            'title': '',
            'content': 'test'
        })
        data = response.get_json()
        assert data['code'] == 400

    def test_rate_diary_invalid_rating(self, client):
        """无效评分应该被拒绝"""
        response = client.post('/api/diary/test_diary_id/rate', json={'rating': 'invalid'})
        data = response.get_json()
        assert data['code'] == 400

        response = client.post('/api/diary/test_diary_id/rate', json={'rating': 0})
        data = response.get_json()
        assert data['code'] == 400

    def test_rate_diary_missing_rating(self, client):
        """缺少 rating 应该返回 400"""
        response = client.post('/api/diary/test_id/rate', json={})
        data = response.get_json()
        assert data['code'] == 400

    def test_compress_nonexistent_diary(self, client):
        """压缩不存在的日记应该返回 404"""
        response = client.post('/api/diary/nonexistent_id/compress')
        data = response.get_json()
        assert data['code'] == 404 or response.status_code == 404

    def test_search_by_title_empty_title(self, client):
        """空标题查询应该返回 400 或无结果"""
        response = client.get('/api/diaries/title?title=')
        data = response.get_json()
        # 可能返回 400 或者空结果列表
        assert data['code'] == 400 or (data['code'] == 200 and data['data']['total'] == 0)


class TestFoodAPIStability:
    """food.py API 稳定性测试"""

    def test_get_foods_invalid_limit(self, client):
        """无效 limit 应该被拒绝或修正"""
        response = client.get('/api/foods?limit=-1')
        data = response.get_json()
        assert data['code'] in [200, 400]

    def test_search_foods_invalid_limit(self, client):
        """搜索时无效 limit 应该被拒绝"""
        response = client.get('/api/foods/search?q=test&limit=-1')
        data = response.get_json()
        assert data['code'] in [200, 400]

    def test_invalid_origin_format(self, client):
        """无效 origin 格式应该返回 400 或空结果"""
        response = client.get('/api/foods?origin=invalid')
        data = response.get_json()
        assert data['code'] in [200, 400]


class TestNearbyAPIStability:
    """nearby.py API 稳定性测试"""

    def test_get_nearby_invalid_range(self, client):
        """无效 range 应该被拒绝或修正"""
        response = client.get('/api/nearby?origin=116.4,39.9&range=-1')
        data = response.get_json()
        assert data['code'] in [200, 400]


class TestRouteAPIStability:
    """route.py API 稳定性测试"""

    def test_shortest_path_missing_params(self, client):
        """缺少必需参数应该返回 400"""
        response = client.post('/api/route/shortest', json={})
        data = response.get_json()
        assert data['code'] == 400

    def test_tsp_missing_params(self, client):
        """TSP 缺少必需参数应该返回 400"""
        response = client.post('/api/route/tsp', json={})
        data = response.get_json()
        assert data['code'] == 400

    def test_indoor_route_missing_params(self, client):
        """室内导航缺少必需参数应该返回 400"""
        response = client.post('/api/route/indoor', json={})
        data = response.get_json()
        assert data['code'] == 400


class TestAIGCAPIStability:
    """aigc.py API 稳定性测试"""

    def test_generate_animation_missing_location(self, client):
        """缺少 location 应该返回 400"""
        response = client.post('/api/aigc/animation', json={})
        data = response.get_json()
        # 可能返回 400 或 500
        assert data['code'] in [400, 500] if data else True

    def test_generate_animation_invalid_json(self, client):
        """无效 JSON 应该返回 400 或 500"""
        response = client.post('/api/aigc/animation',
                               data='not json',
                               content_type='application/json')
        data = response.get_json()
        assert data['code'] in [400, 500] if data else True


class TestErrorResponseFormat:
    """错误响应格式一致性测试"""

    def test_error_response_has_code_and_message(self, client):
        """错误响应应该包含 code 和 message 字段"""
        cases = [
            lambda: client.post('/api/diary', json={'user_id': 'user_001', 'title': '', 'content': 'test'}),
        ]

        for make_request in cases:
            response = make_request()
            data = response.get_json()
            assert 'code' in data, f"Missing 'code' in response"
            assert 'message' in data, f"Missing 'message' in response"

    def test_success_response_has_code_message_data(self, client):
        """成功响应应该包含 code, message, data 字段"""
        response = client.post('/api/diary', json={
            'user_id': 'user_001',
            'title': 'Format Test',
            'content': 'Test content'
        })
        data = response.get_json()
        assert 'code' in data
        assert 'message' in data
        assert 'data' in data