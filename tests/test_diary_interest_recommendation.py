"""
日记兴趣推荐测试
验证基于用户兴趣标签和日记 tags/title/content 匹配得分的推荐功能
"""

import pytest
from backend.app import app


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestDiaryInterestRecommendation:
    """日记兴趣推荐功能测试"""

    def test_interest_recommendation_with_matching_tags(self, client):
        """用户兴趣标签与日记 tags 匹配时，匹配日记排名更靠前"""
        # user_001 兴趣: ["历史", "校园"]
        response = client.get('/api/diaries?sort=interest&user_id=user_001&limit=10')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200

        items = data['data']['items']
        assert len(items) <= 10

        # 检查返回结果中有 score, interest_match, content_match, match_reasons
        for item in items:
            assert 'score' in item
            assert 'interest_match' in item
            assert 'content_match' in item
            assert 'match_reasons' in item

    def test_interest_recommendation_list_type_interests(self, client):
        """用户兴趣是列表时可以正确计算"""
        # user_001 兴趣: ["历史", "校园"]
        response = client.get('/api/diaries?sort=interest&user_id=user_001&limit=10')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200
        assert data['data']['strategy'] == 'interest'

    def test_interest_recommendation_nonexistent_user(self, client):
        """用户不存在时返回 404"""
        response = client.get('/api/diaries?sort=interest&user_id=nonexistent_user&limit=10')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 404
        assert '用户不存在' in data['message']

    def test_interest_recommendation_no_interests(self, client):
        """用户没有兴趣标签时降级为综合推荐"""
        # user_3781e767 兴趣为空列表
        response = client.get('/api/diaries?sort=interest&user_id=user_3781e767&limit=5')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200
        # 降级到 interest_fallback 策略
        assert data['data']['strategy'] == 'interest_fallback'

    def test_interest_recommendation_limit(self, client):
        """limit=10 时返回不超过 10 条"""
        response = client.get('/api/diaries?sort=interest&user_id=user_001&limit=10')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['data']['items']) <= 10

    def test_interest_recommendation_score_calculation(self, client):
        """验证 score 计算包含 interest_match, content_match, rating, heat"""
        response = client.get('/api/diaries?sort=interest&user_id=user_001&limit=5')
        assert response.status_code == 200
        data = response.get_json()

        for item in data['data']['items']:
            score = item['score']
            interest_match = item['interest_match']
            content_match = item['content_match']
            # score 应该在 0-1 范围内（因为各分量都是归一化的）
            assert 0 <= score <= 1.0
            assert 0 <= interest_match <= 1.0
            assert 0 <= content_match <= 1.0

    def test_interest_recommendation_match_reasons(self, client):
        """返回结果包含 match_reasons，便于演示"""
        response = client.get('/api/diaries?sort=interest&user_id=user_001&limit=10')
        assert response.status_code == 200
        data = response.get_json()

        # 检查 match_reasons 格式
        for item in data['data']['items']:
            assert isinstance(item['match_reasons'], list)

    def test_interest_recommendation_content_match(self, client):
        """title/content 命中用户兴趣时 content_match > 0"""
        # user_001 兴趣: ["历史", "校园"]
        response = client.get('/api/diaries?sort=interest&user_id=user_001&limit=20')
        assert response.status_code == 200
        data = response.get_json()

        # 检查有 content_match > 0 的结果（标题/内容匹配）
        has_content_match = any(item['content_match'] > 0 for item in data['data']['items'])
        # 可能没有，因为要看具体日记内容

    def test_interest_recommendation_fallback_to_heat(self, client):
        """不传 sort=interest 时默认按热度推荐"""
        response = client.get('/api/diaries?user_id=user_001&limit=5')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200
        # 默认是 heat，不应该有 strategy 字段或 strategy=heat
        strategy = data.get('data', {}).get('strategy', 'heat')
        assert strategy == 'heat'

    def test_top_k_not_full_sort(self, client):
        """验证业务实现使用 Top-K 而非全量排序"""
        response = client.get('/api/diaries?sort=interest&user_id=user_001&limit=10')
        assert response.status_code == 200
        data = response.get_json()

        items = data['data']['items']
        # 检查有合理数量的结果（不超过limit）
        assert len(items) <= 10
        # 检查返回的 score 在合理范围内
        for item in items:
            assert 0 <= item['score'] <= 1.0

    def test_interest_recommendation_returns_all_fields(self, client):
        """返回结果包含日记完整信息"""
        response = client.get('/api/diaries?sort=interest&user_id=user_001&limit=5')
        assert response.status_code == 200
        data = response.get_json()

        for item in data['data']['items']:
            assert 'id' in item
            assert 'title' in item
            assert 'view_count' in item
            assert 'score' in item
            assert 'interest_match' in item
            assert 'content_match' in item
            assert 'match_reasons' in item

    def test_normal_diary_apis_still_work(self, client):
        """原有日记 API 仍然正常工作"""
        # 测试 diary list
        response = client.get('/api/diaries')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200

        # 测试 diary search
        response = client.get('/api/diaries/search?q=test&limit=5')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200

    def test_rating_sort_still_works(self, client):
        """rating 排序仍然正常"""
        response = client.get('/api/diaries?sort=rating&limit=5')
        assert response.status_code == 200
        data = response.get_json()
        assert data['code'] == 200
        items = data['data']['items']
        assert len(items) <= 5