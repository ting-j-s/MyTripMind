# 需求追踪矩阵 (Requirement Traceability Matrix)

## 1. 课程要求概述

本项目为北京邮电大学数据结构课程设计，要求实现以下功能模块：

| 章节 | 要求 | 对应模块 |
|------|------|---------|
| 3.1 | 旅游景区介绍及推荐 | attractions.py (景点列表/搜索/推荐) |
| 3.2 | 最短路径规划（Dijkstra） | route.py (室外路径/室内导航) |
| 3.3 | 场所查询（附近设施） | nearby.py (基于道路网络的附近查询) |
| 3.4 | 旅游日记分享 | diary.py (CRUD/搜索/评分/压缩) |
| 3.5 | 美食推荐 | food.py (列表/搜索/推荐) |
| 3.6 | 地图显示 | frontend/pages/route_planning.html (Leaflet地图) |

---

## 2. 功能模块详细追踪矩阵

### 2.1 旅游景区介绍及推荐 (3.1)

| 编号 | 课程要求 | 当前状态 | 对应代码 | 对应 API | 对应测试 | 前端演示 | 是否满足 | 缺口说明 | 优先级 |
|------|---------|---------|---------|---------|---------|---------|---------|---------|--------|
| 3.1.1 | 用户选择景点/学校作为目的地 | 已完成 | attractions.py:get_attractions, get_campuses | GET /api/attractions, GET /api/campuses | test_api_full_requirements.py | home.html | 是 | 无 | - |
| 3.1.2 | 按热度推荐 | 已完成 | attractions.py:recommend_attractions | GET /api/recommend | test_api_full_requirements.py | home.html | 是 | 无 | - |
| 3.1.3 | 按评价推荐 | 已完成 | attractions.py:recommend_attractions | GET /api/recommend?sort=rating | test_api_full_requirements.py | home.html | 是 | 无 | - |
| 3.1.4 | 按个人兴趣推荐 | 已完成 | attractions.py:recommend() strategy=interest | GET /api/recommend?user_id=xxx&strategy=interest | test_attraction_interest_recommendation.py | 无 | 是 | 使用 0.45*兴趣匹配+0.30*评分+0.25*热度 综合评分，Top-K 选取 | - |
| 3.1.5 | 名称查询 | 已完成 | attractions.py:search_attractions + fuzzy_search | GET /api/attractions/search?q=xxx | test_api_full_requirements.py | home.html | 是 | 无 | - |
| 3.1.6 | 类别查询 | 已完成 | attractions.py:get_attractions?type=xxx | GET /api/attractions?type=xxx | test_api_full_requirements.py | home.html | 是 | 无 | - |
| 3.1.7 | 关键字查询 | 已完成 | attractions.py:search_attractions | GET /api/attractions/search?q=xxx | test_api_full_requirements.py | home.html | 是 | 无 | - |
| 3.1.8 | 查询结果按热度排序 | 已完成 | attractions.py (sort=heat) | GET /api/attractions?sort=heat | test_api_full_requirements.py | home.html | 是 | 无 | - |
| 3.1.9 | 查询结果按评价排序 | 已完成 | attractions.py (sort=rating) | GET /api/attractions?sort=rating | test_api_full_requirements.py | home.html | 是 | 无 | - |
| 3.1.10 | 前10推荐使用Top-K | 已完成 | sort.py:top_k, attractions.py | top_k(diaries, limit, key=..., reverse=True) | test_api_full_requirements.py | home.html | 是 | 无 | - |
| 3.1.11 | 数据动态变化后推荐结果更新 | 已完成 | diary.py:mark_search_index_dirty() | index dirty flag 机制 | test_api_full_requirements.py | 无 | 部分 | 索引有脏标记机制，但需重新请求才会更新 | P2 |

---

### 2.2 旅游路线规划 (3.2)

