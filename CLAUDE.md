# TripMind 项目规则

## 自动提交
完成任务后，自动 stage 相关文件并创建 git commit，使用项目的 commit message 风格（简洁描述，中文或英文均可）。不需要等用户明确要求提交。对于小的单行修改可以与下一个有意义的变更一起批量提交。

## 项目上下文
- 个性化旅游系统，Flask 后端 + 原生 HTML/CSS/JS 前端
- 数据存储：JSON 文件（`backend/data/*.json`），不使用数据库
- 核心算法需自己实现：Dijkstra、TSP、Top-K（堆选）、模糊搜索、倒排索引全文搜索、霍夫曼压缩
- 算法文件在 `backend/algorithms/`，数据结构在 `backend/core/`
- 测试：186 个用例，`python -m pytest -q`
