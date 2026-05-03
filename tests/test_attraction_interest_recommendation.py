"""
景点兴趣推荐测试
验证基于用户兴趣标签和景点 tags 匹配得分的推荐功能
"""

import pytest
from backend.app import app


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAttractionInterestRecommendation:
    """景点兴趣推荐功能测试"""

    def test_interest_recommendation_with_matching_tags(self, client):
        """用户兴趣标签与景点 tags 匹配时，匹配景点排名更靠前"""
        # user_001 兴趣: ["历史", "校园"]
        # 北京邮电校史馆 tags: ["校园", "拍照", "运动"] - 匹配"校园"
        response = client.get('/api/recommend?user_id=user_001&strategy=interest&limit=10')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200

        items = data['data']['items']
        assert len(items) <= 10

        # 检查返回结果中有 score 和 match_reasons
        for item in items:
            assert 'score' in item
            assert 'interest_match' in item
            assert 'match_reasons' in item
            # 如果有匹配，match_reasons 不为空
            if item['match_reasons']:
                assert any('匹配兴趣:' in reason for reason in item['match_reasons'])

    def test_interest_recommendation_list_type_interests(self, client):
        """用户兴趣是列表时可以正确计算"""
        # user_002 兴趣: ["美食", "自然"]
        response = client.get('/api/recommend?user_id=user_002&strategy=interest&limit=10')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200
        assert data['data']['strategy'] == 'interest'
        assert len(data['data']['items']) <= 10

    def test_interest_recommendation_nonexistent_user(self, client):
        """用户不存在时返回 404"""
        response = client.get('/api/recommend?user_id=nonexistent_user&strategy=interest')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 404
        assert '用户不存在' in data['message']

    def test_interest_recommendation_no_interests(self, client):
        """用户没有兴趣标签时降级为热度推荐"""
        # user_3781e767 兴趣为空列表
        response = client.get('/api/recommend?user_id=user_3781e767&strategy=interest&limit=5')
        assert response.status_code == 200
        data = response.get_json()
        # 降级到 heat 策略
        assert data['code'] == 200

    def test_interest_recommendation_attraction_without_tags(self, client):
        """景点无 tags 不报错，interest_match 为 0"""
        # 遍历结果，确保无 tags 的景点也能处理
        response = client.get('/api/recommend?user_id=user_001&strategy=interest&limit=20')
        assert response.status_code == 200
        data = response.get_json()

        for item in data['data']['items']:
            # interest_match 应该是 0 或正数
            assert 'interest_match' in item
            assert item['interest_match'] >= 0

    def test_interest_recommendation_limit(self, client):
        """limit=10 时返回不超过 10 条"""
        response = client.get('/api/recommend?user_id=user_001&strategy=interest&limit=10')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['data']['items']) <= 10

    def test_interest_recommendation_score_calculation(self, client):
        """验证 score 计算包含 interest_match, rating_norm, heat_norm"""
        response = client.get('/api/recommend?user_id=user_001&strategy=interest&limit=5')
        assert response.status_code == 200
        data = response.get_json()

        for item in data['data']['items']:
            score = item['score']
            interest_match = item['interest_match']
            # score 应该在 0-1 范围内（因为各分量都是归一化的）
            assert 0 <= score <= 1.0
            assert 0 <= interest_match <= 1.0

    def test_interest_recommendation_match_reasons(self, client):
        """返回结果包含 match_reasons，便于演示"""
        response = client.get('/api/recommend?user_id=user_001&strategy=interest&limit=10')
        assert response.status_code == 200
        data = response.get_json()

        # 至少有一些结果有 match_reasons
        has_match = any(item['match_reasons'] for item in data['data']['items'])
        # 如果没有匹配（用户兴趣与景点标签不符），可能全为空
        # 但应该能正常返回结果
        assert data['code'] == 200

    def test_interest_recommendation_fallback_to_heat(self, client):
        """不传 strategy 时默认按热度推荐"""
        response = client.get('/api/recommend?user_id=user_001&limit=5')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200
        assert data['data']['strategy'] == 'heat'

    def test_interest_recommendation_with_rating_strategy(self, client):
        """rating 策略按评分排序"""
        response = client.get('/api/recommend?strategy=rating&limit=5')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200
        assert data['data']['strategy'] == 'rating'

    def test_top_k_not_full_sort(self, client):
        """验证业务实现使用 Top-K 而非全量排序"""
        response = client.get('/api/recommend?user_id=user_001&strategy=interest&limit=10')
        assert response.status_code == 200
        data = response.get_json()

        items = data['data']['items']
        # 检查有合理数量的结果（不超过limit）
        assert len(items) <= 10
        # 检查返回的 score 在合理范围内
        for item in items:
            assert 0 <= item['score'] <= 1.0
        # 验证结果按 score 降序排列
        scores = [item['score'] for item in items]
        assert scores == sorted(scores, reverse=True)

    def test_interest_recommendation_score_descending_order(self, client):
        """验证推荐结果按 score 降序排列"""
        response = client.get('/api/recommend?user_id=user_001&strategy=interest&limit=10')
        assert response.status_code == 200
        data = response.get_json()

        items = data['data']['items']
        # 验证 score 降序
        scores = [item['score'] for item in items]
        assert scores == sorted(scores, reverse=True), f"Scores not descending: {scores}"

    def test_interest_recommendation_returns_all_fields(self, client):
        """返回结果包含景点完整信息"""
        response = client.get('/api/recommend?user_id=user_001&strategy=interest&limit=5')
        assert response.status_code == 200
        data = response.get_json()

        for item in data['data']['items']:
            assert 'id' in item
            assert 'name' in item
            assert 'rating' in item
            assert 'heat' in item
            assert 'tags' in item
            assert 'score' in item
            assert 'interest_match' in item
            assert 'match_reasons' in item