| 编号 | 课程要求 | 当前状态 | 对应代码 | 对应 API | 对应测试 | 前端演示 | 是否满足 | 缺口说明 | 优先级 |
|------|---------|---------|---------|---------|---------|---------|---------|---------|--------|
| 3.2.1 | 单目标最短路径 | 已完成 | dijkstra.py:dijkstra, route.py:shortest_path | POST /api/route/shortest | test_api_full_requirements.py | route_planning.html | 是 | 无 | - |
| 3.2.2 | 多目标路径 | 已完成 | tsp.py:solve_tsp, route.py:tsp_route | POST /api/route/tsp | test_api_full_requirements.py | route_planning.html | 是 | 无 | - |
| 3.2.3 | 多目标路径返回起点 | 已完成 | tsp.py:solve_tsp 返回 path 含起点和终点 | path = [起点, A, B, C, 起点] | test_api_full_requirements.py | route_planning.html | 是 | 无 | - |
| 3.2.4 | 最短距离策略 | 已完成 | dijkstra.py:dijkstra(weight='distance') | weight=distance | test_api_full_requirements.py | route_planning.html | 是 | 无 | - |
| 3.2.5 | 最短时间策略 | 已完成 | dijkstra.py:dijkstra(weight='time') | weight=time | test_api_full_requirements.py | route_planning.html | 是 | 无 | - |
| 3.2.6 | 拥挤度参与时间计算 | 已完成 | dijkstra.py:edge_weight = distance / (ideal_speed * congestion) | congestion in edge data | test_api_full_requirements.py | route_planning.html | 是 | 无 | - |
| 3.2.7 | 交通工具最短时间策略 | 已完成 | dijkstra.py:dijkstra_with_constraints | transport=步行/自行车/电瓶车 | test_api_full_requirements.py | route_planning.html | 是 | 无 | - |
| 3.2.8 | 校区步行/自行车 | 已完成 | dijkstra_with_constraints road_types 限制 | road_types=['步行', '自行车'] | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.2.9 | 景区步行/电瓶车 | 已完成 | dijkstra_with_constraints road_types 限制 | road_types=['步行', '电瓶车'] | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.2.10 | 自行车只能走自行车道路 | 已完成 | dijkstra_with_constraints 过滤 road_types | transport='自行车' checks road_types | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.2.11 | 电瓶车只能走固定路线 | 已完成 | dijkstra_with_constraints 过滤 road_types | transport='电瓶车' checks road_types | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.2.12 | 混合交通工具 | 已完成 | shortest_path_mixed_transport | transport='mixed_transport' | test_mixed_transport_route.py | 无 | 是 | 已实现多段不同交通工具混合，每段记录实际使用的 mode | - |
| 3.2.13 | 地图展示 | 已完成 | route_planning.html Leaflet | - | 无专门测试 | route_planning.html | 是 | 无 | - |
| 3.2.14 | 路径展示 | 已完成 | route_planning.html path_coords 显示 | path_coords in API response | test_api_full_requirements.py | route_planning.html | 是 | 无 | - |
| 3.2.15 | 室内导航：大门到电梯 | 已完成 | indoor_navigation_service.py:plan_indoor_route | POST /api/route/indoor | test_indoor_route.py | 无 | 是 | 无 | - |
| 3.2.16 | 室内导航：楼层间电梯 | 已完成 | indoor_navigation_service.py 分层图 | elevator edges in indoor graph | test_indoor_route.py | 无 | 是 | 无 | - |
| 3.2.17 | 室内导航：楼层内到房间 | 已完成 | indoor_navigation_service.py 分层图 | elevator/room edges in indoor graph | test_indoor_route.py | 无 | 是 | 无 | - |

---

### 2.3 场所查询 (3.3)

| 编号 | 课程要求 | 当前状态 | 对应代码 | 对应 API | 对应测试 | 前端演示 | 是否满足 | 缺口说明 | 优先级 |
|------|---------|---------|---------|---------|---------|---------|---------|---------|--------|
| 3.3.1 | 选中地点后查询附近设施 | 已完成 | nearby.py:get_nearby | GET /api/nearby | test_api_full_requirements.py | route_planning.html | 是 | 无 | - |
| 3.3.2 | 超市、卫生间等设施 | 已完成 | facilities.json 包含多类型 | GET /api/facilities | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.3.3 | 类别过滤 | 已完成 | nearby.py:get_nearby?type=xxx | ?type= | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.3.4 | 输入类别名称查询 | 已完成 | nearby.py:search_facilities + fuzzy_search | GET /api/facilities/search?q=xxx | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.3.5 | 按距离排序 | 已完成 | nearby.py:calc_road_distance 使用 dijkstra | sort by distance | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.3.6 | 距离使用道路网络实际距离 | 已完成 | nearby.py:calculate_road_distance(graph, from, to) 调用 dijkstra | Dijkstra道路距离 | test_api_full_requirements.py | 无 | 是 | 无 | - |

---

### 2.4 旅游日记管理 (3.4)

