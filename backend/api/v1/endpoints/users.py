from flask import Blueprint, request, jsonify
from flask_restx import Namespace, Resource, fields
from utils.auth import token_required, admin_required
from models.user import User
from config.database import AsyncSessionLocal

# 创建命名空间
ns = Namespace('users', description='用户管理相关接口')

# 定义请求/响应模型
user_model = ns.model('User', {
    'id': fields.Integer(required=True, description='用户ID'),
    'username': fields.String(required=True, description='用户名'),
    'email': fields.String(required=True, description='邮箱'),
    'is_active': fields.Boolean(required=True, description='是否激活'),
    'is_superuser': fields.Boolean(required=True, description='是否超级用户'),
    'created_at': fields.DateTime(required=True, description='创建时间'),
    'updated_at': fields.DateTime(required=True, description='更新时间')
})

user_list_model = ns.model('UserList', {
    'users': fields.List(fields.Nested(user_model)),
    'total': fields.Integer(required=True, description='总用户数'),
    'page': fields.Integer(required=True, description='当前页码'),
    'per_page': fields.Integer(required=True, description='每页数量')
})

@ns.route('')
class UserList(Resource):
    @ns.doc('get_users',
            description='获取用户列表',
            security='apikey',
            responses={
                200: ('成功', user_list_model),
                401: '未认证',
                403: '无权限',
                500: '服务器内部错误'
            })
    @ns.marshal_with(user_list_model)
    @token_required
    @admin_required
    async def get(self):
        """获取用户列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        async with AsyncSessionLocal() as session:
            # 获取总用户数
            total = await User.count(session)
            
            # 获取分页用户列表
            users = await User.get_paginated(session, page=page, per_page=per_page)
            
            return {
                'users': [user.to_dict() for user in users],
                'total': total,
                'page': page,
                'per_page': per_page
            }

@ns.route('/<int:user_id>')
@ns.param('user_id', '用户ID')
class UserDetail(Resource):
    @ns.doc('get_user',
            description='获取用户详情',
            security='apikey',
            responses={
                200: ('成功', user_model),
                401: '未认证',
                403: '无权限',
                404: '用户不存在',
                500: '服务器内部错误'
            })
    @ns.marshal_with(user_model)
    @token_required
    @admin_required
    async def get(self, user_id):
        """获取用户详情"""
        async with AsyncSessionLocal() as session:
            user = await User.get_by_id(session, user_id)
            if not user:
                return {'message': '用户不存在'}, 404
            return user.to_dict()

    @ns.doc('update_user',
            description='更新用户信息',
            security='apikey',
            responses={
                200: ('成功', user_model),
                401: '未认证',
                403: '无权限',
                404: '用户不存在',
                500: '服务器内部错误'
            })
    @ns.expect(user_model)
    @ns.marshal_with(user_model)
    @token_required
    @admin_required
    async def put(self, user_id):
        """更新用户信息"""
        data = request.get_json()
        
        async with AsyncSessionLocal() as session:
            user = await User.get_by_id(session, user_id)
            if not user:
                return {'message': '用户不存在'}, 404
            
            # 更新用户信息
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            await session.commit()
            await session.refresh(user)
            return user.to_dict()

    @ns.doc('delete_user',
            description='删除用户',
            security='apikey',
            responses={
                204: '删除成功',
                401: '未认证',
                403: '无权限',
                404: '用户不存在',
                500: '服务器内部错误'
            })
    @token_required
    @admin_required
    async def delete(self, user_id):
        """删除用户"""
        async with AsyncSessionLocal() as session:
            user = await User.get_by_id(session, user_id)
            if not user:
                return {'message': '用户不存在'}, 404
            
            await session.delete(user)
            await session.commit()
            return '', 204 