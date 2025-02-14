from app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'groups')


user_schema = UserSchema()
users_schema = UserSchema(many=True)