| 编号 | 课程要求 | 当前状态 | 对应代码 | 对应 API | 对应测试 | 前端演示 | 是否满足 | 缺口说明 | 优先级 |
|------|---------|---------|---------|---------|---------|---------|---------|---------|--------|
| 3.4.1 | 创建日记 | 已完成 | diary.py:create_diary | POST /api/diary | test_api_full_requirements.py | diary_write.html | 是 | 无 | - |
| 3.4.2 | 文字 | 已完成 | diary.py:create_diary content 字段 | content 字段 | test_api_full_requirements.py | diary_write.html | 是 | 无 | - |
| 3.4.3 | 图片 | 已完成 | diary.py:create_diary images 字段 | images 字段 | test_api_full_requirements.py | diary_write.html | 是 | 无 | - |
| 3.4.4 | 视频 | 已完成 | diary.py:create_diary videos 字段 | videos 字段 | test_api_full_requirements.py | diary_write.html | 是 | 无 | - |
| 3.4.5 | 所有用户日记统一管理 | 已完成 | loader.get_all_diaries() | GET /api/diaries | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |
| 3.4.6 | 浏览所有日记 | 已完成 | diary.py:get_diaries | GET /api/diaries | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |
| 3.4.7 | 查询所有日记 | 已完成 | diary.py:get_diaries 支持筛选 | ?location_id= | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |
| 3.4.8 | 浏览量作为热度 | 已完成 | diary.py:increment_view, view_count | view_count 字段 | test_api_full_requirements.py | diary_detail.html | 是 | 无 | - |
| 3.4.9 | 用户评分 | 已完成 | diary.py:rate_diary, add_rating | POST /api/diary/<id>/rate | test_api_full_requirements.py | diary_detail.html | 是 | 无 | - |
| 3.4.10 | 按热度推荐 | 已完成 | diary.py:get_diaries sort=heat | GET /api/diaries?sort=heat | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |
| 3.4.11 | 按评价推荐 | 已完成 | diary.py:get_diaries sort=rating | GET /api/diaries?sort=rating | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |
| 3.4.12 | 按个人兴趣推荐 | 已完成 | diary.py:get_diaries sort=interest | GET /api/diaries?sort=interest&user_id=xxx | test_diary_interest_recommendation.py | 无 | 是 | 使用 0.45*兴趣匹配+0.25*评分+0.20*热度+0.10*内容匹配 综合评分，Top-K 选取 | - |
| 3.4.13 | 前10推荐使用Top-K | 已完成 | sort.py:top_k | top_k(diaries, limit, ...) | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |

---

### 2.5 旅游日记交流 (3.5)

| 编号 | 课程要求 | 当前状态 | 对应代码 | 对应 API | 对应测试 | 前端演示 | 是否满足 | 缺口说明 | 优先级 |
|------|---------|---------|---------|---------|---------|---------|---------|---------|--------|
| 3.5.1 | 输入目的地查询相关日记 | 已完成 | diary.py:get_diaries?location_id=xxx | GET /api/diaries?location_id=xxx | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |
| 3.5.2 | 相关日记按热度排序 | 已完成 | diary.py:get_diaries sort=heat | GET /api/diaries?sort=heat | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |
| 3.5.3 | 相关日记按评分排序 | 已完成 | diary.py:get_diaries sort=rating | GET /api/diaries?sort=rating | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |
| 3.5.4 | 日记名称精确查询 | 已完成 | diary.py:search_by_title 使用 HashTable | GET /api/diaries/title?title=xxx | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.5.5 | 日记内容全文检索 | 已完成 | diary.py:search_diaries 使用 TextSearchIndex | GET /api/diaries/search?q=xxx | test_api_full_requirements.py | diary_square.html | 是 | 无 | - |
| 3.5.6 | 日记压缩存储 | 已完成 | diary.py:compress_diary 使用 HuffmanCoding | POST /api/diary/<id>/compress | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.5.7 | 日记无损解压 | 已完成 | diary.py:decompress_diary | POST /api/diary/<id>/decompress | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.5.8 | AIGC旅游动画生成 | 已完成 | aigc.py:generate_animation, aigc_service.py | POST /api/aigc/animation | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.5.9 | AIGC本地fallback | 已完成 | aigc_service.py:generate_mock_animation | 无外部API时使用模拟 | test_api_full_requirements.py | 无 | 是 | 无 | - |

---

### 2.6 美食推荐 (3.6)

