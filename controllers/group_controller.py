# from flask import request, jsonify, flash, redirect, url_for
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token
# from models.Group import Group
# from models.User import User
# from schemas.group_schema import GroupSchema
# from schemas.user_schema import UserSchema
# from app import db

# group_schema = GroupSchema()
# groups_schema = GroupSchema(many=True)
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)

# def get_groups():
#     groups_list = Group.query.all()
#     result = groups_schema.dump(groups_list)
#     return jsonify(result)


# def add_user_to_group():
#     if request.method == 'POST':
#         user_id = request.form.get('user_id')  # Get selected user id
#         group_id = request.form.get('group_id')  # Get selected group id

#         # Find the user and group from the database
#         user = User.query.get(user_id)
#         group = Group.query.get(group_id)

#         if user and group:
#             # Add user to group if not already added
#             if group not in user.groups:
#                 user.groups.append(group)
#                 db.session.commit()
#                 flash(f'{user_id} has been added to {group.name}!', 'success')
#             else:
#                 flash(f'{user_id} is already in {group.name}.', 'warning')

#         else:
#             flash('User or Group not found.', 'error')

#         return redirect(url_for('add_user_to_group'))

