# 个性化旅游系统 - 系统设计文档

**版本**：v2.0
**日期**：2026-03-25
**状态**：与PRD.md保持一致

---

## 1. 项目概述

**项目名称**：个性化旅游系统（Personalized Travel System）
**项目类型**：前后端分离Web应用
**前端技术**：HTML5 + CSS3 + 原生JavaScript
**后端技术**：Python Flask + SQLite
**地图服务**：高德地图API

---

## 2. 目录结构

```
e:/TripMind/
│
├── backend/                        # 后端目录
│   ├── __init__.py
│   ├── app.py                      # Flask应用入口
│   ├── config.py                   # 配置文件
│   │
│   ├── core/                       # 核心数据结构和算法
│   │   ├── __init__.py
│   │   ├── graph.py                # 图结构（邻接表）
│   │   ├── heap.py                 # 堆（优先队列）
│   │   ├── hash_table.py           # 哈希表（自己实现）
│   │   ├── linked_list.py          # 链表
│   │   └── sort.py                 # 排序算法
│   │
│   ├── algorithms/                # 核心算法
│   │   ├── __init__.py
│   │   ├── dijkstra.py             # Dijkstra最短路径
│   │   ├── dijkstra_var.py         # Dijkstra变体（时间/交通）
│   │   ├── tsp.py                  # 旅行商问题
│   │   ├── top_k.py                # Top-K部分排序
│   │   ├── fuzzy_search.py          # 模糊搜索
│   │   ├── text_search.py          # 全文搜索
│   │   └── compression.py           # 霍夫曼压缩
│   │
│   ├── models/                    # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py                 # 用户模型
│   │   ├── attraction.py            # 景点模型
│   │   ├── building.py              # 建筑模型
│   │   ├── facility.py             # 设施模型
│   │   ├── road.py                 # 道路模型
│   │   ├── diary.py                # 日记模型
│   │   └── food.py                 # 美食模型
│   │
│   ├── routes/                    # 路由/接口
│   │   ├── __init__.py
│   │   ├── auth.py                 # 认证接口
│   │   ├── attractions.py          # 景点接口
│   │   ├── route.py                # 路线接口
│   │   ├── nearby.py               # 场所接口
│   │   ├── diary.py                # 日记接口
│   │   ├── food.py                 # 美食接口
│   │   └── user.py                 # 用户接口
│   │
│   ├── services/                  # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── recommend_service.py    # 推荐服务
│   │   ├── route_service.py       # 路线服务
│   │   ├── search_service.py       # 搜索服务
│   │   └── aigc_service.py         # AIGC服务
│   │
│   └── utils/                     # 工具
│       ├── __init__.py
│       ├── hash_func.py           # 哈希函数
│       └── distance.py            # 距离计算
│
├── frontend/                       # 前端目录
│   ├── index.html                  # 主页
│   ├── login.html                  # 登录页
│   ├── register.html               # 注册页
│   ├── css/
│   │   ├── style.css               # 全局样式
│   │   ├── home.css                # 首页样式
│   │   ├── attraction.css          # 景点页样式
│   │   ├── route.css               # 路线页样式
│   │   ├── diary.css               # 日记页样式
│   │   └── food.css                # 美食页样式
│   ├── js/
│   │   ├── api.js                  # API调用封装
│   │   ├── auth.js                 # 认证逻辑
│   │   ├── home.js                 # 首页逻辑
│   │   ├── attraction.js           # 景点逻辑
│   │   ├── route.js                # 路线逻辑
│   │   ├── nearby.js               # 场所逻辑
│   │   ├── diary.js                # 日记逻辑
│   │   ├── food.js                 # 美食逻辑
│   │   ├── map.js                  # 地图组件
│   │   └── utils.js                # 工具函数
│   └── pages/
│       ├── home.html               # 首页
│       ├── attraction_detail.html  # 景点详情
│       ├── route_plan.html         # 路线规划
│       ├── diary_square.html       # 日记广场
│       ├── diary_write.html        # 写日记
│       ├── diary_detail.html       # 日记详情
│       ├── food.html               # 美食
│       └── profile.html            # 个人中心
│
├── data/                          # 数据目录
│   ├── init_data.py               # 数据初始化脚本
│   ├── attractions.json           # 景点数据
│   ├── buildings.json             # 建筑数据（北邮全建筑）
│   ├── facilities.json            # 设施数据
│   ├── roads.json                 # 道路数据
│   ├── diaries.json               # 日记数据
│   ├── foods.json                 # 美食数据
│   └── users.json                 # 用户数据
│
├── aigc/                          # AIGC相关
│   └── qwen_client.py             # 通义千问客户端
│
├── requirements.txt               # Python依赖
├── README.md                      # 项目说明
├── PRD.md                         # 需求文档
└── SPEC.md                        # 本文档
```

