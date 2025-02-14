from app import ma

class ProfileSchema(ma.Schema):
    class Meta:
        fields = ('profile_id', 'profile_fname', 'profile_lname', 'role', 'bio')

profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
