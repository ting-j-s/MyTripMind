"""
链表实现 - 自己动手实现，不用Python内置的list
链表是哈希表解决冲突的基础，也是理解更复杂数据结构的前提
"""


class Node:
    """链表节点"""

    def __init__(self, key=None, value=None):
        self.key = key      # 用于哈希表时存储键
        self.value = value  # 存储的值
        self.next = None    # 指向下一个节点


class LinkedList:
    """
    单向链表
    主要操作：头部插入、尾部插入、按key查找、删除、遍历
    """

    def __init__(self):
        self.head = None    # 头节点
        self.size = 0       # 节点数量

    def is_empty(self):
        """链表是否为空"""
        return self.head is None

    def length(self):
        """返回链表长度"""
        return self.size

    def insert_at_head(self, key, value=None):
        """
        头部插入节点 - O(1)
        哈希表用的就是这个
        """
        new_node = Node(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        return new_node

    def insert_at_tail(self, key, value=None):
        """
        尾部插入节点 - O(n)
        """
        new_node = Node(key, value)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
        return new_node

    def find_by_key(self, key):
        """
        按key查找节点 - O(n)
        哈希表查找时，如果哈希冲突，会在链表上线性查找
        """
        current = self.head
        while current:
            if current.key == key:
                return current
            current = current.next
        return None

    def delete_by_key(self, key):
        """
        按key删除节点 - O(n)
        """
        if self.is_empty():
            return False

        # 如果是头节点
        if self.head.key == key:
            self.head = self.head.next
            self.size -= 1
            return True

        # 在链表中查找
        current = self.head
        while current.next:
            if current.next.key == key:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def traverse(self):
        """
        遍历链表，返回所有元素
        """
        result = []
        current = self.head
        while current:
            result.append((current.key, current.value))
            current = current.next
        return result

    def to_list(self):
        """转换为Python列表"""
        return self.traverse()


# 测试代码
if __name__ == "__main__":
    print("=" * 50)
    print("链表测试")
    print("=" * 50)

    # 创建链表
    ll = LinkedList()

    # 插入测试
    print("\n插入测试:")
    ll.insert_at_head("c", 3)
    print(f"  头部插入('c', 3)")
    ll.insert_at_head("b", 2)
    print(f"  头部插入('b', 2)")
    ll.insert_at_head("a", 1)
    print(f"  头部插入('a', 1)")
    ll.insert_at_tail("d", 4)
    print(f"  尾部插入('d', 4)")

    print(f"\n链表长度: {ll.length()}")
    print(f"遍历结果: {ll.to_list()}")

    # 查找测试
    print("\n查找测试:")
    node = ll.find_by_key("b")
    print(f"  查找'b': {node.value if node else '未找到'}")

    node = ll.find_by_key("x")
    print(f"  查找'x': {node.value if node else '未找到'}")

    # 删除测试
    print("\n删除测试:")
    result = ll.delete_by_key("b")
    print(f"  删除'b': {'成功' if result else '失败'}")
    print(f"  删除后遍历: {ll.to_list()}")

    result = ll.delete_by_key("x")
    print(f"  删除'x': {'成功' if result else '失败'}")
