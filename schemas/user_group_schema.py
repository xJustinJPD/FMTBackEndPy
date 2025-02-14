from app import ma

class UserGroupSchema(ma.Schema):
    class Meta:
        fields = ('user_group_id', 'user_id', 'group_id')

user_group_schema = UserGroupSchema()