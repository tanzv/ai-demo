from flask_restx import Namespace, Resource, fields
from flask import jsonify

# 创建命名空间
ns = Namespace('health', description='健康检查相关接口')

# 定义响应模型
health_model = ns.model('Health', {
    'status': fields.String(required=True, description='服务状态'),
    'message': fields.String(required=True, description='状态信息'),
    'version': fields.String(required=True, description='API 版本')
})

@ns.route('')
class HealthCheck(Resource):
    @ns.doc('get_health',
            description='获取服务健康状态',
            responses={
                200: ('成功', health_model),
                500: '服务器内部错误'
            })
    @ns.marshal_with(health_model)
    async def get(self):
        """获取服务健康状态"""
        return {
            'status': 'healthy',
            'message': '服务运行正常',
            'version': '1.0.0'
        } 