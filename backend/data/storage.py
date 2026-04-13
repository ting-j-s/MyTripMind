"""
JSON文件存储模块
负责数据的读取和写入
"""

import json
import os
from typing import List, Dict, Any


class JsonStorage:
    """
    JSON文件存储管理器

    功能：
    - 从JSON文件读取数据
    - 写入数据到JSON文件
    - 自动创建目录
    """

    def __init__(self, data_dir: str = None):
        """
        初始化存储管理器

        参数:
            data_dir: 数据目录路径，默认使用当前模块所在目录
        """
        if data_dir is None:
            # 获取当前文件所在目录（storage.py所在目录）
            data_dir = os.path.dirname(os.path.abspath(__file__))

        self.data_dir = os.path.abspath(data_dir)
        self._ensure_dir()

    def _ensure_dir(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _get_file_path(self, filename: str) -> str:
        """获取文件完整路径"""
        return os.path.join(self.data_dir, filename)

    def load(self, filename: str, default: Any = None) -> Any:
        """
        从JSON文件加载数据

        参数:
            filename: 文件名（不含路径）
            default: 默认返回值（文件不存在时）

        返回:
            文件中的数据，或default
        """
        filepath = self._get_file_path(filename)

        if not os.path.exists(filepath):
            return default

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {filename} is not valid JSON")
            return default
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return default

    def save(self, filename: str, data: Any) -> bool:
        """
        保存数据到JSON文件

        参数:
            filename: 文件名
            data: 要保存的数据

        返回:
            是否成功
        """
        filepath = self._get_file_path(filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False

    def exists(self, filename: str) -> bool:
        """检查文件是否存在"""
        filepath = self._get_file_path(filename)
        return os.path.exists(filepath)

    def delete(self, filename: str) -> bool:
        """删除文件"""
        filepath = self._get_file_path(filename)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            return True
        except Exception as e:
            print(f"Error deleting {filename}: {e}")
            return False


# 全局存储实例
_storage = None


def get_storage() -> JsonStorage:
    """获取全局存储实例"""
    global _storage
    if _storage is None:
        _storage = JsonStorage()
    return _storage
