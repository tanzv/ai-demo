from flask_restx import fields

def create_user_info_model(api):
    """创建用户信息模型
    
    Args:
        api: Flask-RESTX API 实例
        
    Returns:
        Model: 用户信息模型
    """
    return api.model('UserInfo', {
        'id': fields.Integer(required=True, description='用户ID'),
        'username': fields.String(required=True, description='用户名'),
        'email': fields.String(required=True, description='邮箱'),
        'is_active': fields.Boolean(required=True, description='是否激活'),
        'is_superuser': fields.Boolean(required=True, description='是否超级用户'),
        'created_at': fields.DateTime(required=True, description='创建时间'),
        'updated_at': fields.DateTime(required=True, description='更新时间')
    }) 