"""
堆(Heap)的实现 - 用数组实现
堆是一种完全二叉树，分为最大堆和最小堆
应用：Top-K问题、优先队列、Dijkstra算法
"""


class MinHeap:
    """
    最小堆 - 父节点比子节点小
    Python的heapq就是最小堆，我们自己实现是为了理解原理和满足课程要求
    """

    def __init__(self):
        self._heap = []  # 用列表存储堆，索引0是根

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return len(self._heap) == 0

    def _parent(self, i):
        """返回父节点索引"""
        return (i - 1) // 2

    def _left_child(self, i):
        """返回左子节点索引"""
        return 2 * i + 1

    def _right_child(self, i):
        """返回右子节点索引"""
        return 2 * i + 2

    def _swap(self, i, j):
        """交换堆中两个元素"""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, i):
        """
        将节点向上调整 - 用于插入
        时间复杂度: O(log n)
        """
        while i > 0:
            parent = self._parent(i)
            if self._heap[i] < self._heap[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        """
        将节点向下调整 - 用于删除或构建堆
        时间复杂度: O(log n)
        """
        size = len(self._heap)
        while True:
            smallest = i
            left = self._left_child(i)
            right = self._right_child(i)

            if left < size and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < size and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    def push(self, item):
        """
        插入元素 - O(log n)
        item可以是任意对象，但需要支持比较运算
        """
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        """
        弹出最小元素 - O(log n)
        如果堆为空返回None
        """
        if self.is_empty():
            return None

        min_val = self._heap[0]
        last = self._heap.pop()

        if not self.is_empty():
            self._heap[0] = last
            self._sift_down(0)

        return min_val

    def peek(self):
        """查看最小元素，不弹出"""
        if self.is_empty():
            return None
        return self._heap[0]

    def heapify(self, items):
        """
        堆化 - 从一个列表构建堆
        时间复杂度: O(n)
        """
        self._heap = list(items)
        # 从最后一个非叶子节点开始向下调整
        for i in range(len(self._heap) // 2 - 1, -1, -1):
            self._sift_down(i)


class MaxHeap:
    """
    最大堆 - 父节点比子节点大
    Top-K问题中用最大堆维护前K大的元素
    """

    def __init__(self):
        self._heap = []

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return len(self._heap) == 0

    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * i + 2

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, i):
        while i > 0:
            parent = self._parent(i)
            # 最大堆：父节点比子节点大
            if self._heap[i] > self._heap[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i):
        size = len(self._heap)
        while True:
            largest = i
            left = self._left_child(i)
            right = self._right_child(i)

            if left < size and self._heap[left] > self._heap[largest]:
                largest = left
            if right < size and self._heap[right] > self._heap[largest]:
                largest = right

            if largest != i:
                self._swap(i, largest)
                i = largest
            else:
                break

    def push(self, item):
        self._heap.append(item)
        self._sift_up(len(self._heap) - 1)

    def pop(self):
        if self.is_empty():
            return None

        max_val = self._heap[0]
        last = self._heap.pop()

        if not self.is_empty():
            self._heap[0] = last
            self._sift_down(0)

        return max_val

    def peek(self):
        if self.is_empty():
            return None
        return self._heap[0]

    def heapify(self, items):
        self._heap = list(items)
        for i in range(len(self._heap) // 2 - 1, -1, -1):
            self._sift_down(i)


# ============================================================
# 支持自定义比较的堆元素
# ============================================================

class HeapElement:
    """
    堆元素 - 支持自定义比较key
    用于Dijkstra算法等场景
    """

    def __init__(self, value, key=None):
        """
        value: 实际存储的值
        key: 比较的键，默认为value本身
        """
        self.value = value
        self.key = key if key is not None else value

    def __lt__(self, other):
        """最小堆比较"""
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __eq__(self, other):
        if isinstance(other, HeapElement):
            return self.key == other.key
        return self.key == other

    def __repr__(self):
        return f"HeapElement({self.value}, key={self.key})"


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("最小堆测试")
    print("=" * 50)

    min_heap = MinHeap()
    test_data = [5, 3, 8, 1, 9, 2, 7]

    print(f"插入数据: {test_data}")
    for x in test_data:
        min_heap.push(x)
        print(f"  插入{x}，堆顶: {min_heap.peek()}")

    print(f"\n堆内容: {min_heap._heap}")
    print("\n弹出顺序（从小到大）:")
    result = []
    while not min_heap.is_empty():
        result.append(min_heap.pop())
    print(result)

    print("\n" + "=" * 50)
    print("最大堆测试（用于Top-K）")
    print("=" * 50)

    max_heap = MaxHeap()
    print(f"插入数据: {test_data}")
    for x in test_data:
        max_heap.push(x)
        print(f"  插入{x}，堆顶: {max_heap.peek()}")

    print(f"\n弹出顺序（从大到小）:")
    result = []
    while not max_heap.is_empty():
        result.append(max_heap.pop())
    print(result)

    print("\n" + "=" * 50)
    print("HeapElement测试（自定义比较）")
    print("=" * 50)

    # 用于Dijkstra算法
    element_heap = MinHeap()
    element_heap.push(HeapElement("A", 5))
    element_heap.push(HeapElement("B", 2))
    element_heap.push(HeapElement("C", 8))

    print("弹出演示:")
    while not element_heap.is_empty():
        e = element_heap.pop()
        print(f"  {e.value}, key={e.key}")
