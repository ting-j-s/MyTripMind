"""
AIGC服务 - 通义千问API调用
用于：根据照片和文字描述生成旅游动画
"""

import os
from typing import Dict, Optional

# 通义千问API（需要安装dashscope）
# pip install dashscope


class AIGCService:
    """
    AIGC服务类

    使用通义千问API生成旅游动画描述
    """

    def __init__(self, api_key: str = None):
        """
        初始化AIGC服务

        参数:
            api_key: 通义千问API密钥，默认从环境变量获取
        """
        self.api_key = api_key or os.environ.get('DASHSCOPE_API_KEY', '')
        self.available = bool(self.api_key)

    def generate_animation_description(self,
                                     location: str,
                                     images: list = None,
                                     user_description: str = None) -> Dict:
        """
        生成旅游动画描述

        参数:
            location: 景点名称
            images: 图片URL列表
            user_description: 用户描述

        返回:
            {
                'success': True/False,
                'description': '生成的动画描述',
                'error': '错误信息（如果失败）'
            }
        """
        if not self.available:
            return {
                'success': False,
                'description': None,
                'error': 'AIGC API未配置，请设置DASHSCOPE_API_KEY环境变量'
            }

        try:
            import dashscope
            dashscope.api_key = self.api_key

            from dashscope import MultimodalConversation
            from typing import List

            # 构建消息
            messages = []

            # 用户消息
            user_content = [
                {'text': f'请为旅游地点"{location}"生成一段动画描述。'}
            ]

            if user_description:
                user_content.append({'text': f'用户描述：{user_description}'})

            if images:
                for img in images:
                    user_content.append({'image': img})

            messages.append({
                'role': 'user',
                'content': user_content
            })

            # 调用API
            response = MultimodalConversation.call(
                model='qwen-vl-plus',
                messages=messages
            )

            if response.status_code == 200:
                return {
                    'success': True,
                    'description': response.output['choices'][0]['message']['content'],
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'description': None,
                    'error': f'API错误: {response.message}'
                }

        except Exception as e:
            return {
                'success': False,
                'description': None,
                'error': str(e)
            }


def generate_mock_animation(location: str,
                           images: list = None,
                           user_description: str = None) -> Dict:
    """
    生成模拟的动画描述（当没有API Key时使用）

    这是一个简化版本，直接返回预定义的动画描述
    """
    templates = [
        f"在{location}的精彩之旅开始了！阳光洒落在古老的建筑上，",
        f"欢迎来到{location}！跟随镜头一起探索这个美丽的地方...",
        f"让我们一起游览{location}，感受这里独特的魅力..."
    ]

    import random

    description = random.choice(templates)

    if user_description:
        description += f"\n\n用户分享：{user_description}"

    description += "\n\n（这是一段由AI生成的旅游动画描述）"

    return {
        'success': True,
        'description': description,
        'error': None,
        'mock': True  # 标记为模拟数据
    }


# 全局AIGC服务实例
_aigc_service = None


def get_aigc_service() -> AIGCService:
    """获取AIGC服务实例"""
    global _aigc_service
    if _aigc_service is None:
        _aigc_service = AIGCService()
    return _aigc_service
