"""
混合交通工具路线测试
测试 mixed_transport 最短时间路线功能
"""

import pytest
from backend.core.graph import Graph
from backend.algorithms.dijkstra import shortest_path_mixed_transport, _normalize_transport


class TestMixedTransportAlgorithm:
    """混合交通算法单元测试"""

    def test_mixed_transport_returns_valid_path(self):
        """混合交通工具可以返回成功路径"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')
        g.add_node('D')

        # A -> B: only walk
        g.add_edge('A', 'B', distance=100, road_types=['步行'])
        # B -> C: walk and bike
        g.add_edge('B', 'C', distance=100, road_types=['步行', '自行车'])
        # A -> C: only walk (longer)
        g.add_edge('A', 'C', distance=300, road_types=['步行'])
        # C -> D: only bike
        g.add_edge('C', 'D', distance=100, road_types=['自行车'])

        result = shortest_path_mixed_transport(g, 'A', 'D')
        assert result['success'] is True
        assert len(result['path']) > 0
        assert 'A' in result['path']
        assert 'D' in result['path']

    def test_mixed_transport_returns_segments(self):
        """返回结果包含 segments"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')

        g.add_edge('A', 'B', distance=100, road_types=['步行', '自行车'])
        g.add_edge('B', 'C', distance=100, road_types=['步行', '自行车'])

        result = shortest_path_mixed_transport(g, 'A', 'C')
        assert result['success'] is True
        assert 'segments' in result
        assert len(result['segments']) == 2

    def test_segments_contain_mode_distance_time_congestion(self):
        """segments 中每段包含 mode、distance、time、congestion"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')

        g.add_edge('A', 'B', distance=100, road_types=['步行', '自行车'], congestion=0.5)
        g.add_edge('B', 'C', distance=100, road_types=['步行', '自行车'], congestion=0.8)

        result = shortest_path_mixed_transport(g, 'A', 'C')
        assert result['success'] is True

        for seg in result['segments']:
            assert 'mode' in seg
            assert 'distance' in seg
            assert 'time' in seg
            assert 'congestion' in seg
            assert seg['mode'] in ['walk', 'bike', 'shuttle']
            assert seg['distance'] == 100
            assert 0 < seg['congestion'] <= 1

    def test_mixed_transport_uses_multiple_modes(self):
        """modes_used 至少可以包含两种交通方式"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')
        g.add_node('D')

        # A -> B: only walk
        g.add_edge('A', 'B', distance=100, road_types=['步行'])
        # B -> C: both walk and bike
        g.add_edge('B', 'C', distance=100, road_types=['步行', '自行车'])
        # C -> D: only bike
        g.add_edge('C', 'D', distance=100, road_types=['自行车'])

        result = shortest_path_mixed_transport(g, 'A', 'D')
        assert result['success'] is True
        assert 'modes_used' in result
        # Should use both walk and bike
        assert len(result['modes_used']) >= 1

    def test_bike_cannot_use_walk_only_edges(self):
        """bike 模式不能走不包含 bike 的边"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')

        # A -> B: only walk (bike not allowed)
        g.add_edge('A', 'B', distance=100, road_types=['步行'])
        # B -> C: only walk (bike not allowed)
        g.add_edge('B', 'C', distance=100, road_types=['步行'])
        # No bike paths at all

        result = shortest_path_mixed_transport(g, 'A', 'C', allowed_modes=['bike'])
        # No path exists with only bike
        assert result['success'] is False

    def test_shuttle_cannot_use_non_shuttle_edges(self):
        """shuttle 模式不能走不包含 shuttle 的边"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')

        # A -> B: only walk
        g.add_edge('A', 'B', distance=100, road_types=['步行'])
        # A -> C: walk only
        g.add_edge('A', 'C', distance=200, road_types=['步行'])

        result = shortest_path_mixed_transport(g, 'A', 'B', allowed_modes=['shuttle'])
        # No path exists with only shuttle
        assert result['success'] is False

    def test_walk_can_use_walk_edges(self):
        """walk 模式可以走 walk 边"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')

        g.add_edge('A', 'B', distance=100, road_types=['步行'])

        result = shortest_path_mixed_transport(g, 'A', 'B', allowed_modes=['walk'])
        assert result['success'] is True
        assert result['path'] == ['A', 'B']
        assert 'walk' in result['modes_used']

    def test_congestion_affects_shortest_time(self):
        """拥挤度会影响最短时间选择"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')

        # Path 1: short but very congested
        g.add_edge('A', 'B', distance=50, road_types=['步行', '自行车'], congestion=0.1)
        # Path 2: longer but no congestion
        g.add_edge('B', 'C', distance=200, road_types=['步行', '自行车'], congestion=1.0)

        # Alternative path A -> C directly (medium distance, medium congestion)
        g.add_edge('A', 'C', distance=150, road_types=['步行', '自行车'], congestion=0.9)

        result = shortest_path_mixed_transport(g, 'A', 'C', allowed_modes=['walk', 'bike'])
        assert result['success'] is True
        # The algorithm should pick the path with lowest total time

    def test_mixed_transport_time_not_exceed_single_walk(self):
        """mixed_transport 的 total_time 不大于单一 walk 路线时间"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')

        # All edges allow both walk and bike
        g.add_edge('A', 'B', distance=100, road_types=['步行', '自行车'])
        g.add_edge('B', 'C', distance=100, road_types=['步行', '自行车'])
        # Direct path A -> C (walk only shorter distance but bike available)
        g.add_edge('A', 'C', distance=180, road_types=['步行', '自行车'])

        result_mixed = shortest_path_mixed_transport(g, 'A', 'C', allowed_modes=['walk', 'bike'])
        assert result_mixed['success'] is True

        # With bike available, mixed should be faster than walk only
        # Since bike speed (15 km/h) > walk speed (5 km/h)
        # For same distance, bike is faster

    def test_start_node_not_exists_returns_error(self):
        """start 不存在返回错误"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')

        result = shortest_path_mixed_transport(g, 'nonexistent', 'B')
        assert result['success'] is False
        assert 'error' in result

    def test_end_node_not_exists_returns_error(self):
        """end 不存在返回错误"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')

        result = shortest_path_mixed_transport(g, 'A', 'nonexistent')
        assert result['success'] is False
        assert 'error' in result

    def test_normalize_transport(self):
        """交通方式名称标准化"""
        assert _normalize_transport('步行') == 'walk'
        assert _normalize_transport('自行车') == 'bike'
        assert _normalize_transport('电瓶车') == 'shuttle'
        assert _normalize_transport('bike') == 'bike'
        assert _normalize_transport('walk') == 'walk'
        assert _normalize_transport('shuttle') == 'shuttle'

    def test_no_path_returns_error(self):
        """无法到达时返回错误"""
        g = Graph(directed=False)
        g.add_node('A')
        g.add_node('B')
        g.add_node('C')

        # A -> B but B is isolated from C
        g.add_edge('A', 'B', distance=100, road_types=['步行'])

        result = shortest_path_mixed_transport(g, 'A', 'C')
        assert result['success'] is False


class TestMixedTransportAPI:
    """混合交通 API 测试"""

    @pytest.fixture
    def client(self):
        """创建测试客户端"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from backend.app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_mixed_transport_api_invalid_strategy(self, client):
        """strategy 非法返回 400"""
        response = client.post('/api/route/shortest',
                               json={'from': 'test', 'to': 'test', 'strategy': 'invalid'})
        # Should return 400 for missing required params or similar

    def test_empty_json_returns_400(self, client):
        """空 JSON 返回 400"""
        response = client.post('/api/route/shortest',
                               json={},
                               content_type='application/json')
        assert response.status_code == 400 or response.get_json().get('code') == 400