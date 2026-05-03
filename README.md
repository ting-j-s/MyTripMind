# 个性化旅游系统 (TripMind)

基于智能体的个性化旅游系统的设计和开发

## 项目简介

本系统是一个集景点推荐、路线规划、场所查询、旅游日记分享和美食推荐于一体的综合性旅游管理平台。

## 环境要求

- Python 3.10+
- Flask 3.0.0
- pip

## 安装依赖

```bash
pip install -r requirements.txt
```

或使用系统包管理（需要 --break-system-packages）：

```bash
pip install --break-system-packages -r requirements.txt
```

## 运行测试

```bash
python -m pytest tests -q
```

当前测试状态：**95 passed**

## 启动后端

```bash
cd backend
python app.py
```

后端地址：http://127.0.0.1:5000

如端口被占用，可修改 `backend/app.py` 中的 `port=5000` 为其他端口。

## 启动前端

```bash
cd frontend
python -m http.server 8080
```

访问 http://localhost:8080

## 功能模块

- **旅游推荐**：基于热度、评分、兴趣的个性化景点推荐
- **路线规划**：Dijkstra最短路径 + TSP多景点路线规划 + 室内导航
- **场所查询**：基于道路网络的附近设施查询（使用Dijkstra道路距离）
- **日记管理**：旅游日记的创建、分享、评分和全文检索
- **美食推荐**：按热度、评分、道路距离排序，支持模糊搜索
- **室内导航**：教学楼/图书馆等多楼层建筑内路径规划

## 技术栈

- **后端**：Python Flask
- **前端**：HTML5 + CSS3 + JavaScript
- **地图**：Leaflet
- **存储**：JSON文件

## 核心算法

| 算法 | 说明 |
|------|------|
| Dijkstra | 单源最短路径 |
| TSP | 多景点闭环路径（贪心 + 2-opt） |
| Top-K排序 | 高效选取前K名 |
| 模糊搜索 | 编辑距离匹配 |
| 全文检索 | 倒排索引 |
| 霍夫曼压缩 | 日记内容压缩存储 |

## 核心数据结构

| 数据结构 | 说明 |
|----------|------|
| 图 | 邻接表存储道路网络 |
| 堆 | 优先队列、最小堆 |
| 哈希表 | 快速查找 |
| 链表 | 动态列表 |

## 课程要求

本项目为北京邮电大学数据结构课程设计，完成以下要求：

- 自己实现核心数据结构（堆、哈希表、链表、图等）
- 自己实现核心算法（Dijkstra、TSP、Top-K排序等）
- 不使用数据库存储核心功能
- 使用JSON文件进行数据存储

## 项目结构

```
backend/
├── algorithms/     # 核心算法
├── core/          # 核心数据结构
├── data/          # 数据文件
├── models/        # 数据模型
├── routes/        # API路由
├── services/       # 业务服务
├── utils/         # 工具函数
└── app.py         # Flask入口

frontend/
├── pages/         # HTML页面
├── css/           # 样式文件
└── js/            # JavaScript

tests/             # 测试文件
docs/              # 文档
scripts/           # 数据处理脚本
```

---

**课程**：数据结构课程设计
**学校**：北京邮电大学