| 编号 | 课程要求 | 当前状态 | 对应代码 | 对应 API | 对应测试 | 前端演示 | 是否满足 | 缺口说明 | 优先级 |
|------|---------|---------|---------|---------|---------|---------|---------|---------|--------|
| 3.6.1 | 选中景点/学校后推荐美食 | 已完成 | food.py:recommend_foods 支持 campus_id 筛选 | GET /api/foods/recommend?campus_id=xxx | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.2 | 按热度排序 | 已完成 | food.py:get_foods sort=heat | GET /api/foods?sort=heat | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.3 | 按评价排序 | 已完成 | food.py:get_foods sort=rating | GET /api/foods?sort=rating | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.4 | 按道路距离排序 | 已完成 | food.py:calculate_road_distance 使用 dijkstra | GET /api/foods?sort=distance | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.5 | 按菜系过滤 | 已完成 | food.py:get_foods?cuisine=xxx | GET /api/foods?cuisine=xxx | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.6 | 美食名称模糊查询 | 已完成 | food.py:search_foods + fuzzy_search | GET /api/foods/search?q=xxx | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.7 | 菜系模糊查询 | 已完成 | food.py:search_foods + fuzzy_search | q=菜系名 | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.8 | 饭店名称模糊查询 | 已完成 | food.py:search_foods fuzzy_search fields=['name', 'cuisine', 'restaurant'] | q=饭店名 | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.6.9 | 窗口名称模糊查询 | 已完成 | food.py:search_foods fuzzy_search fields=['name', 'cuisine', 'restaurant'] | q=窗口名 | test_api_full_requirements.py | 无 | 是 | 无 | - |
| 3.6.10 | 多结果按热度排序 | 已完成 | food.py:top_k(datas, limit, key=heat) | top_k | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.11 | 多结果按评价排序 | 已完成 | food.py:top_k(datas, limit, key=rating) | top_k | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.12 | 多结果按距离排序 | 已完成 | food.py:sort by distance | sort=distance | test_api_full_requirements.py | food.html | 是 | 无 | - |
| 3.6.13 | 前10美食使用Top-K | 已完成 | sort.py:top_k, food.py | top_k(foods, limit, ...) | test_api_full_requirements.py | food.html | 是 | 无 | - |

---

### 2.7 数据规模 (3.7)

| 编号 | 课程要求 | 当前状态 | 对应代码 | 数据文件 | 实际数量 | 对应测试 | 是否达标 | 缺口说明 | 优先级 |
|------|---------|---------|---------|---------|---------|---------|---------|---------|--------|
| 3.7.1 | 景区和校园数量 >= 200 | 已完成 | loader.get_all_attractions() | attractions.json | 205 | test_data_scale.py | 是 | 无 | - |
| 3.7.2 | 建筑物数量 >= 20 | 已完成 | loader.get_all_buildings() | buildings.json | 20 | test_data_scale.py | 是 | 无 | - |
| 3.7.3 | 服务设施种类 >= 10 | 已完成 | Facility.FACILITY_TYPES | backend/models/facility.py | 10 | test_api_full_requirements.py | 是 | 无 | - |
| 3.7.4 | 服务设施数量 >= 50 | 已完成 | loader.get_all_facilities() | facilities.json | 50 | test_data_scale.py | 是 | 无 | - |
| 3.7.5 | 道路边数 >= 200 | 已完成 | roads.json edges | roads.json | 51317 | test_road_network.py | 是 | 无 | - |
| 3.7.6 | 系统用户数 >= 10 | 已完成 | loader.get_all_users() | users.json | 11 | test_data_scale.py | 是 | 无 | - |

---

### 2.8 前端演示

| 编号 | 页面 | 当前状态 | 文件 | 缺口说明 | 优先级 |
|------|-----|---------|------|---------|--------|
| 3.8.1 | home.html | 部分完成 | frontend/pages/home.html | 静态页面，部分API已对接 | P2 |
| 3.8.2 | route_planning.html | 部分完成 | frontend/pages/route_planning.html | Leaflet地图+路径展示 | - |
| 3.8.3 | attraction_detail.html | 部分完成 | frontend/pages/attraction_detail.html | 静态页面 | P2 |
| 3.8.4 | food.html | 部分完成 | frontend/pages/food.html | 静态页面 | P2 |
| 3.8.5 | diary_square.html | 部分完成 | frontend/pages/diary_square.html | 静态页面 | P2 |
| 3.8.6 | diary_detail.html | 部分完成 | frontend/pages/diary_detail.html | 静态页面 | P2 |
| 3.8.7 | diary_write.html | 部分完成 | frontend/pages/diary_write.html | 静态页面 | P2 |
| 3.8.8 | trip_planning.html | 部分完成 | frontend/pages/trip_planning.html | 静态页面 | P2 |

---

### 2.9 测试覆盖

