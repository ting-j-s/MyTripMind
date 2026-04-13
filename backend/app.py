"""
个性化旅游系统 - Flask应用入口
这是整个后端服务的启动文件
"""

import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS  # 解决跨域问题

# 导入各模块路由
from routes.auth import auth_bp
from routes.attractions import attractions_bp
from routes.route import route_bp
from routes.nearby import nearby_bp
from routes.diary import diary_bp
from routes.food import food_bp
from routes.user import user_bp
from routes.aigc import aigc_bp


def create_app():
    """创建Flask应用实例"""
    app = Flask(__name__)

    # 配置
    app.config['SECRET_KEY'] = 'travel-system-secret-key-2026'
    app.config['JSON_AS_ASCII'] = False  # JSON中文不转义

    # 允许跨域访问
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(attractions_bp, url_prefix='/api')
    app.register_blueprint(route_bp, url_prefix='/api/route')
    app.register_blueprint(nearby_bp, url_prefix='/api')
    app.register_blueprint(diary_bp, url_prefix='/api')
    app.register_blueprint(food_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(aigc_bp, url_prefix='/api/aigc')

    # 根路径测试
    @app.route('/')
    def index():
        return jsonify({
            'message': '个性化旅游系统 API',
            'version': '1.0',
            'status': 'running'
        })

    # 健康检查
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'ok'})

    return app


# 创建应用实例
app = create_app()


if __name__ == '__main__':
    print("=" * 50)
    print("个性化旅游系统启动中...")
    print("后端地址: http://127.0.0.1:5000")
    print("按 Ctrl+C 停止服务")
    print("=" * 50)
    # 绑定0.0.0.0允许外部访问
    app.run(debug=True, host='0.0.0.0', port=5000)
