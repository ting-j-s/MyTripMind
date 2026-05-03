# 景点兴趣推荐算法设计

## 1. 概述

景点兴趣推荐功能根据用户的兴趣标签与景点的标签进行匹配，结合评分和热度，计算综合得分进行推荐。

## 2. 数据结构

### 输入

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | string | 用户ID |
| strategy | string | 推荐策略: heat/rating/interest |
| limit | int | 返回数量，默认10 |

### 用户数据结构 (User)

```python
class User:
    id: str
    username: str
    interests: List[str]  # 兴趣标签列表，如 ["历史", "校园"]
    favorites: List[str]
    visited: List[str]
```

### 景点数据结构 (Attraction)

```python
class Attraction:
    id: str
    name: str
    type: str  # 景区/校园
    tags: List[str]  # 标签列表，如 ["安静", "健身", "文化"]
    heat: int  # 热度
    rating: float  # 评分 1-5
```

## 3. 评分公式

### 兴趣匹配得分

```
interest_match = matched_tags_count / user_interests_count
```

- 如果用户无兴趣标签：interest_match = 0
- 如果景点无 tags：interest_match = 0
- 范围：0 到 1

### 归一化评分

```
rating_norm = rating / 5.0
heat_norm = heat / max_heat
```

### 综合得分

```
score = 0.45 * interest_match + 0.30 * rating_norm + 0.25 * heat_norm
```

权重分配：
- 兴趣匹配权重 45%（最重要）
- 评分权重 30%
- 热度权重 25%

## 4. Top-K 流程

```
1. 获取所有景点列表
2. 计算 max_heat 用于热度归一化
3. 对每个景点计算:
   - matched_tags = [t for t in user.interests if t in attraction.tags]
   - interest_match = len(matched_tags) / len(user.interests)
   - rating_norm = attraction.rating / 5.0
   - heat_norm = attraction.heat / max_heat
   - score = 0.45 * interest_match + 0.30 * rating_norm + 0.25 * heat_norm
4. 使用 top_k(scored_attractions, limit, key=lambda x: x['score'], reverse=True)
5. 构建返回结果，包含 score, interest_match, match_reasons
```

## 5. 时间复杂度和空间复杂度

| 指标 | 值 |
|------|------|
| 时间复杂度 | O(n log k)，n=景点数量，k=limit |
| 空间复杂度 | O(n)，存储所有景点的评分数据 |
| 适用场景 | n很大（数千到数万），k很小（10-100） |

## 6. 返回格式

```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": "ATTR_CAMPUS001_001",
        "name": "北京邮电图书馆",
        "rating": 4.8,
        "heat": 1234,
        "tags": ["安静", "健身", "文化"],
        "score": 0.87,
        "interest_match": 0.333,
        "match_reasons": ["匹配兴趣: 文化"]
      }
    ],
    "total": 10,
    "strategy": "interest"
  },
  "message": "success"
}
```

## 7. 特殊处理

### 用户不存在
- 返回 code 404，message "用户不存在"

### 用户无兴趣标签
- 降级为 strategy=heat，按热度推荐

### 景点无 tags
- interest_match = 0，score 计算正常进行

### 策略参数
| strategy | 行为 |
|----------|------|
| interest | 基于兴趣评分推荐（需要 user_id） |
| rating | 按评分排序推荐 |
| heat（默认） | 按热度排序推荐 |

## 8. Top-K 合规性

- 使用 `backend/core/sort.py:top_k` 实现
- 不是 `sorted(all)[:k]` 或 `list.sort()[:k]`
- 时间复杂度 O(n log k) vs 全量排序 O(n log n)
- heap_sort 已补充边界测试，Top-K 仍使用堆结构

## 9. 动态数据变化处理

当景点数据变化（新增/修改/删除）：
1. 热度变化：实时生效，max_heat 重新计算
2. 评分变化：实时生效
3. tags 变化：实时生效

推荐结果由请求时实时计算，无需缓存失效。