| 编号 | 测试文件 | 覆盖内容 | 当前状态 | 缺口说明 | 优先级 |
|------|---------|---------|---------|---------|--------|
| 3.9.1 | test_api_full_requirements.py | 3.1-3.6全部API端点 | 已完成 | 无 | - |
| 3.9.2 | test_road_network.py | 道路网络Dijkstra | 已完成 | 无 | - |
| 3.9.3 | test_indoor_route.py | 室内导航 | 已完成 | 无 | - |
| 3.9.4 | test_nearby.py | 附近设施查询 | 已完成 | 无 | - |
| 3.9.5 | test_food.py | 美食推荐 | 已完成 | 无 | - |
| 3.9.6 | test_data_scale.py | 数据规模 | 已完成 | 无 | - |
| 3.9.7 | test_api_stability.py | API稳定性 | 已完成 | 无 | - |

---

### 2.10 文档覆盖

| 编号 | 文档 | 当前状态 | 缺口说明 | 优先级 |
|------|-----|---------|---------|--------|
| 3.10.1 | README.md | 已完成 | 无 | - |
| 3.10.2 | requirement_traceability_matrix.md | 已完成 | 无 | - |
| 3.10.3 | indoor_navigation_design.md | 已完成 | 无 | - |
| 3.10.4 | road_network_integration.md | 已完成 | 无 | - |
| 3.10.5 | file_cleanup_report.md | 已完成 | 无 | - |
| 3.10.6 | data_scale_report.md | 已完成 | 无 | - |
| 3.10.7 | check_step2_api_stability_report.md | 已完成 | 无 | - |

---

## 3. 算法合规性检查

| 检查项 | 结论 | 证据文件 | 风险 | 建议 |
|--------|------|---------|------|------|
| Top-K 是否有全量排序截断风险 | 无风险 | sort.py:top_k (line 130-194) 使用 MaxHeap 维护前K大，时间复杂度 O(n log k) | 无 | 无需修改 |
| 附近设施距离是否使用道路网络距离 | 是 | nearby.py:calculate_road_distance (line 127-137) 调用 dijkstra(graph, from, to, weight='distance') | 无 | 无需修改 |
| 美食距离是否使用道路网络距离 | 是 | food.py:calculate_road_distance (line 125-134) 调用 dijkstra(graph, from, to, weight='distance') | 无 | 无需修改 |
| 路线规划是否真实使用图算法 | 是 | dijkstra.py:dijkstra 使用 MinHeap，不是简单遍历 | 无 | 无需修改 |
| 多目标路线是否返回起点 | 是 | tsp.py:solve_tsp (line 216-261) 返回 path 含起点和终点 | 无 | 无需修改 |
| 交通工具策略是否限制道路类型 | 是 | dijkstra_with_constraints (line 137-231) 检查 road_types 过滤边 | 无 | 无需修改 |
| 全文检索是否使用倒排索引 | 是 | text_search.py:TextSearchIndex (line 11-202) 倒排索引结构 | 无 | 无需修改 |
| 标题精确查询是否使用哈希表 | 是 | diary.py:build_title_index 使用 HashTable (line 36-68) | 无 | 无需修改 |
| 压缩存储是否无损还原 | 是 | compression.py:HuffmanCoding 完整实现，test_compress_then_decompress_lossless 通过 | 无 | 无需修改 |
| 核心功能是否依赖数据库 | 否 | 使用 JSON 文件存储，backend/data/*.json | 无 | 无需修改 |
| 数据是否真实接入系统 | 是 | loader 从 JSON 文件加载，routes 使用 loader 获取数据 | 无 | 无需修改 |

---

## 4. 当前缺口总结

### P0 优先级（不影响验收主流程）

无 P0 缺口。

### P1 优先级（课程明确要求但已有部分基础）

无 P1 缺口。混合交通工具路线已通过 shortest_path_mixed_transport 完成；日记按个人兴趣推荐已使用 0.45*兴趣+0.25*评分+0.20*热度+0.10*内容 综合评分完成；景点按个人兴趣推荐已使用 0.45*兴趣+0.30*评分+0.25*热度 综合评分完成。

### P2 优先级（完善演示和文档）

| 缺口 | 说明 | 涉及文件 |
|------|------|---------|
| 前端动态交互 | 当前前端为静态 HTML，API 已对接但无动态数据刷新 | frontend/pages/*.html |
| 用户兴趣标签匹配 | 可基于标签/类别做更精准的兴趣推荐 | attractions.py, diary.py |

### P3 优先级（优化项）

| 缺口 | 说明 | 涉及文件 |
|------|------|---------|
| 索引脏标记触发 | 数据变化后索引自动重建需手动触发 | diary.py |
| 搜索结果缓存 | 可添加搜索结果缓存提升性能 | diary.py, attractions.py |

---

**最后更新**: 2026-05-04
**状态**: 全部核心功能已完成，仅有 P1/P2 级别优化空间
**测试结果**: 186 passed