---

## 3. 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户浏览器                               │
│                    HTML5 + CSS3 + JavaScript                    │
│                         + 高德地图                              │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Python Flask 后端                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Routes/API  │  │  Services    │  │  Algorithms  │        │
│  │   路由接口层   │  │   业务逻辑层   │  │   核心算法层   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Models    │  │    Core      │  │   Utils      │        │
│  │   数据模型    │  │   基础结构    │  │    工具      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────┬───────────────────────────────────┘
                              │ SQL / JSON
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SQLite 数据库                               │
│        (数据存储) + JSON文件 (景点/建筑/道路等数据)             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. 核心算法清单

| 算法 | 文件 | 时间复杂度 | 用途 |
|------|------|------------|------|
| **快速排序** | sort.py | O(n log n) | 基础排序 |
| **堆排序** | sort.py | O(n log n) | Top-K排序 |
| **Top-K** | top_k.py | O(n log k) | 只排前10个景点/美食 |
| **Dijkstra** | dijkstra.py | O((V+E) log V) | 单源最短路径 |
| **Dijkstra时间** | dijkstra_var.py | O((V+E) log V) | 考虑拥挤度的时间最短 |
| **Dijkstra约束** | dijkstra_var.py | O((V+E) log V) | 交通工具约束 |
| **TSP贪心** | tsp.py | O(n²) | 多点闭环路径 |
| **哈希表** | hash_table.py | O(1) 平均 | 日记ID查询 |
| **模糊匹配** | fuzzy_search.py | O(n×m) | 美食/景点名称模糊查询 |
| **全文搜索** | text_search.py | O(n) | 日记内容检索 |
| **霍夫曼压缩** | compression.py | O(n log n) | 日记压缩存储 |

---

## 5. 数据库/数据文件设计

### 5.1 数据文件对应

| 数据类型 | 存储方式 | 文件 |
|----------|----------|------|
| 用户 | SQLite users表 | 写入数据库 |
| 景点 | JSON文件 | attractions.json |
| 建筑 | JSON文件 | buildings.json |
| 设施 | JSON文件 | facilities.json |
| 道路 | JSON文件 | roads.json |
| 日记 | SQLite diaries表 | 写入数据库 |
| 美食 | JSON文件 | foods.json |

### 5.2 道路数据结构（重点）

```json
{
  "roads": [
    {
      "id": "RD_001",
      "from": "BLD_001",
      "to": "BLD_002",
      "distance": 150,
      "ideal_speed": 5,
      "congestion": 0.8,
      "road_types": ["步行", "自行车"],
      "floor": 0
    },
    {
      "id": "RD_002",
      "from": "ENTRANCE_1",
      "to": "ELEVATOR_A",
      "distance": 30,
      "ideal_speed": 3,
      "congestion": 1.0,
      "road_types": ["步行"],
      "floor": 0
    }
  ]
}
```

**road_types 说明**：
- `["步行"]` - 只允许步行
- `["步行", "自行车"]` - 步行+自行车
- `["步行", "电瓶车"]` - 电瓶车路线

### 5.3 建筑数据结构（室内导航）

```json
{
  "buildings": [
    {
      "id": "BUPT_LIB",
      "name": "北京邮电大学图书馆",
      "type": "教学楼",
      "campus_id": "BUPT",
      "x": 116.352,
      "y": 39.963,
      "floors": 5,
      "rooms": ["101", "102", "201", "自息室", "会议室A"],
      "elevators": ["电梯A", "电梯B"],
      "entrances": ["东门", "西门"]
    }
  ]
}
```

---

## 6. 北邮（BUPT）数据

### 6.1 校园信息

| 属性 | 值 |
|------|-----|
| 名称 | 北京邮电大学（BUPT） |
| 地址 | 北京市海淀区西土城路10号 |
| 类型 | 校园 |

### 6.2 主要建筑清单（待填充）

**教学楼类**：
- 主教学楼
- 图书馆
- 行政楼
- 学生活动中心

**生活服务类**：
- 食堂（多个）
- 宿舍楼（多个）
- 超市
- 医院/卫生所

