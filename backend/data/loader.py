"""
数据加载模块
统一管理所有数据的加载和初始化
"""

from typing import List, Dict, Optional
from backend.core import Graph, HashTable

# 模型
from backend.models.user import User
from backend.models.attraction import Attraction, Campus
from backend.models.building import Building
from backend.models.facility import Facility
from backend.models.road import Road
from backend.models.diary import Diary
from backend.models.food import Food

# 存储
from .storage import get_storage


class DataLoader:
    """
    数据加载器

    功能：
    - 加载各类数据（景点、用户、日记等）
    - 提供数据查询接口
    - 管理内存中的数据缓存
    """

    def __init__(self):
        self.storage = get_storage()

        # 数据缓存
        self._users = {}
        self._attractions = {}
        self._campuses = {}
        self._buildings = {}
        self._facilities = {}
        self._roads = []
        self._diaries = {}
        self._foods = {}

        # 图结构缓存
        self._graphs = {}

        # 加载所有数据
        self.load_all()

    def load_all(self):
        """加载所有数据"""
        self.load_users()
        self.load_attractions()
        self.load_buildings()
        self.load_facilities()
        self.load_roads()
        self.load_diaries()
        self.load_foods()
        # 注意：暂时不加载北邮详细数据，避免污染全局路网
        # 如果需要使用北邮校内导航，单独处理
        # self.load_bupt_data()

    def load_bupt_data(self):
        """加载北邮沙河校区详细数据"""
        import os

        data_dir = os.path.dirname(os.path.abspath(__file__))

        # 加载北邮建筑数据
        bupt_buildings_file = os.path.join(data_dir, 'bupt_buildings.json')
        if os.path.exists(bupt_buildings_file):
            data = self.storage.load('bupt_buildings.json', {'buildings': []})
            for item in data.get('buildings', []):
                building = Building.from_dict(item)
                if building:
                    self._buildings[building.id] = building

        # 加载北邮设施数据
        bupt_facilities_file = os.path.join(data_dir, 'bupt_facilities.json')
        if os.path.exists(bupt_facilities_file):
            data = self.storage.load('bupt_facilities.json', {'facilities': []})
            for item in data.get('facilities', []):
                facility = Facility.from_dict(item)
                if facility:
                    self._facilities[facility.id] = facility

        # 加载北邮道路数据
        bupt_roads_file = os.path.join(data_dir, 'bupt_roads.json')
        if os.path.exists(bupt_roads_file):
            data = self.storage.load('bupt_roads.json', {'roads': []})
            for item in data.get('roads', []):
                road = Road.from_dict(item)
                if road:
                    self._roads.append(road)

        # 加载北邮景点数据（校园、建筑物等）
        bupt_attractions_file = os.path.join(data_dir, 'bupt_attractions.json')
        if os.path.exists(bupt_attractions_file):
            data = self.storage.load('bupt_attractions.json', {'attractions': []})
            for item in data.get('attractions', []):
                if item.get('type') == '校园':
                    campus = Campus.from_dict(item)
                    if campus:
                        self._campuses[campus.id] = campus
                else:
                    attraction = Attraction.from_dict(item)
                    if attraction:
                        self._attractions[attraction.id] = attraction

    # ==================== 用户 ====================

    def load_users(self):
        """加载用户数据"""
        data = self.storage.load('users.json', {'users': []})
        self._users = {}
        for item in data.get('users', []):
            user = User.from_dict(item)
            if user:
                self._users[user.id] = user

    def save_users(self):
        """保存用户数据"""
        data = {'users': [u.to_dict() for u in self._users.values()]}
        self.storage.save('users.json', data)

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def get_user_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def add_user(self, user: User):
        self._users[user.id] = user
        self.save_users()

    # ==================== 景点 ====================

    def load_attractions(self):
        """加载景点数据"""
        data = self.storage.load('attractions.json', {'attractions': []})
        self._attractions = {}
        self._campuses = {}

        for item in data.get('attractions', []):
            # 跳过北邮相关数据，避免污染全局路网
            if item.get('campus_id') == 'BUPT' or item.get('id', '').startswith('BUPT_'):
                continue

            if item.get('type') in ['景区', '校园']:
                campus = Campus.from_dict(item)
                if campus:
                    self._campuses[campus.id] = campus
            else:
                attraction = Attraction.from_dict(item)
                if attraction:
                    self._attractions[attraction.id] = attraction

    def save_attractions(self):
        """保存景点数据"""
        all_items = []
        all_items.extend([c.to_dict() for c in self._campuses.values()])
        all_items.extend([a.to_dict() for a in self._attractions.values()])
        data = {'attractions': all_items}
        self.storage.save('attractions.json', data)

    def get_attraction(self, attraction_id: str) -> Optional[Attraction]:
        return self._attractions.get(attraction_id)

    def get_all_attractions(self) -> List[Attraction]:
        return list(self._attractions.values())

    def get_campus(self, campus_id: str) -> Optional[Campus]:
        return self._campuses.get(campus_id)

    def get_all_campuses(self) -> List[Campus]:
        return list(self._campuses.values())

    # ==================== 建筑 ====================

    def load_buildings(self):
        """加载建筑数据"""
        data = self.storage.load('buildings.json', {'buildings': []})
        self._buildings = {}
        for item in data.get('buildings', []):
            building = Building.from_dict(item)
            if building:
                self._buildings[building.id] = building

    def save_buildings(self):
        """保存建筑数据"""
        data = {'buildings': [b.to_dict() for b in self._buildings.values()]}
        self.storage.save('buildings.json', data)

    def get_building(self, building_id: str) -> Optional[Building]:
        return self._buildings.get(building_id)

    def get_all_buildings(self) -> List[Building]:
        return list(self._buildings.values())

    def get_buildings_by_campus(self, campus_id: str) -> List[Building]:
        return [b for b in self._buildings.values() if b.campus_id == campus_id]

    # ==================== 设施 ====================

    def load_facilities(self):
        """加载设施数据"""
        data = self.storage.load('facilities.json', {'facilities': []})
        self._facilities = {}
        for item in data.get('facilities', []):
            facility = Facility.from_dict(item)
            if facility:
                self._facilities[facility.id] = facility

    def save_facilities(self):
        """保存设施数据"""
        data = {'facilities': [f.to_dict() for f in self._facilities.values()]}
        self.storage.save('facilities.json', data)

    def get_facility(self, facility_id: str) -> Optional[Facility]:
        return self._facilities.get(facility_id)

    def get_all_facilities(self) -> List[Facility]:
        return list(self._facilities.values())

    def get_facilities_by_campus(self, campus_id: str) -> List[Facility]:
        return [f for f in self._facilities.values() if f.campus_id == campus_id]

    def get_facilities_by_type(self, facility_type: str) -> List[Facility]:
        return [f for f in self._facilities.values() if f.type == facility_type]

    # ==================== 道路 ====================

    def load_roads(self):
        """加载道路数据"""
        data = self.storage.load('roads.json', {'roads': []})
        self._roads = []
        for item in data.get('roads', []):
            road = Road.from_dict(item)
            if road:
                self._roads.append(road)

    def save_roads(self):
        """保存道路数据"""
        data = {'roads': [r.to_dict() for r in self._roads]}
        self.storage.save('roads.json', data)

    def get_all_roads(self) -> List[Road]:
        return self._roads

    def get_roads_by_campus(self, campus_id: str) -> List[Road]:
        # 通过起点/终点节点的campus_id判断
        campus_nodes = set()
        for b in self._buildings.values():
            if b.campus_id == campus_id:
                campus_nodes.add(b.id)
        return [r for r in self._roads if r.from_node in campus_nodes or r.to_node in campus_nodes]

    # ==================== 日记 ====================

    def load_diaries(self):
        """加载日记数据"""
        data = self.storage.load('diaries.json', {'diaries': []})
        self._diaries = {}
        for item in data.get('diaries', []):
            diary = Diary.from_dict(item)
            if diary:
                self._diaries[diary.id] = diary

    def save_diaries(self):
        """保存日记数据"""
        data = {'diaries': [d.to_dict() for d in self._diaries.values()]}
        self.storage.save('diaries.json', data)

    def get_diary(self, diary_id: str) -> Optional[Diary]:
        return self._diaries.get(diary_id)

    def get_all_diaries(self) -> List[Diary]:
        return list(self._diaries.values())

    def add_diary(self, diary: Diary):
        self._diaries[diary.id] = diary
        self.save_diaries()

    def delete_diary(self, diary_id: str):
        if diary_id in self._diaries:
            del self._diaries[diary_id]
            self.save_diaries()

    # ==================== 美食 ====================

    def load_foods(self):
        """加载美食数据"""
        data = self.storage.load('foods.json', {'foods': []})
        self._foods = {}
        for item in data.get('foods', []):
            food = Food.from_dict(item)
            if food:
                self._foods[food.id] = food

    def save_foods(self):
        """保存美食数据"""
        data = {'foods': [f.to_dict() for f in self._foods.values()]}
        self.storage.save('foods.json', data)

    def get_food(self, food_id: str) -> Optional[Food]:
        return self._foods.get(food_id)

    def get_all_foods(self) -> List[Food]:
        return list(self._foods.values())

    def get_foods_by_campus(self, campus_id: str) -> List[Food]:
        return [f for f in self._foods.values() if f.campus_id == campus_id]

    # ==================== 图结构 ====================

    def get_graph(self, campus_id: str = None) -> Graph:
        """
        获取图结构（道路网络）

        如果指定campus_id，只包含该校区的节点
        """
        cache_key = campus_id or 'global'

        if cache_key in self._graphs:
            return self._graphs[cache_key]

        graph = Graph(directed=False)

        # 添加所有建筑作为节点
        for building in self._buildings.values():
            if campus_id and building.campus_id != campus_id:
                continue
            graph.add_node(building.id, building.to_dict())

        # 添加所有设施作为节点
        for facility in self._facilities.values():
            if campus_id and facility.campus_id != campus_id:
                continue
            node_id = f"FAC_{facility.id}"
            graph.add_node(node_id, facility.to_dict())

        # 添加所有道路
        for road in self._roads:
            if campus_id:
                # 简单检查：道路两端节点是否在campus内
                from_node = road.from_node
                to_node = road.to_node
                if not (from_node.startswith(campus_id) or to_node.startswith(campus_id)):
                    continue

            graph.add_edge(
                road.from_node,
                road.to_node,
                distance=road.distance,
                ideal_speed=road.ideal_speed,
                congestion=road.congestion,
                road_types=road.road_types
            )

        self._graphs[cache_key] = graph
        return graph

    # ==================== 统计 ====================

    def get_stats(self) -> Dict:
        """获取数据统计"""
        return {
            'users': len(self._users),
            'attractions': len(self._attractions),
            'campuses': len(self._campuses),
            'buildings': len(self._buildings),
            'facilities': len(self._facilities),
            'roads': len(self._roads),
            'diaries': len(self._diaries),
            'foods': len(self._foods),
        }


# 全局数据加载器实例
_loader = None


def get_loader() -> DataLoader:
    """获取全局数据加载器实例"""
    global _loader
    if _loader is None:
        _loader = DataLoader()
    return _loader
