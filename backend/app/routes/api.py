from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from ..models.user import User
from .. import db

bp = Blueprint('api', __name__)

@bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@bp.route('/user/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
    if current_user.id != id:
        return jsonify({'error': '无权限修改其他用户信息'}), 403
        
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    return jsonify(user.to_dict()) 