---

## 10. 日记兴趣推荐算法

### 10.1 概述

日记兴趣推荐功能根据用户的兴趣标签与日记的标签、标题、内容进行匹配，结合评分和热度，计算综合得分进行推荐。

### 10.2 数据结构

#### 输入

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | string | 用户ID |
| sort | string | 排序策略: heat/rating/time/interest |
| limit | int | 返回数量，默认10 |

#### 用户数据结构 (User)

```python
class User:
    id: str
    username: str
    interests: List[str]  # 兴趣标签列表，如 ["历史", "校园"]
    favorites: List[str]
    visited: List[str]
```

#### 日记数据结构 (Diary)

```python
class Diary:
    id: str
    user_id: str
    title: str  # 标题
    content: str  # 内容
    location_id: str  # 关联景点ID
    view_count: int  # 浏览量（热度）
    ratings: List[float]  # 评分列表
```

### 10.3 评分公式

#### 兴趣匹配得分

```
interest_match = matched_tags_count / user_interests_count
```

- 如果用户无兴趣标签：降级为 interest_fallback
- 如果日记无标签：interest_match = 0
- 范围：0 到 1

#### 内容匹配得分

```
content_match = content_hits / user_interests_count
```

其中 content_hits 是用户兴趣在 title + content 中出现的次数。

#### 综合得分

```
score = 0.45 * interest_match + 0.25 * rating_norm + 0.20 * heat_norm + 0.10 * content_match
```

权重分配：
- 兴趣匹配权重 45%（最重要）
- 评分权重 25%
- 热度权重 20%
- 内容匹配权重 10%

#### 归一化

```
rating_norm = avg_rating / 5.0
heat_norm = view_count / max_view_count
```

### 10.4 Top-K 流程

```
1. 获取所有日记列表
2. 如果 user_id 指定用户且 sort=interest:
   a. 获取用户兴趣标签
   b. 如果用户无兴趣，降级为 rating + heat 综合推荐
   c. 对每个日记计算:
      - interest_match = matched_tags / user_interests_count
      - content_match = content_hits / user_interests_count
      - rating_norm = avg_rating / 5.0
      - heat_norm = view_count / max_view_count
      - score = 0.45*interest_match + 0.25*rating_norm + 0.20*heat_norm + 0.10*content_match
   d. 使用 top_k(scored_diaries, limit, key=score, reverse=True)
3. 否则按默认策略（heat/rating/time）排序
```

### 10.5 时间复杂度和空间复杂度

| 指标 | 值 |
|------|------|
| 时间复杂度 | O(n log k)，n=日记数量，k=limit |
| 空间复杂度 | O(n)，存储所有日记的评分数据 |
| 适用场景 | n很大（数千到数万），k很小（10-100） |

### 10.6 特殊处理

#### 用户不存在
- 返回 code 404，message "用户不存在"

#### 用户无兴趣标签
- 降级为 strategy=interest_fallback
- 按 rating_norm * 0.6 + heat_norm * 0.4 综合评分

#### 日记无标签
- interest_match = 0，score 计算正常进行

### 10.7 返回格式

```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": "diary_001",
        "title": "北邮沙河一日游",
        "location_id": "CAMPUS001",
        "view_count": 103,
        "ratings": [5.0, 4.5],
        "score": 0.483,
        "interest_match": 0.0,
        "content_match": 0.5,
        "match_reasons": ["标题匹配: 校园", "内容匹配: 历史"]
      }
    ],
    "total": 10,
    "limit": 10,
    "strategy": "interest"
  },
  "message": "success"
}
```

### 10.8 Top-K 合规性

- 使用 `backend/core/sort.py:top_k` 实现
- 不是 `sorted(all)[:k]` 或 `list.sort()[:k]`
- 时间复杂度 O(n log k) vs 全量排序 O(n log n)

---

**最后更新**: 2026-05-04
**状态**: 景点和日记兴趣推荐均已完成实现和测试