from app import ma

class GroupSchema(ma.Schema):
    class Meta:
        fields = ('group_id', 'group_name', 'users', 'hidden')

profile_schema = GroupSchema()
profiles_schema = GroupSchema(many=True)