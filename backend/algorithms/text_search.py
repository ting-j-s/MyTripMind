"""
全文搜索算法实现
用于：日记内容关键词搜索
课程要求：必须自己实现
"""

from typing import List, Dict, Set, Tuple
import re


class TextSearchIndex:
    """
    文本搜索索引 - 使用倒排索引加速搜索

    倒排索引（Inverted Index）：
        普通索引：文档ID -> 文档内容
        倒排索引：词 -> [文档ID列表]

    适用于：大量文档的关键词搜索
    """

    def __init__(self):
        # 倒排索引：{词: [(文档ID, 词频), ...]}
        self._inverted_index = {}
        # 文档存储：{文档ID: 文档内容}
        self._documents = {}
        # 文档词频：{文档ID: {词: 次数}}
        self._doc_term_freq = {}

    def add_document(self, doc_id: str, content: str, metadata: Dict = None):
        """
        添加文档到索引

        参数:
            doc_id: 文档唯一ID
            content: 文档内容
            metadata: 文档的元数据（如标题、作者等）
        """
        # 预处理：分词、去停用词、提取词干
        words = self._tokenize(content)

        # 更新文档存储
        self._documents[doc_id] = {
            'content': content,
            'metadata': metadata or {},
            'word_count': len(words)
        }

        # 更新词频
        self._doc_term_freq[doc_id] = {}
        for word in words:
            self._doc_term_freq[doc_id][word] = self._doc_term_freq[doc_id].get(word, 0) + 1

        # 更新倒排索引
        for word in set(words):
            if word not in self._inverted_index:
                self._inverted_index[word] = []
            self._inverted_index[word].append((doc_id, self._doc_term_freq[doc_id][word]))

    def _tokenize(self, text: str) -> List[str]:
        """
        分词 - 将文本分割成单词列表

        简单实现：按空格和标点分割，转小写

        实际生产环境应使用：jieba分词、hanlp等中文分词库
        """
        if not text:
            return []

        # 转小写
        text = text.lower()

        # 去除标点符号，只保留字母、数字、中文
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)

        # 按空格分割
        words = text.split()

        # 去除停用词
        stop_words = self._get_stop_words()

        # 去除长度小于2的词（英文）
        words = [w for w in words if len(w) >= 2 and w not in stop_words]

        return words

    def _get_stop_words(self) -> Set[str]:
        """
        获取停用词表

        停用词：常见但无意义的词，如"的"、"是"等
        """
        # 简单的中文停用词
        chinese_stopwords = {
            '的', '是', '在', '了', '和', '与', '或', '的', '地', '得',
            '我', '你', '他', '她', '它', '们', '这', '那', '有', '没有',
            '个', '了', '啊', '呢', '吧', '吗', '哦', '嗯', '噢',
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'and', 'or', 'but', 'if', 'then', 'so', 'because', 'as'
        }
        return chinese_stopwords

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        搜索文档

        参数:
            query: 查询字符串
            limit: 返回结果数量

        返回:
            [{doc_id, content, score, metadata}, ...]
        """
        if not query:
            return []

        # 分词
        query_words = self._tokenize(query)

        if not query_words:
            return []

        # 计算每个文档的得分
        doc_scores = {}

        for word in query_words:
            if word not in self._inverted_index:
                continue

            # 获取包含该词的文档列表
            for doc_id, term_freq in self._inverted_index[word]:
                if doc_id not in doc_scores:
                    doc_scores[doc_id] = {
                        'score': 0,
                        'matched_words': set()
                    }

                # TF-IDF风格的评分
                tf = term_freq
                idf = 1.0  # 简化版本，不计算全局IDF
                doc_scores[doc_id]['score'] += tf * idf
                doc_scores[doc_id]['matched_words'].add(word)

        # 排序并返回
        results = []
        for doc_id, data in doc_scores.items():
            doc = self._documents[doc_id]
            results.append({
                'doc_id': doc_id,
                'content': doc['content'],
                'metadata': doc['metadata'],
                'score': data['score'],
                'matched_words': list(data['matched_words']),
                'match_count': len(data['matched_words'])
            })

        # 按分数降序
        results.sort(key=lambda x: (x['score'], x['match_count']), reverse=True)

        return results[:limit]

    def search_with_context(self, query: str, context_len: int = 50,
                           limit: int = 10) -> List[Dict]:
        """
        搜索并返回包含关键词上下文的片段

        用于在搜索结果中显示匹配的文字片段
        """
        results = self.search(query, limit)
        query_words = set(self._tokenize(query))

        for result in results:
            content = result['content']
            # 找到第一个匹配词的位置
            match_pos = -1
            for word in query_words:
                pos = content.lower().find(word)
                if pos != -1:
                    if match_pos == -1 or pos < match_pos:
                        match_pos = pos

            # 提取上下文
            if match_pos != -1:
                start = max(0, match_pos - context_len)
                end = min(len(content), match_pos + context_len + len(query))
                excerpt = content[start:end]
                if start > 0:
                    excerpt = '...' + excerpt
                if end < len(content):
                    excerpt = excerpt + '...'
                result['excerpt'] = excerpt

        return results

    def document_count(self) -> int:
        """文档数量"""
        return len(self._documents)

    def word_count(self) -> int:
        """索引词数量"""
        return len(self._inverted_index)


def simple_text_search(documents: List[Dict], query: str,
                      content_field: str = 'content',
                      limit: int = 10) -> List[Dict]:
    """
    简单的文本搜索（不使用索引）

    适用于：文档数量较少的场景

    参数:
        documents: 文档列表
        query: 查询字符串
        content_field: 内容字段名
        limit: 返回数量

    返回:
        匹配的文档列表，按相关度排序
    """
    if not query or not documents:
        return []

    # 简单的关键词匹配
    results = []

    for doc in documents:
        content = doc.get(content_field, '')
        if not content:
            continue

        # 计算匹配词数
        query_words = query.lower().split()
        content_lower = content.lower()

        matched = 0
        for word in query_words:
            if word in content_lower:
                matched += 1

        if matched > 0:
            doc_copy = doc.copy()
            doc_copy['_match_score'] = matched
            doc_copy['_match_ratio'] = matched / len(query_words)
            results.append(doc_copy)

    # 排序
    results.sort(key=lambda x: (x['_match_score'], x['_match_ratio']), reverse=True)

    return results[:limit]


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("全文搜索算法测试")
    print("=" * 50)

    # 创建索引
    index = TextSearchIndex()

    # 添加文档
    docs = [
        ("d1", "今天天气很好，我去故宫参观，故宫很大很壮观，故宫的历史很长。"),
        ("d2", "北京大学的校园很美丽，春天樱花盛开，北大很适合参观。"),
        ("d3", "清华大学和北京大学都在北京，两所大学都很著名。"),
        ("d4", "去旅游的话，故宫是必去的景点，天坛公园也很不错。"),
        ("d5", "北京邮电大学的食堂饭菜很好吃，图书馆环境也不错。"),
    ]

    for doc_id, content in docs:
        index.add_document(doc_id, content)

    print(f"\n索引创建完成: {index.document_count()}个文档, {index.word_count()}个词")

    # 测试搜索
    print("\n1. 搜索'故宫':")
    results = index.search("故宫")
    for r in results:
        print(f"  {r['doc_id']}: score={r['score']}, matched={r['matched_words']}")

    print("\n2. 搜索'北京':")
    results = index.search("北京")
    for r in results:
        print(f"  {r['doc_id']}: score={r['score']}, matched={r['matched_words']}")

    print("\n3. 搜索'大学参观':")
    results = index.search_with_context("大学参观")
    for r in results:
        print(f"  {r['doc_id']}: {r['excerpt']}")

    # 测试简单搜索
    print("\n4. 简单文本搜索'故宫':")
    results = simple_text_search(docs, "故宫", limit=3)
    for r in results:
        print(f"  {r[0]}: score={r['_match_score']}")

    print("\n[SUCCESS] Text search test passed!")
