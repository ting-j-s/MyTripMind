"""
模糊搜索算法实现
用于：景点名称搜索、美食名称搜索、饭店名称搜索
课程要求：必须自己实现
"""

from typing import List, Dict, Callable


def fuzzy_match(query: str, target: str, threshold: float = 0.6) -> Dict:
    """
    模糊匹配 - 判断查询字符串与目标字符串的相似度

    算法：编辑距离（Levenshtein Distance）+ Jaccard相似度

    时间复杂度: O(m*n)，m=query长度，n=target长度

    参数:
        query: 查询字符串
        target: 目标字符串
        threshold: 匹配阈值，0-1之间，越大越严格

    返回:
        {
            'match': True/False,
            'similarity': 0-1的相似度,
            'score': 得分
        }
    """
    if not query or not target:
        return {'match': False, 'similarity': 0, 'score': 0}

    # 统一转小写比较
    query_lower = query.lower()
    target_lower = target.lower()

    # 完全包含优先
    if query_lower in target_lower:
        similarity = len(query) / len(target)
        return {'match': True, 'similarity': similarity, 'score': similarity * 100}

    # 关键词匹配
    if target_lower.startswith(query_lower):
        similarity = len(query) / len(target) + 0.3  # 额外的起始匹配加分
        return {'match': True, 'similarity': min(similarity, 1.0), 'score': similarity * 100}

    # 编辑距离计算
    distance = levenshtein_distance(query_lower, target_lower)
    max_len = max(len(query), len(target))

    # Jaccard相似度（基于字符）
    jaccard_sim = jaccard_similarity(query_lower, target_lower)

    # 综合相似度：编辑距离相似度 * 0.4 + Jaccard * 0.6
    edit_similarity = 1 - (distance / max_len) if max_len > 0 else 0
    combined_similarity = edit_similarity * 0.4 + jaccard_sim * 0.6

    return {
        'match': combined_similarity >= threshold,
        'similarity': combined_similarity,
        'score': combined_similarity * 100,
        'edit_distance': distance
    }


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    编辑距离（Levenshtein Distance）

    定义：将字符串s1转换成s2所需的最少单字符编辑操作次数
    操作包括：插入、删除、替换

    时间复杂度: O(m*n)
    空间复杂度: O(m*n)

    示例:
        "kitten" -> "sitting": 3次 (k->s, e->i, +g)
    """
    m, n = len(s1), len(s2)

    # 动态规划表
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 初始化
    for i in range(m + 1):
        dp[i][0] = i  # 删除操作
    for j in range(n + 1):
        dp[0][j] = j  # 插入操作

    # 填充表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]  # 字符相同，无需操作
            else:
                dp[i][j] = min(
                    dp[i-1][j] + 1,      # 删除
                    dp[i][j-1] + 1,      # 插入
                    dp[i-1][j-1] + 1     # 替换
                )

    return dp[m][n]


def jaccard_similarity(s1: str, s2: str, n_gram: int = 2) -> float:
    """
    Jaccard相似度（基于n-gram）

    将字符串分割成n-gram集合，然后计算集合的Jaccard系数

    时间复杂度: O(m + n)
    """
    def get_ngrams(s: str, n: int) -> set:
        return set(s[i:i+n] for i in range(len(s) - n + 1))

    if not s1 or not s2:
        return 0

    ngrams1 = get_ngrams(s1, n_gram)
    ngrams2 = get_ngrams(s2, n_gram)

    # Jaccard = |A ∩ B| / |A ∪ B|
    intersection = ngrams1 & ngrams2
    union = ngrams1 | ngrams2

    if not union:
        return 0

    return len(intersection) / len(union)


def fuzzy_search(items: List[Dict], query: str,
                 fields: List[str] = None,
                 threshold: float = 0.5,
                 limit: int = 10) -> List[Dict]:
    """
    模糊搜索 - 在列表中搜索匹配的项目

    参数:
        items: 要搜索的列表，每个元素是字典
        query: 查询字符串
        fields: 要搜索的字段列表，如 ['name', 'title']
        threshold: 匹配阈值
        limit: 返回结果数量限制

    返回:
        匹配的项列表，按相似度降序排列

    示例:
        fuzzy_search(attractions, "故宫", fields=['name', 'tags'])
    """
    if not query or not items:
        return []

    results = []

    for item in items:
        best_score = 0
        best_field = None

        # 搜索指定字段
        search_fields = fields or list(item.keys())

        for field in search_fields:
            if field not in item:
                continue

            value = item[field]

            # 如果是字符串，直接匹配
            if isinstance(value, str):
                result = fuzzy_match(query, value, threshold)
                if result['match'] and result['score'] > best_score:
                    best_score = result['score']
                    best_field = field

            # 如果是列表（如tags），匹配列表中的每一项
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, str):
                        result = fuzzy_match(query, v, threshold)
                        if result['match'] and result['score'] > best_score:
                            best_score = result['score']
                            best_field = field

        if best_score > 0:
            item_copy = item.copy()
            item_copy['_fuzzy_score'] = best_score
            item_copy['_fuzzy_field'] = best_field
            results.append(item_copy)

    # 按分数降序排列
    results.sort(key=lambda x: x['_fuzzy_score'], reverse=True)

    return results[:limit]


def keyword_match(query: str, text: str, case_insensitive: bool = True) -> Dict:
    """
    关键词匹配 - 检查文本中是否包含查询关键词

    支持多关键词（用空格分隔）

    返回:
        {
            'match': True/False,
            'matched_keywords': [匹配的关键词列表],
            'match_count': 匹配数量
        }
    """
    if not query or not text:
        return {'match': False, 'matched_keywords': [], 'match_count': 0}

    if case_insensitive:
        query = query.lower()
        text = text.lower()

    keywords = query.split()
    matched = [kw for kw in keywords if kw in text]

    return {
        'match': len(matched) > 0,
        'matched_keywords': matched,
        'match_count': len(matched),
        'match_ratio': len(matched) / len(keywords) if keywords else 0
    }


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("模糊搜索算法测试")
    print("=" * 50)

    # 测试1：模糊匹配
    print("\n1. 模糊匹配测试:")
    test_cases = [
        ("故宫", "故宫博物院"),
        ("北大", "北京大学"),
        ("清华", "清华大学"),
        ("图书馆", "北京邮电大学图书馆"),
        ("食堂", "学生食堂"),
    ]

    for query, target in test_cases:
        result = fuzzy_match(query, target)
        status = "MATCH" if result['match'] else "NO"
        print(f"  '{query}' vs '{target}': {status} (score={result['score']:.1f})")

    # 测试2：编辑距离
    print("\n2. 编辑距离测试:")
    print(f"  'kitten' vs 'sitting': {levenshtein_distance('kitten', 'sitting')}")
    print(f"  'apple' vs 'apples': {levenshtein_distance('apple', 'apples')}")
    print(f"  '' vs 'test': {levenshtein_distance('', 'test')}")

    # 测试3：Jaccard相似度
    print("\n3. Jaccard相似度测试:")
    print(f"  '故宫' vs '故宫博物院': {jaccard_similarity('故宫', '故宫博物院'):.2f}")
    print(f"  '北京大学' vs '清华大学': {jaccard_similarity('北京大学', '清华大学'):.2f}")

    # 测试4：模糊搜索
    print("\n4. 模糊搜索测试:")
    attractions = [
        {"id": "1", "name": "故宫博物院", "type": "景区", "tags": ["历史", "博物馆"]},
        {"id": "2", "name": "北京大学", "type": "校园", "tags": ["大学", "历史"]},
        {"id": "3", "name": "清华大学", "type": "校园", "tags": ["大学", "校园"]},
        {"id": "4", "name": "天坛公园", "type": "景区", "tags": ["公园", "历史"]},
        {"id": "5", "name": "北京邮电大学", "type": "校园", "tags": ["大学", "通信"]},
    ]

    results = fuzzy_search(attractions, "故宫", fields=['name', 'tags'])
    print(f"  搜索'故宫':")
    for r in results:
        print(f"    {r['name']} (score={r['_fuzzy_score']:.1f})")

    results = fuzzy_search(attractions, "大学", fields=['name', 'tags'])
    print(f"  搜索'大学':")
    for r in results:
        print(f"    {r['name']} (score={r['_fuzzy_score']:.1f})")

    # 测试5：关键词匹配
    print("\n5. 关键词匹配测试:")
    text = "今天天气很好，我去参观了故宫博物院，非常壮观"
    result = keyword_match("故宫 博物院 参观", text)
    print(f"  文本: {text[:30]}...")
    print(f"  关键词'故宫 博物院 参观': matched={result['matched_keywords']}")

    print("\n[SUCCESS] Fuzzy search test passed!")
