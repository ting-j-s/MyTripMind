"""
哈希表(Hash Table)的实现 - 自己实现，不用Python内置的dict
哈希表是一种键值对数据结构，支持O(1)平均时间复杂度的查找
应用：日记ID快速查询、用户ID查询、缓存等
"""

from .linked_list import LinkedList


class HashTable:
    """
    哈希表 - 使用链地址法解决哈希冲突
    """

    def __init__(self, size=100):
        """
        初始化哈希表
        size: 哈希表的大小（槽的数量）
        """
        self._size = size
        self._buckets = [None] * size  # 桶数组
        self._count = 0  # 元素数量

    def __len__(self):
        return self._count

    def __contains__(self, key):
        """支持 'key in hash_table' 语法"""
        return self._find_bucket(key) is not None

    def _hash(self, key):
        """
        哈希函数 - 将键转换为数组索引
        时间复杂度: O(k)，k为键的长度
        """
        if isinstance(key, int):
            return key % self._size

        # 字符串哈希 - 使用经典的多项式哈希
        hash_val = 0
        prime = 31
        for char in str(key):
            hash_val = hash_val * prime + ord(char)
        return abs(hash_val) % self._size

    def _find_bucket(self, key):
        """
        查找键所在的桶
        返回: (bucket_index, node) 或 None
        """
        index = self._hash(key)
        bucket = self._buckets[index]
        if bucket is None:
            return None
        node = bucket.find_by_key(key)
        if node:
            return (index, node)
        return None

    def put(self, key, value):
        """
        插入或更新键值对 - O(1)平均
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        if bucket is None:
            # 桶为空，创建新链表
            bucket = LinkedList()
            self._buckets[index] = bucket

        # 检查是否已存在
        existing = bucket.find_by_key(key)
        if existing:
            existing.value = value  # 更新
        else:
            bucket.insert_at_head(key, value)
            self._count += 1

            # 扩容检查：负载因子 > 0.75 时扩容
            if self._count / self._size > 0.75:
                self._resize()

    def get(self, key, default=None):
        """
        获取键对应的值 - O(1)平均
        如果键不存在，返回default
        """
        result = self._find_bucket(key)
        if result:
            return result[1].value
        return default

    def delete(self, key):
        """
        删除键值对 - O(1)平均
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        if bucket is None:
            return False

        if bucket.delete_by_key(key):
            self._count -= 1
            # 如果桶空了，可以置为None节省空间
            if bucket.is_empty():
                self._buckets[index] = None
            return True
        return False

    def has(self, key):
        """检查键是否存在 - O(1)平均"""
        return self._find_bucket(key) is not None

    def _resize(self):
        """
        扩容 - 当负载因子超过0.75时调用
        时间复杂度: O(n)
        """
        old_buckets = self._buckets
        self._size *= 2
        self._buckets = [None] * self._size
        self._count = 0

        # 重新插入所有元素
        for bucket in old_buckets:
            if bucket:
                for key, value in bucket.traverse():
                    self.put(key, value)

    def keys(self):
        """返回所有键"""
        result = []
        for bucket in self._buckets:
            if bucket:
                for key, _ in bucket.traverse():
                    result.append(key)
        return result

    def values(self):
        """返回所有值"""
        result = []
        for bucket in self._buckets:
            if bucket:
                for _, value in bucket.traverse():
                    result.append(value)
        return result

    def items(self):
        """返回所有键值对"""
        result = []
        for bucket in self._buckets:
            if bucket:
                for key, value in bucket.traverse():
                    result.append((key, value))
        return result

    def load_factor(self):
        """返回负载因子"""
        return self._count / self._size

    def __repr__(self):
        items = []
        for bucket in self._buckets:
            if bucket:
                for key, value in bucket.traverse():
                    items.append(f"{key}: {value}")
        return "{" + ", ".join(items) + "}"


class HashTableIterator:
    """哈希表迭代器"""

    def __init__(self, hash_table):
        self._hash_table = hash_table
        self._bucket_index = 0
        self._node = None
        self._advance()

    def _advance(self):
        """移动到下一个有效元素"""
        while self._bucket_index < self._hash_table._size:
            bucket = self._hash_table._buckets[self._bucket_index]
            if bucket and bucket.head:
                self._node = bucket.head
                return
            self._bucket_index += 1
        self._node = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._node is None:
            raise StopIteration
        key = self._node.key
        value = self._node.value

        # 移动到链表下一个节点
        self._node = self._node.next
        if self._node is None:
            self._bucket_index += 1
            self._advance()

        return (key, value)


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("哈希表测试")
    print("=" * 50)

    ht = HashTable(size=10)

    # 插入测试
    print("\n插入操作:")
    test_data = [
        ("user_001", {"name": "张三", "age": 20}),
        ("user_002", {"name": "李四", "age": 21}),
        ("diary_001", {"title": "故宫游记", "content": "..."}),
        ("diary_002", {"title": "北大参观", "content": "..."}),
    ]

    for key, value in test_data:
        ht.put(key, value)
        print(f"  put({key}) -> 负载因子: {ht.load_factor():.2f}")

    print(f"\n哈希表内容: {ht}")
    print(f"元素数量: {len(ht)}")

    # 查找测试
    print("\n查找操作:")
    print(f"  get(user_001) = {ht.get('user_001')}")
    print(f"  get(user_999, default='不存在') = {ht.get('user_999', '不存在')}")
    print(f"  'user_001' in ht = {'user_001' in ht}")

    # 删除测试
    print("\n删除操作:")
    print(f"  delete(user_002) = {ht.delete('user_002')}")
    print(f"  delete(user_002) = {ht.delete('user_002')}")  # 再次删除
    print(f"  'user_002' in ht = {'user_002' in ht}")

    # 遍历测试
    print("\n遍历操作:")
    print("  所有键值对:")
    for key, value in ht.items():
        print(f"    {key}: {value}")

    # 扩容测试
    print("\n扩容测试:")
    print(f"  当前大小: {ht._size}")
    for i in range(50):
        ht.put(f"key_{i}", f"value_{i}")
    print(f"  插入50个元素后大小: {ht._size}")
    print(f"  负载因子: {ht.load_factor():.2f}")
