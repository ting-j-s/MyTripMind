# 功能完善计划 (Feature Completion Plan)

## 概述

本计划基于 Step 3 功能验收追踪矩阵，列出当前最需要完善的功能缺口，按优先级排序。

---

## 一、P1 优先级任务

### 任务 1: 混合交通工具路线

**任务名称**: 支持多段不同交通方式的混合路线规划

**目标**: 用户可以选择多种交通工具（如步行+自行车），系统自动分段计算最优路径

**状态**: ✅ 已完成

**涉及文件**:
- `backend/algorithms/dijkstra.py` - 新增 `shortest_path_mixed_transport()` 函数
- `backend/routes/route.py` - 扩展 `/api/route/shortest` 支持 `transport=mixed_transport`

**涉及 API**:
- `POST /api/route/shortest` (扩展)

**算法设计**:
- 使用 MinHeap 选择前 K 大元素，每条边枚举 allowed_modes 中可用的交通工具
- 时间 = distance / (ideal_speed × congestion)
- 对每条边选择使总时间最短的交通工具

**验收方式**:
1. 调用 API 时传入 `transport: 'mixed_transport'`，`modes: ['walk', 'bike', 'shuttle']`
2. 返回的 path 中不同路段使用不同 speed 计算时间
3. 返回 segments 包含每段的 mode、distance、time、congestion
4. 返回 modes_used 列出实际使用的交通方式
5. 验证总时间 = sum(segment_time)

**风险**: 低 - 已完成

---

### 任务 2: 日记个人兴趣推荐增强

**任务名称**: 基于标签的日记个人兴趣推荐

**目标**: 用户设置兴趣标签（如"历史"、"博物馆"），系统推荐包含匹配标签的日记

**状态**: ✅ 已完成

**涉及文件**:
- `backend/models/user.py` - interests 字段已存在
- `backend/models/diary.py` - 现有字段
- `backend/routes/diary.py` - 扩展 `get_diaries()` 支持 sort=interest

**涉及 API**:
- `GET /api/diaries?sort=interest&user_id=xxx` - 基于兴趣评分推荐

**评分公式**:
```
score = 0.45 * interest_match + 0.25 * rating_norm + 0.20 * heat_norm + 0.10 * content_match
- interest_match = matched_tags_count / user_interests_count (0 到 1)
- rating_norm = avg_rating / 5.0
- heat_norm = view_count / max_view_count
- content_match = content_hits / user_interests_count
```

**Top-K 合规**: 使用 `sort.py:top_k` 实现，时间复杂度 O(n log k)

**需要新增/修改的测试**:
- `tests/test_diary_interest_recommendation.py` - 13 个测试用例

**验收方式**:
1. 用户有 interests = ["历史", "校园"]
2. 日记 title/content 包含这些词
3. 推荐结果优先显示匹配日记（高 interest_match/content_match）
4. 返回结果包含 score, interest_match, content_match, match_reasons

**风险**: 低 - 已完成

---

### 任务 3: 景点个人兴趣推荐增强

**任务名称**: 基于标签的景点个人兴趣推荐

**目标**: 与任务 2 类似，但针对景点推荐，基于用户兴趣标签匹配景点类别

**状态**: ✅ 已完成

**涉及文件**:
- `backend/models/attraction.py` - tags 字段已存在
- `backend/routes/attractions.py` - 扩展 `recommend()` 支持 strategy=interest

**涉及 API**:
- `GET /api/recommend?user_id=xxx&strategy=interest` - 基于兴趣评分推荐

**评分公式**:
```
score = 0.45 * interest_match + 0.30 * rating_norm + 0.25 * heat_norm
- interest_match = matched_tags / user_interests_count (0 到 1)
- rating_norm = rating / 5.0
- heat_norm = heat / max_heat
```

**Top-K 合规**: 使用 `sort.py:top_k` 实现，时间复杂度 O(n log k)

**需要新增/修改的测试**:
- `tests/test_attraction_interest_recommendation.py` - 12 个测试用例

**验收方式**:
1. 用户有 interests = ["历史", "校园"]
2. 景点有 tags = ["历史", "博物馆"]
3. 推荐结果优先显示匹配景点（高 interest_match）
4. 返回结果包含 score, interest_match, match_reasons

**风险**: 低 - 已完成

---

## 二、P2 优先级任务

### 任务 4: 前端动态交互

**任务名称**: 将静态 HTML 页面改为动态数据渲染

**目标**: 前端页面能从 API 动态加载数据并实时更新 UI

**涉及文件**:
- `frontend/pages/home.html` - 改为动态加载景点列表
- `frontend/pages/diary_square.html` - 改为动态加载日记列表
- `frontend/js/app.js` - 新增统一的数据请求和渲染逻辑

**涉及 API**:
- 所有现有 GET API

**需要新增/修改的测试**:
- 无需修改后端测试
- 前端测试使用 Selenium 或 Playwright（可选）

**验收方式**:
1. 打开 home.html 能自动加载景点列表
2. 点击筛选条件时页面刷新数据而非重新加载
3. 日记列表支持下拉加载更多

**风险**: 高 - 前端工作量较大，但不影响后端验收

---

### 任务 5: 数据变化后索引自动重建

**任务名称**: 索引脏标记自动触发重建

**目标**: 当 diary 数据变化时，搜索索引能自动重建而不需要手动调用

**涉及文件**:
- `backend/routes/diary.py` - 在 `create_diary/update_diary/delete_diary` 时自动重建
- `backend/algorithms/text_search.py` - 添加自动重建方法

**涉及 API**:
- `POST /api/diary` - 自动触发搜索索引重建
- `PUT /api/diary/<id>` - 自动触发标题索引和搜索索引重建
- `DELETE /api/diary/<id>` - 自动触发索引重建

**需要新增/修改的测试**:
- `tests/test_diary.py` - 新增 `test_index_auto_rebuild_after_create` 测试用例

**验收方式**:
1. 创建新日记后立即搜索，能找到新日记
2. 更新日记标题后，精确搜索能找到更新后的标题

**风险**: 低 - 已有脏标记机制，只需添加自动调用

---

## 三、任务开发顺序

建议按以下顺序开发：

1. **任务 3 (景点兴趣推荐)** - 最简单，先热身
2. **任务 2 (日记兴趣推荐)** - 类似逻辑，巩固理解
3. **任务 5 (索引自动重建)** - 改进代码质量
4. **任务 1 (混合交通工具)** - 功能性较强，放在后面

前端动态交互任务建议最后处理，或根据实际需要决定是否开发。

---

## 四、不需要开发的内容

以下内容课程要求已满足，无需额外开发：

1. **Dijkstra 算法** - 已完整实现，使用 MinHeap 优化
2. **TSP 算法** - 已实现贪心+2-opt，返回起点
3. **Top-K 排序** - 已使用堆实现，非全量排序
4. **倒排索引** - 已实现 TextSearchIndex
5. **哈希表** - 已实现 HashTable 用于标题精确查询
6. **霍夫曼压缩** - 已实现，支持压缩/解压无损还原
7. **道路网络距离** - 附近设施和美食都使用 Dijkstra 计算
8. **数据规模** - 所有数据文件均满足 >=200 景点, >=200 道路边等要求

---

**最后更新**: 2026-05-04
**优先级排序**: P1 > P2
**建议**: 先完成 P1 任务再考虑 P2