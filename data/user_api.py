from flask import jsonify, Blueprint, request
from werkzeug.security import generate_password_hash

import data.db_session as db_session
from data.users import User

blueprint = Blueprint('user_api', __name__, template_folder='templates')


def set_password(password):
    return generate_password_hash(password)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify({'users': [item.to_dict(
        only=('id', 'name', 'surname', 'age', 'city', 'email', 'hashed_password')
    )
        for item in users]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify({'users': users.to_dict(
        only=('id', 'name', 'surname', 'age', 'city', 'email', 'hashed_password')
    )})


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['id', 'name', 'surname', 'age', 'city', 'email']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    users = User(
        id=request.json['id'],
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        address=request.json['city'],
        email=request.json['email'],
        hashed_password=set_password(request.json['hashed_password'])
    )

    if db_sess.query(User).filter(User.id == users.id).first():
        return jsonify({'error': 'Id already exists'})
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['id', 'name', 'surname', 'age', 'city', 'email']):
        return jsonify({'error': 'Bad request'})

    users = User(
        id=request.json['id'],
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        address=request.json['city'],
        email=request.json['email'],
        hashed_password=set_password(request.json['hashed_password']),
    )
    user_to_edit = db_sess.query(User).filter(User.id == user_id).first()
    if not user_to_edit:
        return jsonify({'error': 'Not found'})
    if user_to_edit:
        user_to_edit.id = users.id
        user_to_edit.name = users.name
        user_to_edit.surname = users.surname
        user_to_edit.age = users.age
        user_to_edit.address = users.address
        user_to_edit.email = users.email
        user_to_edit.hashed_password = set_password(users.hashed_password)

    db_sess.commit()
    return jsonify({'success': 'OK'})
