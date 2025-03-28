from app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'groups', 'bio', 'role', 'stats', 'discord_id')


user_schema = UserSchema()
users_schema = UserSchema(many=True)