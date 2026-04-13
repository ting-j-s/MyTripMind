"""
将Markdown文档转换为PDF - 方案设计版
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 注册中文字体
try:
    pdfmetrics.registerFont(TTFont('SimHei', 'C:/Windows/Fonts/simhei.ttf'))
    pdfmetrics.registerFont(TTFont('Microsoft YaHei', 'C:/Windows/Fonts/msyh.ttc'))
    CHINESE_FONT = 'SimHei'
except:
    CHINESE_FONT = 'Helvetica'

# 创建PDF
output_path = 'E:\\TripMind\\课程设计方案.pdf'
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

# 获取样式
styles = getSampleStyleSheet()

# 创建自定义样式
styles.add(ParagraphStyle(
    name='ChineseTitle',
    parent=styles['Title'],
    fontName=CHINESE_FONT,
    fontSize=22,
    leading=28,
    spaceAfter=16,
))
styles.add(ParagraphStyle(
    name='ChineseH1',
    parent=styles['Heading1'],
    fontName=CHINESE_FONT,
    fontSize=16,
    leading=22,
    spaceAfter=10,
    spaceBefore=18,
))
styles.add(ParagraphStyle(
    name='ChineseH2',
    parent=styles['Heading2'],
    fontName=CHINESE_FONT,
    fontSize=13,
    leading=18,
    spaceAfter=8,
    spaceBefore=12,
))
styles.add(ParagraphStyle(
    name='ChineseH3',
    parent=styles['Heading3'],
    fontName=CHINESE_FONT,
    fontSize=11,
    leading=16,
    spaceAfter=6,
    spaceBefore=8,
))
styles.add(ParagraphStyle(
    name='ChineseBody',
    parent=styles['Normal'],
    fontName=CHINESE_FONT,
    fontSize=10,
    leading=15,
    firstLineIndent=0,
))
styles.add(ParagraphStyle(
    name='ChineseIndent',
    parent=styles['Normal'],
    fontName=CHINESE_FONT,
    fontSize=10,
    leading=15,
    leftIndent=20,
))
styles.add(ParagraphStyle(
    name='ChineseCode',
    parent=styles['Code'],
    fontName='Courier',
    fontSize=8,
    leading=11,
))

story = []

# 封面
story.append(Spacer(1, 80))
story.append(Paragraph("个性化旅游系统", styles['ChineseTitle']))
story.append(Paragraph("方案设计文档", styles['ChineseTitle']))
story.append(Spacer(1, 40))
story.append(Paragraph("<b>课程名称：</b>数据结构课程设计", styles['ChineseBody']))
story.append(Paragraph("<b>项目名称：</b>基于智能体的个性化旅游系统的设计和开发", styles['ChineseBody']))
story.append(Paragraph("<b>日期：</b>2026年4月", styles['ChineseBody']))
story.append(PageBreak())

# 第1章
story.append(Paragraph("1. 项目概述", styles['ChineseH1']))
story.append(Paragraph("<b>1.1 项目背景</b>", styles['ChineseH2']))
story.append(Paragraph("传统旅游系统功能单一，缺乏个性化推荐和智能化路线规划。本系统旨在为用户提供一个集景点推荐、路线规划、场所查询、旅游日记分享和美食推荐于一体的个性化旅游管理平台。", styles['ChineseBody']))

story.append(Paragraph("<b>1.2 技术约束</b>", styles['ChineseH2']))
constraints = [
    "核心算法必须自己实现，禁止直接调用数据库的排序、查找",
    "必须使用自己设计的数据结构（堆、哈希表、链表、图等）",
    "不使用数据库存储核心功能，采用JSON文件存储",
    "考核重点：数据结构的设计及选择、算法复杂度平衡",
]
for c in constraints:
    story.append(Paragraph("• " + c, styles['ChineseIndent']))

# 第2章
story.append(Paragraph("2. 技术架构设计", styles['ChineseH1']))
story.append(Paragraph("<b>2.1 系统架构</b>", styles['ChineseH2']))
story.append(Paragraph("前后端分离架构：浏览器(HTML/CSS/JS) → Flask后端 → JSON文件存储", styles['ChineseBody']))

story.append(Paragraph("<b>2.2 技术选型</b>", styles['ChineseH2']))
tech_data = [
    ['层次', '技术', '选型理由'],
    ['前端', 'HTML5 + CSS3 + JS', '课程要求，不依赖框架'],
    ['后端', 'Python Flask', '轻量级，易于实现REST API'],
    ['存储', 'JSON文件', '避免数据库，核心功能手动实现'],
    ['地图', 'Leaflet + 本地瓦片', '免费、可离线、课程允许'],
]
tech_table = Table(tech_data, colWidths=[3*cm, 5*cm, 5*cm])
tech_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), CHINESE_FONT),
    ('FONTNAME', (0, 1), (-1, -1), CHINESE_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
]))
story.append(tech_table)

# 第3章
story.append(PageBreak())
story.append(Paragraph("3. 数据结构设计", styles['ChineseH1']))
story.append(Paragraph("<b>3.1 核心数据结构选型</b>", styles['ChineseH2']))
ds_data = [
    ['数据结构', '选用理由', '应用场景'],
    ['图（邻接表）', '稀疏图空间效率高', '道路网络存储'],
    ['堆（最小堆）', '快速获取最小值', 'Dijkstra、Top-K排序'],
    ['哈希表', 'O(1)查找比O(n)快', '用户ID、日记ID查询'],
    ['链表', '动态扩展', '日记、美食列表'],
]
ds_table = Table(ds_data, colWidths=[3.5*cm, 5*cm, 4.5*cm])
ds_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), CHINESE_FONT),
    ('FONTNAME', (0, 1), (-1, -1), CHINESE_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
]))
story.append(ds_table)

story.append(Paragraph("<b>3.2 图结构设计</b>", styles['ChineseH2']))
story.append(Paragraph("使用邻接表存储稀疏图，边权重支持多种计算方式：", styles['ChineseBody']))
edge_items = [
    "最短距离：weight = distance",
    "最短时间：weight = distance / (congestion × ideal_speed)",
    "交通工具约束：扩展边时过滤 road_types",
]
for item in edge_items:
    story.append(Paragraph("• " + item, styles['ChineseIndent']))

# 第4章
story.append(PageBreak())
story.append(Paragraph("4. 核心算法方案", styles['ChineseH1']))

story.append(Paragraph("<b>4.1 最短路径 - Dijkstra</b>", styles['ChineseH2']))
dijkstra_data = [
    ['变体', '边权重', '应用场景'],
    ['标准Dijkstra', 'distance', '最短距离策略'],
    ['时间Dijkstra', 'distance/(congestion×speed)', '最短时间策略'],
    ['约束Dijkstra', '边过滤', '交通工具约束'],
]
dijkstra_table = Table(dijkstra_data, colWidths=[4*cm, 6*cm, 3*cm])
dijkstra_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), CHINESE_FONT),
    ('FONTNAME', (0, 1), (-1, -1), CHINESE_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
]))
story.append(dijkstra_table)
story.append(Paragraph("时间复杂度：O((V+E) log V)，空间复杂度：O(V)", styles['ChineseIndent']))

story.append(Paragraph("<b>4.2 多景点路线 - TSP</b>", styles['ChineseH2']))
story.append(Paragraph("贪心最近邻 O(n²) → 2-opt优化 O(n²×iter)", styles['ChineseBody']))
story.append(Paragraph("为什么不用精确算法？TSP是NP难问题，贪心+局部搜索是工程常用近似算法", styles['ChineseIndent']))

story.append(Paragraph("<b>4.3 Top-K排序</b>", styles['ChineseH2']))
story.append(Paragraph("维护大小为k的小顶堆：时间复杂度 O(n log k)，比全排序 O(n log n) 更高效", styles['ChineseBody']))

story.append(Paragraph("<b>4.4 搜索与压缩</b>", styles['ChineseH2']))
algo_items = [
    "模糊搜索：编辑距离算法（Levenshtein），支持容错查询",
    "全文检索：倒排索引，O(1)查找 + O(n)返回",
    "霍夫曼压缩：变长编码，压缩率30%-50%",
]
for item in algo_items:
    story.append(Paragraph("• " + item, styles['ChineseIndent']))

# 第5章
story.append(PageBreak())
story.append(Paragraph("5. 模块划分", styles['ChineseH1']))
story.append(Paragraph("<b>5.1 模块结构</b>", styles['ChineseH2']))
story.append(Paragraph("Routes层 → Services层 → Algorithms层 → Core层", styles['ChineseBody']))

story.append(Paragraph("<b>5.2 各模块职责</b>", styles['ChineseH2']))
mod_data = [
    ['模块', '核心功能', '关键数据结构'],
    ['auth', '注册、登录、登出', 'HashTable'],
    ['attractions', '列表、搜索、推荐', 'Heap、HashTable'],
    ['route', '最短路径、TSP路线', 'Graph、Dijkstra'],
    ['diary', 'CRUD、评分、搜索', 'LinkedList、TextSearch'],
    ['food', '列表、搜索、推荐', 'Heap、FuzzySearch'],
    ['user', '个人信息、收藏', 'HashTable'],
]
mod_table = Table(mod_data, colWidths=[3*cm, 5*cm, 5*cm])
mod_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), CHINESE_FONT),
    ('FONTNAME', (0, 1), (-1, -1), CHINESE_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
]))
story.append(mod_table)

# 第6章
story.append(Paragraph("6. API接口设计", styles['ChineseH1']))
api_data = [
    ['方法', '路径', '说明'],
    ['POST', '/api/auth/register', '用户注册'],
    ['POST', '/api/auth/login', '用户登录'],
    ['GET', '/api/attractions', '景点列表'],
    ['GET', '/api/attractions/search', '景点搜索'],
    ['GET', '/api/recommend', '个性化推荐'],
    ['POST', '/api/route/shortest', '最短路径'],
    ['POST', '/api/route/tsp', 'TSP多景点'],
    ['GET', '/api/nearby', '附近设施'],
    ['GET', '/api/diaries', '日记列表'],
    ['POST', '/api/diary', '创建日记'],
    ['GET', '/api/diaries/search', '日记搜索'],
    ['GET', '/api/foods', '美食列表'],
    ['GET', '/api/foods/search', '美食搜索'],
]
api_table = Table(api_data, colWidths=[2*cm, 5.5*cm, 5.5*cm])
api_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), CHINESE_FONT),
    ('FONTNAME', (0, 1), (-1, -1), CHINESE_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
]))
story.append(api_table)

# 第7章
story.append(PageBreak())
story.append(Paragraph("7. 开发计划", styles['ChineseH1']))
story.append(Paragraph("<b>7.1 进度安排</b>", styles['ChineseH2']))
plan_data = [
    ['阶段', '时间', '内容'],
    ['方案设计', '第4周', '方案文档、架构设计（当前）'],
    ['核心实现', '第5-6周', '数据结构、算法实现'],
    ['后端开发', '第7-8周', 'API接口、业务逻辑'],
    ['前端开发', '第9-10周', '页面、交互、地图'],
    ['联调测试', '第11周', '前后端联调、测试'],
    ['验收完善', '第12-15周', '文档、演示、答辩'],
]
plan_table = Table(plan_data, colWidths=[3*cm, 2.5*cm, 7.5*cm])
plan_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), CHINESE_FONT),
    ('FONTNAME', (0, 1), (-1, -1), CHINESE_FONT),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.8, 0.8, 0.8)),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
]))
story.append(plan_table)

# 第8章
story.append(Paragraph("8. 关键技术决策", styles['ChineseH1']))
story.append(Paragraph("<b>8.1 Dijkstra为什么用堆优化？</b>", styles['ChineseH2']))
story.append(Paragraph("普通Dijkstra需要O(V²)找最小节点，使用最小堆后复杂度降为O((V+E) log V)", styles['ChineseBody']))

story.append(Paragraph("<b>8.2 Top-K为什么不直接排序？</b>", styles['ChineseH2']))
story.append(Paragraph("全排序 O(n log n) vs Top-K堆 O(n log k)，k=10时效率提升约50%", styles['ChineseBody']))

story.append(Paragraph("<b>8.3 为什么不使用数据库？</b>", styles['ChineseH2']))
story.append(Paragraph("课程明确要求不要使用数据库完成核心功能，使用JSON文件+自建HashTable替代", styles['ChineseBody']))

# 第9章
story.append(Paragraph("9. 创新点", styles['ChineseH1']))
innovations = [
    "多种路径策略：最短距离、最短时间、交通工具约束三种策略",
    "TSP 2-opt优化：在贪心解基础上迭代改进，提升路径质量",
    "霍夫曼压缩存储：日记内容压缩存储，节省空间",
    "倒排索引全文搜索：高效支持多词查询",
]
for inn in innovations:
    story.append(Paragraph("• " + inn, styles['ChineseIndent']))

story.append(Spacer(1, 40))
story.append(Paragraph("— 文档完 —", styles['ChineseBody']))
story.append(Paragraph("<b>版本：</b>v1.0 | <b>日期：</b>2026年4月", styles['ChineseBody']))

# 生成PDF
doc.build(story)
print(f"PDF生成成功: {output_path}")