**体育设施类**：
- 体育馆
- 操场/体育场
- 篮球场
- 网球场

**其他**：
- 体育馆
- 网络信息中心
- 各学院办公楼

**详细道路和建筑数据，在你验收前需要时问我获取。**

---

## 7. 模块功能划分

```
┌─────────────────────────────────────────────────────────────────┐
│                         前端 (frontend/)                        │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │ 首页   │ │ 景点   │ │ 路线   │ │ 日记   │ │ 美食   │        │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      后端 Routes (routes/)                      │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │ 认证   │ │ 景点   │ │ 路线   │ │ 日记   │ │ 美食   │        │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    后端 Services (services/)                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ recommend_   │ │ route_       │ │ search_      │            │
│  │ service      │ │ service      │ │ service      │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   后端 Algorithms (algorithms/)                  │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐   │
│  │TopK  │ │Dijk  │ │ TSP  │ │模糊  │ │全文  │ │霍夫曼   │   │
│  │排序  │ │stra  │ │算法  │ │搜索  │ │搜索  │ │压缩     │   │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       数据层 (SQLite + JSON)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ users    │ │ diaries  │ │roads.json│ │building. │          │
│  │ 表       │ │ 表       │ │道路数据   │ │json建筑  │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. 实现顺序

| 阶段 | 内容 | 交付物 |
|------|------|--------|
| **Step 1** | 项目架子（Flask + 目录结构） | 可运行的空项目 |
| **Step 2** | 基础数据结构（堆、哈希表、排序） | core/algorithms/ |
| **Step 3** | 图结构 + Dijkstra + TSP | algorithms/dijkstra.py, tsp.py |
| **Step 4** | 数据模型 + 文件读写 | models/ + data/ |
| **Step 5** | Top-K + 模糊搜索 + 全文搜索 | algorithms/top_k.py, fuzzy_search.py |
| **Step 6** | 霍夫曼压缩 | algorithms/compression.py |
| **Step 7** | 后端API接口（6大模块） | routes/ |
| **Step 8** | 前端页面（HTML/CSS/JS） | frontend/ |
| **Step 9** | 地图集成（高德API） | 地图展示+路径绘制 |
| **Step 10** | AIGC集成（通义千问） | 动画生成功能 |
| **Step 11** | 生成测试数据 + 联调 | 可运行完整系统 |
| **Step 12** | 代码解释PDF文档 | 验收背诵材料 |

---

## 9. 关键技术点

### 9.1 为什么自己实现哈希表？
- 课程要求：核心算法必须自己实现
- 日记查询用ID，哈希表O(1)比遍历O(n)快很多

### 9.2 Dijkstra为什么用邻接表+堆？
- 邻接表：存储稀疏图省空间
- 堆（优先队列）：快速取出当前最短距离节点
- 时间复杂度 O((V+E) log V)

### 9.3 Top-K为什么不直接排序？
- 10000个景点，用户只看前10
- 直接排序：O(n log n)
- Top-K堆选：O(n log k)，k=10时效率提升明显

### 9.4 TSP为什么用贪心？
- n个点的TSP是NP难问题
- 贪心最近邻：O(n²)，实现简单，效果尚可
- 验收时够用

### 9.5 室内导航怎么做？
- 电梯作为特殊节点，连接不同楼层
- 每层楼的房间作为该层的节点
- 用标准Dijkstra即可

### 9.6 拥挤度计算
```python
真实速度 = 拥挤度 × 理想速度
时间 = 距离 / 真实速度
```

---

## 10. API接口速查

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register | 注册 |
| POST | /api/auth/login | 登录 |
| GET | /api/attractions | 景点列表 |
| GET | /api/attractions/search | 搜索 |
| GET | /api/recommend | 推荐 |
| POST | /api/route/shortest | 最短路径 |
| POST | /api/route/tsp | TSP路线 |
| GET | /api/nearby | 附近设施 |
| GET | /api/diaries | 日记列表 |
| POST | /api/diary | 创建日记 |
| GET | /api/diaries/search | 日记搜索 |
| POST | /api/diary/:id/rate | 评分 |
| GET | /api/foods | 美食列表 |
| GET | /api/foods/search | 美食搜索 |
| POST | /api/aigc/animation | 生成动画 |

---

*文档版本：v2.0*
*与PRD.md v1.0保持一致*
*新增：北邮校内导航支持*
